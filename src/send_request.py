import requests


def main():
    # Address to your image
    filename = "files/sample.jpg"
    files = {"file": (filename, open(filename, "rb"))}
    # Put your email and image description here
    data_json = {
        "description": "This is the picture of my car",
        "email": "example@email.com"
    }

    response = requests.post(
        "http://127.0.0.1:8000/post",
        files=files,
        data=data_json
    )

    print(response.text)

if __name__ == "__main__":
    main()