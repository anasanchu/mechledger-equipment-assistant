"""Legacy entrypoint launcher for IKB-RAG API.

Maintained at the project root for seamless backward compatibility.
The full modular implementation resides in api/main.py.
"""

from api.main import app
from config.settings import API_HOST, API_PORT

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
