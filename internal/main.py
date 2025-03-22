from fastapi import Depends, FastAPI, HTTPException

from internal.depends import get_video_service, get_subtitles_service
from internal.schemas.video import VideoRequest
from internal.services.subtitles import Subtitles
from internal.services.video import Video

app = FastAPI()

@app.post("/video")
async def create_video(body: VideoRequest, subtitles_service: Subtitles = Depends(get_subtitles_service), video_service: Video = Depends(get_video_service)):
    try:
        result = []
        for movie in subtitles_service.list():
            target = subtitles_service.find(movie_name=movie, search_text=body.text)
            
            if target:
                target['movie_name'] = movie
                result.append(target) 
        

        return result

        # if target:
        #     result_file_path = video_service.cut(
        #         video_name=movie_name,
        #         start_time=target['startTime'], 
        #         end_time=target['endTime'], 
        #     )

        #     if result_file_path.exists():
        #         response = FileResponse(result_file_path, media_type="video/mp4", filename='shorts')

        #         return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "UNKNOWN_ERROR", "message": str(e)},
        )
    
@app.post("/test")
async def test(subtitles_service: Subtitles = Depends(get_subtitles_service)):
    try:
        return None
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "UNKNOWN_ERROR", "message": str(e)},
        )
        


