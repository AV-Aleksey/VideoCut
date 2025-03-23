import time
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse

from internal.depends import get_video_service, get_subtitles_service
from internal.schemas.subtitle import SubtitleRequest
from internal.schemas.video import DownloadVideoRequest, StreamVideoRequest
from internal.services.subtitles import Subtitles
from internal.services.video import Video

app = FastAPI()

@app.post("/video")
async def create_video(body: SubtitleRequest, subtitles_service: Subtitles = Depends(get_subtitles_service), video_service: Video = Depends(get_video_service)):
    try:
        start_time = time.time()

        result = []
        for movie in subtitles_service.list():
            target = subtitles_service.find(movie_name=movie, search_text=body.text)
            
            if target:
                target['movie_name'] = movie
                result.append(target) 
        

        end_time = time.time()
        execution_time = end_time - start_time

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "UNKNOWN_ERROR", "message": str(e)},
        )
    
@app.post("/download-video")
async def download(body: DownloadVideoRequest, video_service: Video = Depends(get_video_service)):
    try:
        result_file_path = video_service.cut(
            video_name=body.movie_name,
            start_time=body.start_time, 
            end_time=body.end_time, 
        )

        if result_file_path.exists():
            response = FileResponse(result_file_path, media_type="video/mp4", filename='shorts')

            return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "UNKNOWN_ERROR", "message": str(e)},
        )
    

@app.post("/stream")
async def stream(body: StreamVideoRequest, video_service: Video = Depends(get_video_service)):
    try:
        return StreamingResponse(
            video_service.stream(video_name=body.movie_name, start_time=body.start_time, end_time=body.end_time), 
            media_type="video/mp4"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "UNKNOWN_ERROR", "message": str(e)},
        )
        


