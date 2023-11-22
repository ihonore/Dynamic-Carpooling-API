from .api_router import api_router as router

# router=APIRouter()

@router.get("/")
def home():
    return {"status":200,"message":"Welcome to the API"}