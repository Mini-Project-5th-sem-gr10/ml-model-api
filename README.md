# ML Model API

### Description

This API powers the face recognition component for the Automatic Attendance Marking System. It processes uploaded images, detects faces, and identifies known individuals based on pre-encoded face data, providing recognized face names in the response.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Mini-Project-5th-sem-gr10/ml-model-api.git
   cd ml-model-api
   ```

2. **Prerequisites**:
   Ensure the following dependencies are installed:

   - Python
   - pip
   - cmake
   - dlib
   - uvicorn

3. **Install Required Python Packages**:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` includes:

   ```
   anyio==4.6.2.post1
   click==8.1.7
   colorama==0.4.6
   dlib==19.24.6
   face-recognition-models==0.3.0
   face_recognition==1.3.0
   fastapi==0.115.2
   h11==0.14.0
   idna==3.10
   numpy==2.1.2
   Pillow==11.0.0
   pydantic==2.9.2
   pydantic-core==2.23.4
   sniffio==1.3.1
   starlette==0.40.0
   typing-extensions==4.12.2
   uvicorn==0.32.0
   ```

4. **Run the API**:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. **Docker (Alternative Setup)**:
   - **Build the Docker Image**:
     ```bash
     docker build -t ml-model-api .
     ```
   - **Run the Docker Container**:
     ```bash
     docker run -p 8000:8000 ml-model-api
     ```

### Usage

#### Endpoint

- **`POST /predict/`**
  - **Description**: Accepts an image file (JPEG or PNG) and returns recognized face names.
  - **Request**:
    - Upload an image file as `file` in a multipart form data request.
  - **Response**:
    - JSON object with a list of recognized names, e.g., `{"recognized_faces": ["Name1", "Name2"]}`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License

This project is licensed under the Apache License. See the LICENSE file for details.

---
