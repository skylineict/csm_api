from fastapi import FastAPI,Query,Path
from  enum  import Enum
from pydantic import BaseModel,Field
from typing import Annotated,Literal

app = FastAPI()

@app.get('/items/{itmes_id}')
async def read_me(itmes_id: int):
    return {'message': itmes_id}


@app.get('/users/skyline')
async def user_name():
    return {'user_id': 'this is a current user'}

@app.get('/users/{user_id}')
async def uses(user_id: str):
    return {'user_id': user_id}


class Students_roles(str, Enum):
    leader = 'leader'
    member = 'member'
    president = "president"

@app.get('/names/{students_role}')
async def student_name(student_role: Students_roles ):
    if student_role is  Students_roles.leader:
        return { 'student roles': student_role, "info": 'welcome you have acess in the group'}
        
    

    if student_role.value == 'president':
        return { 'student roles': student_role, "info": 'welcome mr president in this program'}
    else:
        return { 'student roles': student_role, "info": 'you are a member welcome '}

studentmain = [
    {"name": "Alice"},
    {"name": "Bob"},
    {"name": "Charlie"},
    {"name": "David"},
    {"name": "Eva"},
    {"name": "Frank"},
    {"name": "Grace"},
    {"name": "Hannah"},
    {"name": "Ivy"},
    {"name": "Jack"}
]
#getting pagnation documentation
@app.get('/items_students/')
async def dataset(skip: int=0, limit: int = 10):
    return studentmain[skip: skip + limit] 


items_db = [
    {"id": "1", "name": "Foo Item", "description": "A foo item"},
    {"id": "2", "name": "Bar Item", "description": "A bar item"},
    {"id": "3", "name": "Baz Item", "description": "A baz item"},
    {"id": "4", "name": "olisa macaulay", "description": "software dev very good at what i do "},
]


#this is a search function for api
@app.get('/search/')
async def seach_items(item_id:  str | None=None, q:str | None=None):
   
    if item_id:
         items = next((item for item in items_db if item['id']== item_id),None)
         return {'items': items}
    if q:
        search_items  =  [item2 for item2 in items_db if q.lower() in item2['name'].lower() or q.lower()  in item2['description'].lower()]
        return {'items': search_items}
    
    return{'error': 'item is not found '}
    
  

@app.get('/users/{user_id}/items/{item_id}')
async def user_info(user_id: int, itme_id: str, q:str | None=None, short: bool =False):
    item = {
        "item": itme_id, "owner":  user_id
    }

    if q:
        item.update({
            'q':q})
    if not short:
        item.update({
            'descrition': "this is an amazing item that has long decription"

        })


        return item
       



class Items(BaseModel):
    name: str
    description : str | None=None
    price: float
    tax: float  | None=None

#create 
@app.post('/product/')
async def create_product(item: Items):
    item_dict = item.dict()
    if item.tax:
        add_price  = item.price + item.tax
        item_dict.update({'price_with_tax': add_price})
    return item_dict




#update
@app.put('/product/{product_id}')
async def update_product(product_id: int, item: Items):

    return {"item_id":product_id, **item.dict() }



@app.put('/sales/{sales_id}')
async def prdouct_sales(sales_id: int, item: Items, q:str | None=None):
     result = {"item_id":sales_id, **item.dict() }

     if q:
         result.update({'q':q})
     return result
        
    

@app.get('/sales')
async def func(q: Annotated[str |None, Query(min_length=3,max_length=10)] = None):
     result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
     if q:
         result.update({'q':q})
     return result
        
    


@app.get('/searchitem')
async def seachitem(q: Annotated[str |None, Query( alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,)] = None):
     result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
     if q:
         result.update({'q':q})
     return result
        
    


@app.get('/check{item_id}')
async def sales(item_id: Annotated[int, Path(title='enter id to get item', gt=2)],
                q: Annotated[list[str] |None, Query(min_length=3,max_length=10)] = None):
     result = {"items":item_id}
    
     if q:
         result.update({'q':q})
     return result
        
        

class FilterParams(BaseModel):
    model_config = {'extra': "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
    
@app.get('/items_tag/')
async def items_tag(filter: Annotated[FilterParams, Query()]):
    return filter
    
    
    # return {'items': item_id, 'q':q}