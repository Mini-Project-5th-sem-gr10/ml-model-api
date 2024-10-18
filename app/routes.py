from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import face_recognition
import numpy as np
import pickle
from PIL import Image
import io
import os

router = APIRouter()

# Load the trained model
with open('models/trained_model.pkl', 'rb') as f:
    known_face_encodings, known_face_names = pickle.load(f)

@router.post("/predict/")
async def predict_faces(file: UploadFile = File(...)):
    # Check the file size to ensure it isn't too large
    if file.size > 5 * 1024 * 1024:  # 5 MB size limit
        raise HTTPException(status_code=413, detail="File too large. Max size is 5MB.")
    
    # Read the image data
    image_data = await file.read()

    # Check the file type
    if not file.content_type in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=400, detail="Unsupported image type. Please upload a JPEG or PNG image.")
    
    try:
        # Load the image
        image = Image.open(io.BytesIO(image_data))

        # Print image properties for debugging
        print(f"Uploaded image format: {image.format}")
        print(f"Uploaded image mode: {image.mode}")
        print(f"Uploaded image size: {image.size}")

        # Ensure the image is in RGB mode
        if image.mode not in ['RGB', 'L']:  # Check for RGB or grayscale
            raise HTTPException(status_code=400, detail="Image must be in RGB or grayscale format.")

        if image.mode != 'RGB':
            image = image.convert('RGB')

        test_image = np.array(image)

        # Find all face locations and encodings in the image
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        # List to store recognized face names
        recognized_names = []

        for face_encoding in face_encodings:
            # Compare the face with known encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            # Use the closest known face match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            recognized_names.append(name)

        return JSONResponse(content={"recognized_faces": recognized_names})

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f'An error occurred while processing the image.\n Error: {e}')

@router.get("/predict-local-image/")
async def predict_local_image():
    # Define the path to the uploads folder and the specific image
    uploads_folder = "uploads"  # Change this path if necessary
    image_name = "me.jpeg"  # Name of the image file
    image_path = os.path.join(uploads_folder, image_name)

    # Print the current working directory and the image path for debugging
    print(f"Current working directory: {os.getcwd()}")
    print(f"Image path: {image_path}")

    # Check if the file exists
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found.")

    try:
        # Load the image
        image = Image.open(image_path)

        # Print image properties for debugging
        print(f"Uploaded image format: {image.format}")
        print(f"Uploaded image mode: {image.mode}")
        print(f"Uploaded image size: {image.size}")

        # Ensure the image is in RGB mode and convert if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert the image to a NumPy array
        test_image = np.array(image)

        # Ensure the array is of type uint8
        if test_image.dtype != np.uint8:
            test_image = test_image.astype(np.uint8)

        # Check the minimum and maximum pixel values in the image
        print(f"Image data min: {test_image.min()}, max: {test_image.max()}")

        # Find all face locations and encodings in the image
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        # List to store recognized face names
        recognized_names = []

        for face_encoding in face_encodings:
            # Compare the face with known encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            # Use the closest known face match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            recognized_names.append(name)

        return JSONResponse(content={"recognized_faces": recognized_names})

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f'An error occurred while processing the image.\n Error: {e}')


@router.get("/")
async def root():
    return {"message": "API is running!"}