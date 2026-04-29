from fastapi import FastAPI
from app.api.routes import auth, boards, sections, tickets
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(boards.router)
app.include_router(sections.router)
app.include_router(tickets.router)

@app.get("/")
def root():
    return {"message": "Trello Capstone API running"}