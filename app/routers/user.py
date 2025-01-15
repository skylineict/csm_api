from fastapi import APIRouter

router = APIRouter

@router.get('/user/')
async def list_user():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}
