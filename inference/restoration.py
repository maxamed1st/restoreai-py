import cv2
from gfpgan import GFPGANer as model
from pathlib import Path
import uuid

class Restore:
    """Restore images"""
    def __init__(self, image, upscale) -> None:
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

        #set enhancement factor
        self.upscale = upscale
        print("upscale", self.upscale)

    async def restoration(self):
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
        croppedFaces, restoredFaces, restoredImg = model(
            ".venv/lib/python3.11/site-packages/gfpgan/weights/GFPGANv1.3.pth", 
            self.upscale
            ).enhance(img)
        print("result AVAILABLE")
        #save the restored image temporarily
        cv2.imwrite(str(self.restImgPath), restoredImg)
        print("RESTORED IMAGE SAVED")
        return self.restImgPath

if __name__ == "__main__":
    Restore()
