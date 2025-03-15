from internal.services.utils import Utils
from internal.services.video import Video

utils_service = Utils()
video_service = Video()

async def get_utils_service() -> Utils:
    return utils_service

async def get_video_service() -> Video:
    return video_service