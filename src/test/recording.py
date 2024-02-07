from pydantic import BaseModel


class Recording(BaseModel):
    title: str
    artists: str = None
    writers: str = None
    isrcs: str = None
    iswcs: str = None
