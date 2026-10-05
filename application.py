"""Azure App Service entry point compatible with default Gunicorn WSGI and ASGI."""
from a2wsgi import ASGIMiddleware
from app.main import app as fastapi_app

# Azure App Service default fallback command is: gunicorn application:app
# ASGIMiddleware translates WSGI requests from standard Gunicorn into FastAPI ASGI
app = ASGIMiddleware(fastapi_app)
