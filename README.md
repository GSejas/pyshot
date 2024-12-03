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

## Running the Application

To start the application, use the following command:
```
poetry run uvicorn pyshot:app --reload
```

The service will be available at `http://localhost:8000`.

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

## Using Docker componse:

### Re-build

  ```sh
  docker-compose down
  docker-compose build --no-cache
  docker-compose up

  ```


The service will be available at `http://localhost:8000`.


## screenshot_router.py

 file:

### `POST /take`

**Description:**
Takes a screenshot of the specified URL with the given parameters.

**Parameters:**
- 

url

 (str, required): The website to screenshot.
- 

waitUntil

 (str, optional, default="load"): Wait until event. Options are "load", "domcontentloaded", "networkidle".
- 

blockPopups

 (bool, optional, default=True): Block popups.
- 

blockCookieBanners

 (bool, optional, default=True): Block cookie banners.
- 

viewportDevice

 (str, optional): Viewport device. If specified, overrides viewportWidth and viewportHeight.
- 

viewportWidth

 (int, optional, default=1280): Viewport width in pixels.
- 

viewportHeight

 (int, optional, default=720): Viewport height in pixels.
- 

deviceScaleFactor

 (int, optional, default=1, ge=1, le=5): Device scale factor.
- 

fullPage

 (bool, optional, default=True): Capture full page.

**Returns:**
- `dict`: A dictionary containing the screenshot ID and filename.
  - 

screenshot_id

 (str): The ID of the screenshot.
  - 

filename

 (str): The filename of the screenshot.

**Example Request:**
```json
{
  "url": "https://example.com",
  "waitUntil": "load",
  "blockPopups": true,
  "blockCookieBanners": true,
  "viewportDevice": null,
  "viewportWidth": 1280,
  "viewportHeight": 720,
  "deviceScaleFactor": 1,
  "fullPage": true
}
```

**Example Response:**
```json
{
  "screenshot_id": "unique_screenshot_id",
  "filename": "screenshot_filename.png"
}
```

### `GET /screenshot/{screenshot_id}`

**Description:**
Retrieves the screenshot by ID.

**Parameters:**
- 

screenshot_id

 (str, required): The ID of the screenshot.

**Returns:**
- 

FileResponse

: The screenshot file.

**Example Request:**
```
GET /screenshot/unique_screenshot_id
```

**Example Response:**
- Returns the screenshot file with `image/png` media type.

### `GET /screenshots`

**Description:**
Lists all screenshots.

**Returns:**
- `list`: A list of screenshot metadata.
  - 

id

 (str): The ID of the screenshot.
  - 

filename

 (str): The filename of the screenshot.
  - 

timestamp

 (datetime): The timestamp when the screenshot was taken.

**Example Request:**
```
GET /screenshots
```

**Example Response:**
```json
{
  "screenshots": [
    {
      "id": "unique_screenshot_id_1",
      "filename": "screenshot_filename_1.png",
      "timestamp": "2023-10-01T12:34:56Z"
    },
    {
      "id": "unique_screenshot_id_2",
      "filename": "screenshot_filename_2.png",
      "timestamp": "2023-10-02T12:34:56Z"
    }
  ]
}
````