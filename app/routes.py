from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import face_recognition
import numpy as np
import pickle
from PIL import Image, ImageDraw
import io
import os
import uuid

router = APIRouter()

# Load the trained model
with open('models/trained_model.pkl', 'rb') as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Directory to save recognized images (for dev purpose)
SAVE_DIR = "recognized_images_dev"
os.makedirs(SAVE_DIR, exist_ok=True)

@router.post("/predict/")
async def predict_faces(file: UploadFile = File(...)):
    # Check the file size to ensure it isn't too large
    if file.size > 50 * 1024 * 1024:  # 50 MB size limit
        raise HTTPException(status_code=413, detail="File too large. Max size is 50MB.")
    
    # Read the image data
    image_data = await file.read()

    # Check the file type
    if not file.content_type in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=400, detail="Unsupported image type. Please upload a JPEG or PNG image.")
    
    try:
        # Load the image
        image = Image.open(io.BytesIO(image_data))

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

        # Create a drawing object for the image (for saving purposes)
        draw = ImageDraw.Draw(image)

        for i, face_encoding in enumerate(face_encodings):
            # Compare the face with known encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            # Use the closest known face match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            recognized_names.append(name)

            # Draw a rectangle around the face (for dev purpose)
            top, right, bottom, left = face_locations[i]
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=2)

            # Annotate the face with the name (for dev purpose)
            draw.text((left + 6, bottom + 10), name, fill=(255, 255, 255, 255))

        # For dev purposes, save the annotated image to the local folder
        image_filename = f"{uuid.uuid4()}.jpg"
        image.save(os.path.join(SAVE_DIR, image_filename))
        recognized_names_without_unknown = [name for name in recognized_names if name !="Unknown"]

        # Returning only the recognized names (response remains unchanged)
        return JSONResponse(content={"recognized_faces": recognized_names_without_unknown})

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f'An error occurred while processing the image.\n Error: {e}')

@router.get("/")
async def root():
    return {"message": "API is running!"}
