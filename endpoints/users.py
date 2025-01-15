from fastapi import APIRouter
from enum import Enum

router = APIRouter()

class StudentsRoles(str, Enum):
    leader = 'leader'
    member = 'member'
    president = "president"

@router.get('/users/skyline')
async def user_name():
    return {'user_id': 'this is a current user'}

@router.get('/users/{user_id}')
async def uses(user_id: str):
    return {'user_id': user_id}

@router.get('/names/{student_role}')
async def student_name(student_role: StudentsRoles):
    if student_role is StudentsRoles.leader:
        return {'student roles': student_role, "info": 'welcome you have access in the group'}
    if student_role.value == 'president':
        return {'student roles': student_role, "info": 'welcome Mr. President to this program'}
    else:
        return {'student roles': student_role, "info": 'you are a member, welcome'}
