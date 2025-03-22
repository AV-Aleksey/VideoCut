from internal.services.subtitles import Subtitles
from internal.services.video import Video

subtitles_service = Subtitles()
video_service = Video()

async def get_subtitles_service() -> Subtitles:
    return subtitles_service

async def get_video_service() -> Video:
    return video_service