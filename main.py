"""
DropOrCop API - Root Application Entrypoint
Forwarding entrypoint pointing to api.main:app.
Supports running:
  uvicorn main:app --reload
  python main.py
"""

from api.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
