import uvicorn

from core.config import app
from core.logging_config import setup_logging

setup_logging()

@app.get("/health")
def health_check():
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
