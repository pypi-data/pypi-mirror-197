import ast
import json
import sqlite3
import os
from fastapi import Depends, FastAPI, Response, status, APIRouter
import requests
import sys
import boto3
import random
import string
from fastapi.security import OAuth2PasswordBearer, SecurityScopes


# Navigate to the project directory

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from backend import nexrad_main, oauth2
from backend import nexrad_file_retrieval_main
from pydantic import BaseModel
import pandas as pd
import re
from backend import schema



# app = FastAPI()

router = APIRouter()



@router.get('/nexrad_s3_fetch_db')
async def nexrad_s3_fetch_db(getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):

    """Fetches the database from the S3 bucket
    
    Args:
        None
        
    Returns:
        None"""

    nexrad_main.fetch_db()
    nexrad_main.write_logs("Status: 200, Message: Database fetched from S3 bucket")

    return Response(status_code=status.HTTP_200_OK)
    



@router.get('/nexrad_s3_fetch_month')
async def nexrad_s3_fetch_month(nexrad_s3_fetch_month: schema.Nexrad_S3_fetch_month):#, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):

    """Generates the list of months for the year chosen by the user
    
    Args:
        year (str): year chosen by the user
        
    Returns:
        list: Returns the list of months"""


    if not re.match(r"^[0-9]{4}$", nexrad_s3_fetch_month.yearSelected):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    if int(nexrad_s3_fetch_month.yearSelected) < 2022 or int(nexrad_s3_fetch_month.yearSelected) > 2023:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    nexrad_main.write_logs("Status: 200, Message: Month list generated for the year " + nexrad_s3_fetch_month.yearSelected)

    return {"Month": nexrad_main.get_distinct_month(nexrad_s3_fetch_month.yearSelected)}

@router.get('/nexrad_s3_fetch_day')
async def nexrad_s3_fetch_day(nexrad_s3_fetch_day: schema.Nexrad_S3_fetch_day):#, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):
    
    """Generates the list of days for the month chosen by the user
    
    Args:
        year (str): year chosen by the user
        month (str): month chosen by the user
        
    Returns:
        list: Returns the list of days"""
        
    # In the database the month is stored as 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 but in the bucket its stored as 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12


    if not re.match(r"^(1[0-2]|[1-9])$", nexrad_s3_fetch_day.month):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    if int(nexrad_s3_fetch_day.month) < 1 or int(nexrad_s3_fetch_day.month) > 12 :
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    nexrad_main.write_logs("Status: 200, Message: Day list generated for the month " + nexrad_s3_fetch_day.month + " of the year " + nexrad_s3_fetch_day.year)

    print(nexrad_s3_fetch_day.year, nexrad_s3_fetch_day.month)

    return {"Day": nexrad_main.get_distinct_day(nexrad_s3_fetch_day.year, nexrad_s3_fetch_day.month)}

@router.get('/nexrad_s3_fetch_station')
async def nexrad_s3_fetch_station(nexrad_s3_fetch_station: schema.Nexrad_S3_fetch_station):#, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):
    
    """Generates the list of stations for the day chosen by the user
    
    Args:
        year (str): year chosen by the user
        month (str): month chosen by the user
        day (str): day chosen by the user
        
    Returns:
        list: Returns the list of stations"""

    # In the database the day is stored as 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.... but in the bucket its stored as 01, 02, 03, 04, 05, 06, 07, 08, 09, 10....
        
    if not re.match(r"^(3[01]|[12][0-9]|[1-9])$", nexrad_s3_fetch_station.day):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    if int(nexrad_s3_fetch_station.day) < 1 or int(nexrad_s3_fetch_station.day) > 31:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    else:
        nexrad_main.write_logs("Status: 200, Message: Station list generated for the day " + nexrad_s3_fetch_station.day + " of the month " + nexrad_s3_fetch_station.month + " of the year " + nexrad_s3_fetch_station.year)
        return {"Station": nexrad_main.get_distinct_station(nexrad_s3_fetch_station.year, nexrad_s3_fetch_station.month, nexrad_s3_fetch_station.day)}



@router.get('/nexrad_s3_fetch_file')
async def nexrad_s3_fetch_file(nexrad_s3_fetch_file: schema.Nexrad_S3_fetch_file):#, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):

    """Generates the list of files for the station chosen by the user
        
    Args:
        
        year (str): year chosen by the user
        month (str): month chosen by the user
        day (str): day chosen by the user
        station (str): station chosen by the user
        
    Returns:
        list: Returns the list of files"""
    


    if not re.match(r"^[A-Z0-9]{4}$", nexrad_s3_fetch_file.station):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    else:
        if len(nexrad_s3_fetch_file.month) == 1:
            nexrad_s3_fetch_file.month = '0' + nexrad_s3_fetch_file.month
        if len(nexrad_s3_fetch_file.day) == 1:
            nexrad_s3_fetch_file.day = '0' + nexrad_s3_fetch_file.day


        s3 = nexrad_main.createConnection()
        lst = []
        bucket = 'noaa-nexrad-level2'
        result = s3.list_objects(Bucket= bucket , Prefix= nexrad_s3_fetch_file.year + "/" + nexrad_s3_fetch_file.month + "/" + 
        nexrad_s3_fetch_file.day + "/" + nexrad_s3_fetch_file.station + "/", Delimiter='/')
        for o in result.get('Contents'):
            lst.append(o.get('Key').split('/')[4])

        nexrad_main.write_logs("Status: 200, Message: File list generated for the station " + nexrad_s3_fetch_file.station + " of the day " + nexrad_s3_fetch_file.day + " of the month " + nexrad_s3_fetch_file.month + " of the year " + nexrad_s3_fetch_file.year)
        return {"File": lst} 




