from pydantic import BaseModel


# Sample input item for testing and simulation purposes.
class Recording(BaseModel):
    title: str
    artists: str = None
    writers: str = None
    isrcs: str = None
    iswcs: str = None
