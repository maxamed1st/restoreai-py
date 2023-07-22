from fastapi import APIRouter

router = APIRouter()

def authorize():
    #authorize user upon register/login
    return "user authorized"

@router.post("/auth/login")
async def login():
    #authenticate user
    return "login"

@router.post("/auth/register")
async def register():
    #register a new user
    return "register"

@router.post("/auth/reset")
async def resetPassword():
    #reset password
    return "reset password"
