# FastAPI Course Project

Welcome to my **FastAPI Course Project**! This repository contains all the exercises, examples, and projects that I am working on while learning FastAPI through the course on Platzi.

## Table of Contents
- [FastAPI Course Project](#fastapi-course-project)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
  - [Technologies Used](#technologies-used)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Author](#author)

## About the Project

This project is a collection of code examples, projects, and exercises from the FastAPI course on Platzi. The goal is to learn the key features of FastAPI, including:
- Creating APIs quickly and efficiently.
- Using Pydantic for data validation.
- Exploring async capabilities for concurrent requests.

In this course, we will be building an API that allows us to create billing accounts for our clients.

Feel free to explore the repository and learn alongside me!

## Technologies Used
- **FastAPI**: A modern and fast web framework for building APIs with Python 3.7+
- **Python 3.12**: Programming language used for all project exercises.
- **Uvicorn**: ASGI server used for running the FastAPI app.

## Getting Started

To get started with this project, follow the instructions below to set up your environment.

### Prerequisites
- **Python 3.7+**: Make sure you have Python installed. You can verify the version with:
  ```bash
  python --version
  ```
- **Git**: Version control to clone the repository and track changes.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tuusuario/fastapi-course.git
   cd fastapi-course
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI project locally, use the following command:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can also access the auto-generated documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Contributing

Contributions are welcome! If you want to improve something or fix an issue, feel free to open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Víctor Noé Becerra Hernández**
