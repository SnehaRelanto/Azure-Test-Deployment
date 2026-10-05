"""Entry point script for local development and testing."""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting FastAPI Welcome Portal at http://127.0.0.1:8000")
    print("📖 Interactive API docs available at http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
