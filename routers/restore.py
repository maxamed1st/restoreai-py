from fastapi import APIRouter, UploadFile, File, Form
import uuid
from PubSub import EventHub
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context
router = APIRouter()
def emit_event(message, payload):
    EventHub().notify(message, payload)

async def save_image(image: File(...)):
    """Save image on the server"""

    image_data = await image.read()
    _, imageExtension = image.filename.split(".")
    image_path = "images/original/" + str(uuid.uuid4()) + "." + imageExtension

    with open(image_path ,"wb") as f:
        f.write(image_data)
    print("image saved")
    return image_path

@router.post("/restore/upload-image")
async def upload_image(image: UploadFile = File(...), upscale: int = Form(...)):
    '''get image from client'''
    print("request received")

    #save image
    image_path = await save_image(image)
    #notify subscribers about image location
    message = "image has been uploaded"
    emit_event(message, {"image_path": image_path, "upscale": upscale})

    return message

@router.get("/restore/restored-image")
def restoredImage():
    #send the restored image
    return "here is the restored image"
