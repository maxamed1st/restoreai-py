import cv2
from gfpgan import GFPGANer as model
from PubSub import EventHub

class Restore:
    """Restore images"""

    def __init__(self) -> None:
        print("RESTORER INIT")
        #subscribe to "image has been uploaded" event
        message = "image has been uploaded"
        EventHub().subscribe(self.main, message)

    @classmethod
    def _emit_event(message, payload):
        EventHub().notify(message, payload)

    def main(self, payload) -> None:
        #read image file
        image = cv2.imread(payload["image_path"])
        #restore image
        cropped_faces, restored_faces, restored_image = model(
            "gfpgan/weights/GFPGANv1.3.pth", 
            payload["upscale"]
            ).enhance(image)
        #save the restored image on the server
        cv2.imwrite(str(self.restored_image_path), restored_image)
        #notify subscribers about image location
        message = "image is restored"
        self.emit_event(message, {"path": self.restored_image_path})


if __name__ == "__main__":
    Restore()
