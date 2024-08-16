# File Management Microservice

[![codecov](https://codecov.io/github/hanieas/File-Management-Microservice/graph/badge.svg?token=OGUBX46W31)](https://codecov.io/github/hanieas/File-Management-Microservice)

## Table of Contents
1. [Introduction](#Introduction)
2. [Technology Stack and Features]()
3. [Why?](#Why?)
4. [How?](#How?)
4. [Configurations]()
5. [API Endpoints]()
6. [Contributing](#Contributing)

## Introduction

This microservice is crafted to handle all file-related operations within our ecosystem efficiently. Leveraging MinIO for robust object storage and MySQL for managing file metadata, this service ensures high performance and reliability. 

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- 🧰 [SQLAlchemy](https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- 🗄️ [MYSQL](https://www.mysql.com/) as the SQL database.
- 🔄 [Alembic](https://alembic.sqlalchemy.org/en/latest) for database migrations.
- 🔧 [Celery](https://docs.celeryq.dev/en/stable/) with [RabbitMQ](https://www.rabbitmq.com/) for task queue management and background processing.
- 💾 [MinIO](https://min.io/) for scalable object storage with chunk upload support.
- ✅ [Pytest](https://pytest.org) for testing to ensure code reliability and functionality.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
  
## Why?

1. Consolidates all file-related operations into one service, simplifying management and maintenance.
2. Allows independent scaling of file handling capabilities without affecting other services.
3. Facilitates easier updates and modifications related to file handling without disrupting other functionalities.
4. Minimizes code duplication by centralizing file upload and retrieval logic, leading to cleaner and more maintainable code.

## How?

1. **Complete the `.env` File**: 
    - Copy the contents of `.env.example` to a new file named `.env`.
    - Fill in the required environment variables based on your setup.

2. **Build the Docker Image**:
    - Run the following command to build the Docker image:
        ```bash
        docker compose build
        ```

3. **Run the Containers**:
    - After the build is complete, start the containers in detached mode with:
        ```bash
        docker compose up -d
        ```

4. **Migrate the Database**:
    - Access the running container to perform the database migration:
        ```bash
        docker compose exec filemanager bash
        ```
    - Inside the container, run the migration using Alembic:
        ```bash
        alembic upgrade head
        ```

5. **Access the Service**:
    - The project is now up and running, accessible on port `8000`.
    - You can access the project documentation by navigating to `/docs` on your browser.


## Contributing

We welcome contributions from everyone! If you have ideas for improvements, new features, or bug fixes, feel free to contribute to this project. Here's how you can get involved:

1. **Create an Issue**: 
    - If you find a bug, have a question, or want to suggest a feature, please open an issue. This helps us track and discuss your ideas.

2. **Send a Pull Request (PR)**:
    - Fork the repository, make your changes in a new branch, and then create a pull request. 
    - Please make sure your code follows the project's coding standards and passes all tests.

We appreciate your contributions and will do our best to review and merge your pull requests promptly. Thank you for helping us improve this project!
