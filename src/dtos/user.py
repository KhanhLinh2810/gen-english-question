from pydantic import BaseModel


class UserDto(BaseModel):
    id: int
    username: str
    email: str

    model_config = {
        "from_attributes": True,
    }