from fastapi import FastAPI

import app.models as models
from database import engine

from app.routers import user
from app.routers import book
from app.routers import reservations


app = FastAPI(title = "Expense Tracker api")
models.Base.metadata.create_all(bind = engine)

app.include_router(user.router)
app.include_router(book.router)
app.include_router(reservations.router)




@app.get('/')
def root():
    return {'message':"welcome to the library api"}