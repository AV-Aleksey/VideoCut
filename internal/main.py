import re
from pathlib import Path
from fastapi import Depends, FastAPI

from internal.depends import get_utils_service, get_video_service
from internal.services.utils import Utils
from internal.services.video import Video

app = FastAPI()

@app.get("/video")
async def create_orders(utils_service: Utils = Depends(get_utils_service), video_service: Video = Depends(get_video_service)):
    file_path = Path(__file__).parent / "assets" / "bumer.srt"

    subtitles = utils_service.load_subtitles(file_path)

    text = utils_service.find_text_in_subtitles('тебя где так ездить учили ты бля', subtitles)

    video_service.cut()

    return text


