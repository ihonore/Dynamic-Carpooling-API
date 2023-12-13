from .api_router import api_router
from .users_routes import router as users_router
from .welcome_routes import router
from .offers_routes import router as offers_router
from .demands_routes import router as demands_router
from .computations_routes import router as computations_router


api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(offers_router, prefix="/offers", tags=["Offers"])
api_router.include_router(demands_router, prefix="/demands", tags=["Demands"])
api_router.include_router(computations_router, prefix="/computations", tags=["Computations"])
