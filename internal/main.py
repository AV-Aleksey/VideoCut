
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse

from internal.depends import get_utils_service, get_video_service
from internal.schemas.video import VideoRequest
from internal.services.utils import Utils
from internal.services.video import Video

app = FastAPI()

@app.post("/video")
async def create_orders(body: VideoRequest, utils_service: Utils = Depends(get_utils_service), video_service: Video = Depends(get_video_service)):
    try:
        file_path = Path(__file__).parent / "assets" / "bumer.srt"

        subtitles = utils_service.load_subtitles(file_path)

        text = utils_service.find_text_in_subtitles(body.text, subtitles)

        if text:
            [start, end] = utils_service.convert_and_round_time(text[0])

            input_file = Path(__file__).parent / "assets" / "bumer.mp4"  # Входной файл
            start_time = start  # Время начала
            end_time = end   # Время окончания
            output_dir = Path(__file__).parent / "assets" / "results"  # Папка для результата
            video_name = "bumer"

            result_file_path = video_service.cut(input_file, start_time, end_time, output_dir, video_name)

            if result_file_path.exists():
                response = FileResponse(result_file_path, media_type="video/mp4", filename='shorts')

                return response

        return None
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "UNKNOWN_ERROR", "message": str(e)},
        )
        


