from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models as models
from database import engine

from app.routers import user
from app.routers import book
from app.routers import reservations
from app.routers import admin


app = FastAPI(title="Library Management API")

# Configure CORS Middleware
origins = [
    "http://localhost:5173",    # Local Vite frontend
    "http://127.0.0.1:5173",  # Alternative local address
    "*",                        # Allow all origins (useful during early dev/testing)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allows requests from specified domains or all origins
    allow_credentials=True,
    allow_methods=["*"],         # Allows all HTTP methods (GET, POST, PUT, PATCH, DELETE, OPTIONS)
    allow_headers=["*"],         # Allows all headers (Authorization, Content-Type, etc.)
)

models.Base.metadata.create_all(bind=engine)

# Routers
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(book.router)
app.include_router(reservations.router)


@app.get('/')
def root():
    return {'message': "welcome to the library api"}