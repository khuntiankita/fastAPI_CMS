from pydantic import BaseModel

class Contact(BaseModel):
    id:int
    name:str
    lastname:str
    mobile_number:int
