# uvicorn app.main:app --reload
from fastapi import FastAPI
from app.api.routes import router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

app = FastAPI(
    title="Production AI Agent System",
    version="1.0.0",
    description="AI Agent powered by FastAPI + LangChain + Groq"
)

app.include_router(router)

# Static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
def root():
    return {"message": "API running"}

# Chat UI
@app.get("/chat")
def chat_ui():
    return FileResponse("frontend/templates/chat.html")

for route in app.routes:
    print("REGISTERED ROUTE:", route.path)