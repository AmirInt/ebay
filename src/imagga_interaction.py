import requests


class ImageGaInteractor:
    def __init__(self):

        # The api_key and api_secret obtained from ImageGa
        self.api_key = ""
        self.api_secret = ""

    def send_image(self, image_path):
        response = requests.post(
            f"https://api.imagga.com/v2/tags",
            auth=(self.api_key, self.api_secret),
            files={"image": open(image_path, "rb")}
        )
        return response.json()
