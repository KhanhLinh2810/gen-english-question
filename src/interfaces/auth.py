from pydantic import BaseModel, Field

class ILogin(BaseModel):
    username: str
    password: str

class IPagination(BaseModel):
    paging: int = Field(1, ge=1)
    limit: int = Field(10, ge=1)
    sort_by: str = "id",
    sort_order: str = 'asc',

    @property
    def offset(self):
        return (self.page - 1) * self.limit
