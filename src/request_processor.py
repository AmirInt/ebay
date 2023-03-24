import requests

from rabbitmq_interaction import RabbitMqListener
from s3_interaction import S3Interactor
from imagga_interaction import ImageGaInteractor
from database_interaction import DatabaseInteractor

# s3_interactor connects to the object storage cloud
s3_interactor = S3Interactor()

# imagga_interactor is responsible for labeling images using the Imagga API
imagga_interactor = ImageGaInteractor()

# database_interactor connects to the Database cloud
database_interactor = DatabaseInteractor(drop_table=False)


def send_email(email: str, state: str) -> requests.Response:
    """Uses the Mailgun API to send confirmation/rejection emails to users.
    
    Args:
        email (str): The receipient's email address
        state (str): The state of the user's post
    
    Returns:
        requests.Response: The response of the HTTP request to the Mailgun API
    """
    
    response = requests.post(
        # Put your mailgun api address here:
        "",
        # Put your mailgun secret key and email address respectively in 'api' and 'from' fields
        auth=("api", ""),
        data={"from": "",
            "to": email,
            "subject": "Post Confirmation",
            "text": f"Your post was {state}"}
    )
    return response


def reveiw_message_tags(labels: dict) -> str:
    """Checks the incoming labels for the tag "vehicle" with a confidence higher than 50%.

    Args:
        labels (dict): The given tags 
    """


    state = "rejected"
    for x in labels["result"]["tags"]:
        if x["tag"]["en"] == "vehicle":
            if x["confidence"] > 50.0:
                state = "accepted"
            break
    return state
    

def message_arrival_callback(ch, method, properties, body: bytes) -> None:
    """The callback used when the RabbitMQ signals and returns a message enqueuing.

    Args:
        ch (): What?
        method (): Where?
        properties (): Eh?
        body (bytes): The enqueued message. 
    """

    print("RabbitMQ sent something")
    
    # Converting the body to an integer
    id = int(body.decode())

    # Downloading the corresponding image from S3
    s3_interactor.download_file(f"downloads/{id}.jpg", f"{id}.jpg")

    # Tagging the image
    labels = imagga_interactor.send_image(f"downloads/{id}.jpg")
    main_tag = labels["result"]["tags"][0]
    print(f"Main Tage: {main_tag}")
    
    # Deciding whether the image shoudl be rejected or accepted
    state = reveiw_message_tags(labels)

    # Updating the database
    database_interactor.update_record(id, state, main_tag["tag"]["en"])
    record = database_interactor.get_record(id)

    # Sending an email to the user
    if record is not None:
        if send_email(record["email"], record["state"]).status_code == 200:
            print("Email sent")
    else:
        print("There was an issue sending the email")


def main():
    RabbitMqListener(message_arrival_callback)

if __name__ == "__main__":
    main()