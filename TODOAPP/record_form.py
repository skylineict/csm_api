from pydantic import BaseModel,Field,field_validator,EmailStr


class Token(BaseModel):
    access_token : str
    token_type : str



class OtpCreate(BaseModel):
    otp: str = Field( description="A 5-digit OTP (One Time Password) sent to your email.- This OTP expires in 20 minutes.",
                     
        min_length=5,
        max_length=5,
        example="12345",
        title='this is my otp')
    
class Change_password(BaseModel):
       password : EmailStr
       comfirm_password: EmailStr
      
       @field_validator('password')
       def password_validator(value):
             
             if len(value) < 10:
                  raise ValueError('Password must be at least 10 characters long')
        
            
            


        # if len(value) < 10:
        #          raise ValueError('Password must be at least 10 characters long')
        
        # if not re.search(r"\d", value):
        #     raise ValueError("Password must contain at least one number.")
        # return value