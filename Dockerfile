
FROM mcr.microsoft.com/playwright:v1.49.0-noble

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.in-project true

# Create a directory for screenshots
RUN mkdir -p /screenshots

# Copy the application code
COPY . /pyshot

# Set the working directory
WORKDIR /pyshot

# Install dependencies and playwright
RUN poetry install && poetry run playwright install

# Expose ports
EXPOSE 8000

# Start the FastAPI server
CMD ["poetry", "run", "uvicorn", "pyshot.screenshot_router:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]