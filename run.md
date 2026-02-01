To build and run this project, follow these steps:

1.  **Navigate to the project directory:**
    ```bash
    cd /home/asepsaputra/Documents/Developments/Python/yhfinance-fastapi
    ```

2.  **Build the Docker image:**
    This command will build the Docker image based on the `Dockerfile` in the current directory. The `-t yhfinance-api` flag tags the image with the name `yhfinance-api`.
    ```bash
    docker build -t yhfinance-api .
    ```

3.  **Run the Docker container:**
    This command will run a Docker container from the `yhfinance-api` image. The `-p 8000:8000` flag maps port 8000 on your host machine to port 8000 inside the container. The `-d` flag runs the container in detached mode (in the background).
    ```bash
    docker run -d -p 8000:8000 yhfinance-api
    ```

After these steps, the FastAPI application should be running and accessible on `http://localhost:8000`.