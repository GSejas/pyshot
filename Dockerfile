FROM python:3.11.2-buster   


ENV DEBIAN_FRONTEND='noninteractive'

# Install Poetry
RUN apt-get update && apt install -y curl
RUN curl -sSL https://install.python-poetry.org | python

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.in-project true

# WORKDIR /pyshot


# # Copy only the necessary files for installing dependencies
# COPY pyproject.toml poetry.lock* /pyshot


# # Install dependencies
# RUN pipx install poetry
# # Install dependencies
# RUN poetry install

# RUN poetry run playwright install
COPY . .
RUN poetry install && poetry run playwright install
EXPOSE 8000