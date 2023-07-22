from fastapi import APIRouter

router = APIRouter()

def saveFile():
    #save image to database
    return "save image to db"

def restoreImage():
    #restore image
    return "image restored"

@router.post("/restore/upload-image")
def getFile():
    #get image from client
    #save file to db
    return "get image from client"

@router.get("/restore/webhook")
def webhook():
    #signal client when the file is ready for download
    return "The image is ready for download"

@router.get("/restore/restored-image")
def restoredImage():
    #send the restored image
    return "here is the restored image"
