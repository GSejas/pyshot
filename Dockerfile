FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/home/vscode/.local/bin:$PATH"

# Set the working directory
WORKDIR /workspace

# Copy only the necessary files for installing dependencies
COPY pyproject.toml poetry.lock* /workspace/

# Copy the README file
COPY README.md /workspace/

# Install dependencies
RUN pip install poetry
# Install dependencies
RUN poetry install