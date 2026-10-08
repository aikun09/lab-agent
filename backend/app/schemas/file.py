from pydantic import BaseModel


class FileResponse(BaseModel):
    origin_name: str
    disk_name: str
    size: int
    url: str
