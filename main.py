from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from user.router import user_router
from preinscription.router import preregiter_router
from demande.router import demande_router
from rattrapage.router import rattrapge_router
from stage.router import stage_router
from directeur.router import directeur_router
from enseignantdemande.router import enseignantdemande_router
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(user_router)
app.include_router(preregiter_router)
app.include_router(demande_router)
app.include_router(rattrapge_router)
app.include_router(stage_router)
app.include_router(directeur_router)
app.include_router(enseignantdemande_router)



""" allows a server to indicate any origins (domain, scheme, or port) """
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=4000, reload=True)