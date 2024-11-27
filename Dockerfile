FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Install FastAPI and other dependencies
RUN pip install fastapi uvicorn

# Install any other dependencies here