@router.post('/nexrad_s3_fetchurl')
async def nexrad_s3_fetchurl(nexrad_s3_fetch: schema.Nexrad_S3_fetch_url): #, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):

    """Generates the link for the file in the nexrad S3 bucket
    
    Args:
        year (str): year chosen by the user
        month (str): month chosen by the user
        day (str): day chosen by the user
        station (str): station chosen by the user
        file (str): file chosen by the user
        
    Returns:
        str: Returns the url of the file"""

    
    if not re.match(r"^[A-Z0-9]{4}\d{8}_\d{6}.*$", nexrad_s3_fetch.file):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


    else:
        if len(nexrad_s3_fetch.month) == 1:
            nexrad_s3_fetch.month = '0' + nexrad_s3_fetch.month
        if len(nexrad_s3_fetch.day) == 1:
            nexrad_s3_fetch.day = '0' + nexrad_s3_fetch.day

        url = "https://noaa-nexrad-level2.s3.amazonaws.com/" + nexrad_s3_fetch.year + "/" + nexrad_s3_fetch.month + "/" + nexrad_s3_fetch.day + "/" \
        +  nexrad_s3_fetch.station + "/" + nexrad_s3_fetch.file

        response = requests.get(url)
        if response.status_code == 200:
            nexrad_main.write_logs("link generated for the User bucket")
            nexrad_main.write_logs(url)
            return {"Public S3 URL": url}
        else:
            nexrad_main.write_logs("Status: 404, Message: File not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/nexrad_s3_fetch_key')
async def getKey(nexrad_s3_fetch: schema.Nexrad_S3_fetch_url, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):
    """Generates the key for the file in the nexrad S3 bucket
    
    Args:
        
        year (str): year chosen by the user
        month (str): month chosen by the user
        day (str): day chosen by the user
        station (str): station chosen by the user
        file (str): file chosen by the user
        
    Returns:
        str: Returns the key of the file in the S3 bucket"""    


    s3 = nexrad_main.createConnection()
    bucket = 'noaa-nexrad-level2'
    result = s3.list_objects(Bucket=bucket, Prefix= nexrad_s3_fetch.year + "/" + nexrad_s3_fetch.month + "/" + nexrad_s3_fetch.day + "/" + nexrad_s3_fetch.station
    + "/" , Delimiter='/')
    for o in result.get('Contents'):
        if nexrad_s3_fetch.file in o.get('Key'):
            nexrad_main.write_logs("Status: 200, Message: Key generated for the file " + nexrad_s3_fetch.file)
            return {'Key' : (o.get('Key'))}

@router.post('/nexrad_s3_upload')
async def uploadFiletoS3(nexrad_s3_upload: schema.Nexard_S3_upload_file, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):

    """Uploads the file to the S3 bucket

    Args:
        key (str): The key of the file
        source_bucket (str): source bucket name
        target_bucket (str): target bucket name

    Returns:
        str: Returns the key of the uploaded file
    """
    
    s3 = boto3.resource('s3',
         aws_access_key_id= os.environ.get('AWS_ACCESS_KEY1'),
         aws_secret_access_key= os.environ.get('AWS_SECRET_KEY1')
    )
    copy_source = {
        'Bucket': nexrad_s3_upload.source_bucket,
        'Key': nexrad_s3_upload.key
    }
    uploaded_key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    s3.meta.client.copy(copy_source, nexrad_s3_upload.target_bucket , uploaded_key)

    nexrad_main.write_logs("File uploaded to the S3 bucket from source destination to target destination")
    return {'Uploaded_Key': uploaded_key}


@router.post('/nexrad_s3_generate_user_link')
async def generateUserLink(nexrad_s3_generate_url: schema.Nexrad_S3_generate_url, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):
    """Generates the user link in public s3 bucket

    Args:
        bucket_name (str): name of the user bucket
        key (str): Key name of the file

    Returns:
        str: Returns the url of the file
    """

    url = "https://" + nexrad_s3_generate_url.target_bucket + ".s3.amazonaws.com" + "/" + nexrad_s3_generate_url.user_key
    nexrad_main.write_logs("link generated for the Nexxrad bucket")
    nexrad_main.write_logs(url)
    print(url)
    return {'User S3 URL': url}



@router.post('/retrieve_plot_data')
async def retrieve_plot_data(getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):
    database_file_name = "assignment_01.db"
    database_file_path = os.path.join(project_dir, os.path.join('data/',database_file_name))
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query("SELECT * FROM nexrad_plot_new_table", db)
    df_dict = df.to_dict(orient='records')
    db.close()
    return {'df_dict':df_dict, 'status_code': '200'}

@router.post('/create_plot_table')
async def create_plot_table():
    database_file_name = "assignment_01.db"
    database_file_path = os.path.join(project_dir, os.path.join('data/',database_file_name))
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE if not exists NEXRAD_PLOT (Id,State,City,ICAO_Location_Identifier,Coordinates,Lat,Lon)''')
    df = pd.read_csv(os.path.join(project_dir, "data/Nexrad.csv"))
    df["Lon"] = -1 * df["Lon"]
    df.to_sql('nexrad_plot_new_table', db, if_exists='append', index=False)
    db.commit()
    db.close()
    return {'status_code': '200'}


@router.post('/nexrad_get_download_link')
async def nexrad_download_link(nexrad_filename: schema.Nexrad_fetch_filename): #, getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):

    """Generates the link for the file in the nexrad S3 bucket
    
    Args:
        filename (str): filename entered by the user
        
    Returns:
        str: Returns the response from backend function get_nexrad_file_url"""
    
    nexrad_file_retrieval_main.write_logs("NEXRAD_File_Link_Retrieval: API Request Initiated")
    
    response = nexrad_file_retrieval_main.get_nexrad_file_url(nexrad_filename.filename)
    return {"Response": response}