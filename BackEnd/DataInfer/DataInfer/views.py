from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .form import UploadFileForm
import os
from django.conf import settings
import csv
import chardet

import pandas as pd
import json
import numpy as np
import re

dtype_mapping = {
        'object': 'Text',
        'int64': 'Integer',
        'int32': 'Integer',
        'int16': 'Integer',
        'int8': 'Integer',
        'float64': 'Float',
        'float32': 'Float',
        'bool': 'Boolean',
        'datetime64[ns]': 'DateTime',
        'timedelta[ns]': 'DateTime',
        'category': 'Category',    
        }



def reverseMap(map):
    reversed_map = {}
    for key, value in map.items():
        if value not in reversed_map:
            reversed_map[value] = []
        reversed_map[value].append(key)
    return reversed_map


@csrf_exempt
def submit_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Manually parse JSON data
        print(data['keys'])
        print(data['newValues'])
        # new_values = list(data.values())
        # print("new data form is ", new_values)
        # # keys = request.session['keys_from_values']
        # print(request.session)
        # print("keys_from_values ", request.session.get('keys_from_values', []))
        for group, value in zip(data['keys'], data['newValues']):
            for key in group:
                if key in dtype_mapping:
                    dtype_mapping[key] = value
        
        print(dtype_mapping)
        return JsonResponse(data['result'])
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=400)

@csrf_exempt
def file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file, e.g., save it
            result = handle_uploaded_file(request.FILES['file'])
            
            # Extract schema as a dictionary
            schema = {column: str(dtype) for column, dtype in result.dtypes.iteritems()}

            message = map_dtypes_to_friendly_names(result)
            current_value=list(message.values())
            reversed_dtype_mapping = reverseMap(dtype_mapping)
            keys_from_values = [reversed_dtype_mapping.get(value, []) for value in current_value]
            
            print(message)
            data = {
                'message':json.dumps(message),
                'origin': keys_from_values,

            }

            return JsonResponse(data, status=200,safe=False)
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=400)

def handle_uploaded_file(f):
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    if  not file_path.endswith('.csv'):
        print("Excl file upload "+file_path)
        try:
            df = pd.read_excel(file_path,engine='xlrd', nrows=10000)
            df = infer_and_convert_data_types(df)
            # print(df.head())
            return df

        except :
            df = pd.read_excel(file_path,engine='openpyxl',nrows=10000)
            df = infer_and_convert_data_types(df)
            # print(df)
            return df

     # After saving the file, read it back
    else: 
        df = pd.read_csv(file_path, nrows=10000)
        df = infer_and_convert_data_types(df)
        # print(df)
        return df


def looks_like_date(num):
    str_num = str(num)
    
    if len(str_num) >= 10: 
        year, month, day = float(str_num[:4]), float(str_num[4:6]), float(str_num[6:])

        if 1800 <= year <= 2024 and 1 <= month <= 12 and 1 <= day <= 31:
            return True
   
    return False

def reform(num):
    str_num = str(num)
    try:
        # new = str_num.split(",")
        new = re.split(r'[, .]+', str_num)
    
        result = '-'.join(str(number) for number in new)
        return result
        
    except:
        return num

def check(num):
    str_num = str(num)
    current = str_num.split("-")
    if len(str(current[0])) == 4 and len(str(current[1])) == 2:
        return True
    return False

def infer_and_convert_data_types(df):
    # Check if the DataFrame has enough rows
    if len(df) > 10000:
        # Randomly sample 10000 rows from the DataFrame
        df = df.sample(n=10000, random_state=42)  # random_state for reproducibility
    else:
        print("The file has less than 10,000 rows.")

    for col in df.columns:

        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')
        if not df_converted.isna().all():  # If at least one value is numeric            
            col_type = df[col].dtype
            c_min = df_converted.min()
            c_max = df_converted.max()
            if str(col_type)[:3] == "int": # if all values are int-based [1,2,3,4] -> int type
                # check the precision for different int type
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype("int8", errors='ignore')
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype("int16",errors='ignore')
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype("int32",errors='ignore')
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype("int64",errors='ignore')
            # [1.3, 2.4, 4.5] -> float
            # [1, 2.4, 4] -> float
            # elif str(col_type)[:3] == "flo": # if one of values is float-based 
            #     if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
            #         print(df[col])
            #         df[col] = df[col].astype("float32",errors='ignore')
                    
            #     else:
            #         df[col] = df[col].astype("float64",errors='ignore')
            elif str(col_type)[:3] == "obj": # if values include other type
                # [1, 2, 3, Not available] -> int
                # [1.3, 4, 5, Not avalible] -> float
                df[col] = df_converted
                
                if(not df[col].apply(looks_like_date).any()):
                    
                    if df[col].isna().any():
                        df[col] = df[col].fillna(0) # change Nah value to 0.0
                        
                        if (df[col].mod(1) == 0).all():
                            print("All values in the column are integers.")
                            # Convert to integer 
                            df[col] = df[col].astype('int')
                        else: 
                            df[col] = df[col].astype('float')
        
        # Attempt to convert to datetime
        if str(df[col].dtype)[:5] == 'float':
            try:
                # print(df[col].apply(looks_like_date))
                if(df[col].apply(looks_like_date).any()):
                    df[col] = pd.to_datetime(df[col])
                    # print(df[col])
                    continue
                else:
                    try:
                        if df[col].apply(reform).apply(check).any():
                            df[col] = df[col].apply(reform)
                            # df[col] = pd.to_datetime(df[col].apply(reform))
                            
                    except:
                        pass
            except (ValueError, TypeError):
                pass
        # print(df[col])

        if(df[col].dtype == object):
            try:
                # print(df[col].apply(looks_like_date))
                df[col] = pd.to_datetime(df[col].apply(reform))
                # print(df[col])
                continue
            except (ValueError, TypeError):
                pass
            # Attempt to convert to Bool
            if df[col].isin([True,False]).any():
                df[col] = df[col].astype('bool')
                
                # Check if the column should be categorical
            elif len(df[col].unique()) / len(df[col]) < 0.8:  # Example threshold for categorization
                df[col] = pd.Categorical(df[col])
        
    return df


def map_dtypes_to_friendly_names(df):
    # Define a dictionary that maps pandas dtypes to user-friendly names

    
    # Use the dtype mapping to replace dtype names
    friendly_dtypes = {col: dtype_mapping[str(df[col].dtype)] for col in df.columns}
    return friendly_dtypes
