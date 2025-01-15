from pydantic import BaseModel

class FollowRequest(BaseModel):
    followed_id: int


class Create_category(BaseModel):
    name: str
    description: str
    




