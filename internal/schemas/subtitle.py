from pydantic import BaseModel

class SubtitleRequest(BaseModel):
    text: str