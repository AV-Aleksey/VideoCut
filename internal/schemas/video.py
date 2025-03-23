from pydantic import BaseModel

class DownloadVideoRequest(BaseModel):
    movie_name: str
    start_time: str 
    end_time: str 

class StreamVideoRequest(BaseModel):
    movie_name: str
    start_time: str 
    end_time: str 