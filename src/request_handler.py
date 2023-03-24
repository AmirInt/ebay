from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi import status

from database_interaction import DatabaseInteractor
from rabbitmq_interaction import enqueue_to_rabbitmq
from s3_interaction import S3Interactor


# A global variable to handle the unique post id's
id = 0

# database_interactor connects to the Database cloud
database_interactor = DatabaseInteractor(drop_table=True)

# s3_interactor connects to the object storage cloud
s3_interactor = S3Interactor()

async def read_file(file: UploadFile):
    """Assigns a new id to the given file and reads the content of the UploadFile object given.
    
    Args:
        file (UploadFile)
    
    Returns:
        (str, bytes): Tuple of the filename and file content
    """

    global id
    file.filename = f"{id}.jpg"
    contents = await file.read()
    return (file.filename, contents)


# uvicorn and fastapi look for this variable
app = FastAPI()


@app.get("/status/{post_id}")
async def check_post_status(post_id: int):
    """The get method API.
    
    Args:
        post_id (int): The id of the posted material
    
    Returns:
        fastapi.responses.FileResponse or str: The response of the HTTP request
        (either the image with the post mateiral in case of confirmation or a 
        simple text in case of rejection)
    """

    record = database_interactor.get_record(post_id)
    if record is None:
        return "Wrong id"
    if record["state"] == "accepted":
        s3_interactor.download_file(f"downloads/{post_id}.jpg", f"{post_id}.jpg")
        response = FileResponse(
            path=f"downloads/{post_id}.jpg",
            status_code=status.HTTP_200_OK,
            filename=f"{post_id}.jpg",
            headers={
                "ID": f"{record['id']}",
                "Description": f"{record['description']}",
                "Category": f"{record['category']}"
            })
        return response
        
    return f"Your post is {record['state']}"


@app.post("/post/")
async def post_submission(
    file: UploadFile = File(...),
    description: str = Form(...),
    email: str = Form(regex= r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")):
    """The post method API.
    
    Args:
        file (fastapi.UploadFile): The posted image
        description (str): The description of the post
        email (str): The user's email address
    
    Returns:
        str: The response of the HTTP request stating that the post with the
        specified id was submitted
    """

    global id

    filename, contents = await read_file(file)
    await database_interactor.deposit_to_database(id, description, email)
    s3_interactor.upload_file(contents, filename)
    enqueue_to_rabbitmq(id)

    response = f"Your post was submitted with the id '{id}'"
    id += 1

    return response
