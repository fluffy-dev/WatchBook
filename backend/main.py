import uvicorn

from src.app import get_app

app = get_app()

if __name__ == "__main__":
    """
    
    Entry point of the backend app,
    
    for now just uvicorn startup into localhost:8000
    
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)