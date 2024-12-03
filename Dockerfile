FROM python:3.10-slim   


ENV DEBIAN_FRONTEND='noninteractive'

# Install Poetry
RUN apt-get update && apt install -y curl
RUN curl -sSL https://install.python-poetry.org | python

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.in-project true && mkdir -p /screenshots

RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list.d/bullseye.list \
    && apt-get update

# Install Node.js (required for Playwright)
RUN curl -sL https://deb.nodesource.com/setup_21.x | bash - && \
    apt-get install -y nodejs

# Install Playwright globally
RUN npm install -g playwright

# Install system dependencies
RUN playwright install-deps
# RUN poetry run playwright install

# Copy the application code
COPY . /pyshot

# Set the working directory
WORKDIR /pyshot


# Install dependencies and playwright
RUN poetry install && poetry run playwright install && playwright install-deps
RUN poetry add uvicorn
EXPOSE 8000