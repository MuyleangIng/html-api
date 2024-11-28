from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
import os

# Initialize FastAPI app
app = FastAPI()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Ensure uploads folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory user storage
users = []

# User schema for validation
class User(BaseModel):
    id: int
    name: str
    email: str

### HTML Rendering and File Upload Endpoints ###

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render the template with Jinja2
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(name: str = Form(...), file: UploadFile = File(...)):
    # Save uploaded file
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": f"File '{file.filename}' uploaded successfully by {name}!", "path": file_location}

### User Management Endpoints ###

@app.get("/users/", response_model=list[User])
async def get_users():
    """Retrieve all users."""
    return users

@app.post("/users/")
async def create_user(id: int = Form(...), name: str = Form(...), email: str = Form(...)):
    """Create a new user."""
    # Check for duplicate ID
    if any(existing_user.id == id for existing_user in users):
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    
    new_user = User(id=id, name=name, email=email)
    users.append(new_user)
    return new_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
