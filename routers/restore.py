from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from inference import Restore
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context
router = APIRouter()

@router.post("/restore/upload-image")
async def getFile(image: UploadFile = File(...), upscale: int = Form(...)):
    #get image from client
    print("request received")
    #initialize Restorer
    restore = Restore(image, upscale)
    #restore image
    outputPath = await restore.restoration()
    return FileResponse(outputPath, headers={"Content-Disposition": "attachment; filename=result.png"})

@router.get("/restore/webhook")
def webhook():
    #signal client when the file is ready for download
    return "The image is ready for download"

@router.get("/restore/restored-image")
def restoredImage():
    #send the restored image
    return "here is the restored image"
