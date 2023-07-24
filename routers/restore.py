from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
import cv2
from gfpgan import GFPGANer as model
from pathlib import Path
import uuid
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context
router = APIRouter()

class Restorer:
    """Restore images"""
    def __init__(self, image) -> None:
        print("RESTORER INIT")
        self.img = image
        # Extract the file extension
        _, imageExtension = self.img.filename.split(".")
        #save original and restored image
        # with randomly generated name
        #and the original file extension
        origImgPath = "images/original/" + str(uuid.uuid4()) + "." + imageExtension
        resImgPath = "images/restored/" + str(uuid.uuid4()) + "." + imageExtension
        self.origImgPath = Path(origImgPath)
        self.restImgPath = Path(resImgPath)

    async def main(self):
        #save image
        await self.saveImage()
        #restore image
        await self.restoreImage()
        print("restored")
        return self.restImgPath

    async def saveImage(self):
        """Save file temporarily on the server"""
        imageData = await self.img.read()
        with open(self.origImgPath ,"wb") as f:
            f.write(imageData)
        print("image saved")
        return self.origImgPath

    async def restoreImage(self):
        #read image file
        img = cv2.imread(str(self.origImgPath))
        print("image READ")
        # restore image
        croppedFaces, restoredFaces, restoredImg = model(".venv/lib/python3.11/site-packages/gfpgan/weights/GFPGANv1.3.pth").enhance(img)
        print("result AVAILABLE")
        #save the restored image temporarily
        cv2.imwrite(str(self.restImgPath), restoredImg)
        print("RESTORED IMAGE SAVED")
        return self.restImgPath

@router.post("/restore/upload-image")
async def getFile(image: UploadFile = File(...)):
    #get image from client
    print("request received")
    #initialize Restorer
    restorer = Restorer(image)
    #restore image
    outputPath = await restorer.main()
    return FileResponse(outputPath, headers={"Content-Disposition": "attachment; filename=result.png"})

@router.get("/restore/webhook")
def webhook():
    #signal client when the file is ready for download
    return "The image is ready for download"

@router.get("/restore/restored-image")
def restoredImage():
    #send the restored image
    return "here is the restored image"
