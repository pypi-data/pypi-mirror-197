from pydantic import BaseModel
from typing import Union

class goes_url(BaseModel):
    station: str
    year: str
    day: str
    hour: str
    file: str

class goes_hour(BaseModel):
    station: str
    year: str
    day: str

class goes_file(BaseModel):
    station: str
    year: str
    day: str
    hour: str

class goes_day(BaseModel):
    station: str
    year: str

class goes_year(BaseModel):
    station: str

class Nexrad_S3_generate_url(BaseModel):
    target_bucket: str
    user_key: str

class Nexard_S3_upload_file(BaseModel):
    key: str
    source_bucket: str
    target_bucket: str

class Nexrad_S3_fetch_url(BaseModel):
    year: str
    month: str
    day: str
    station: str
    file:str

class Nexrad_S3_fetch_file(BaseModel):
    year: str
    month: str
    day: str
    station: str

class Nexrad_S3_fetch_station(BaseModel):
    year: str
    month: str
    day: str

class Nexrad_S3_fetch_day(BaseModel):
    year: str
    month: str

class Nexrad_S3_fetch_month(BaseModel):
    yearSelected: str

class ValidateFile(BaseModel):
    file_name: str

class LoginData(BaseModel):
    Username: str
    Password: str

class TokenClass(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    
    
class api_detail_fetch(BaseModel):
    api_name:str

class Nexrad_fetch_filename(BaseModel):
    filename: str

class User(BaseModel):
    username: str
    password: str
    service_plan: str
    api_limit: int

class fn_s3_fetch_keys(BaseModel):
    bucket_name: str

class fn_s3_download_file(BaseModel):
    bucket_name: str
    file_name: str

class insert_user(BaseModel):
    username: str
    hashed_password: str
    service_plan: str
    api_limit: int

class insert_user_activity(BaseModel):
    username: str
    api_name: str

class user_details(BaseModel):
    username: str

class user_details_pwd(BaseModel):
    username: str
    password: str

