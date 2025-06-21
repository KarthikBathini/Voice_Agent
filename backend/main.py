from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers import handle_command

app = FastAPI()

# ✅ Add CORS middleware to accept requests from your frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/command")
async def process_command(request: dict):
    command = request.get("command")
    if not command:
        return {"error": "No command provided"}
    result = handle_command(command)
    return {"response": result}
