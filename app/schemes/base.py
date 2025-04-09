from pydantic import BaseModel


class DBEntityReader(BaseModel):
    class Config:
        from_attributes = True
