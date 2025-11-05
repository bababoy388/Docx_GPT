from fastapi import FastAPI
from backend.app.api.routers import docx, user
from backend.app.crud.database import engine, Base

import uvicorn


Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/"
)

app.include_router(docx.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app)

