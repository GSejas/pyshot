# Pyshot

A FastAPI project for taking screenshots of websites using Playwright.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/pyshot.git
    cd pyshot
    ```

2. Build the Docker container:
    ```sh
    docker-compose up --build
    ```

3. Install dependencies:
    ```sh
    poetry install
    ```

## Running the Service

1. Start the FastAPI server:
    ```sh
    poetry run uvicorn pyshot.screenshot_router:app --reload
    ```

2. The service will be available at `http://localhost:8000`.

## Endpoints

- `POST /take`: Takes a screenshot of the specified URL.
- `GET /screenshot/{screenshot_id}`: Retrieves the screenshot by ID.

## Example

To take a screenshot, send a POST request to `/take` with the URL and other parameters. Then, retrieve the screenshot using the ID returned in the response.

```sh
curl -X POST "http://localhost:8000/take?url=https://example.com"
```

```sh
curl -O "http://localhost:8000/screenshot/{screenshot_id}"
```

## Additional Entry Points

You can also run the service using Docker:

1. Build the Docker image:
    ```sh
    docker build -t pyshot .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8000:8000 pyshot
    ```

The service will be available at `http://localhost:8000`.