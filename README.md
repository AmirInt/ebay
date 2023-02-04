# ebay

## The project attempts to recreate an ebay-like service where users submit their posts along with descriptions to the service.

# Project Modules:

All modules are cloud-based and are used by means of addressing the cloud service API.

1. Backend; FastAPI
2. Database Service; MySQL
3. Image Tagging Service
4. RabbitMQ Service
5. Object Storage Service; S3

# Services:

The following cloud-services are used to provide different functionalities:

2. Database Service: https://aiven.io/
3. Image Tagging Service: https://imagga.com/
4. RabbitMQ Service: https://www.cloudamqp.com/
5. Object Storage Service: https://www.arvancloud.ir/en (can alternatively use Amazon S3 service)

# Process

After a post is submitted to the API, the image is stored in the S3 service and the description along with its corresponding image ID is stored in the database. The post ID is enqueued into the RabbitMQ cloud-service for further process. On the other side. A different process listens on the RabbitMQ and receives the recently submitted image IDs. This service then uses the image tagging service to match the image with the description. The result of this matching is emailed to the submitting user.

![Image contains the architecture of the project]( "Architecture of the project")

# Usage

Obtain the services required and connect scripts to their cloud requirements.
Create a directory name 'downloads' inside 'src'.
Use 'send_request.py' to send your images.
Use 'check_status.py' when you haven't yet received any emails to check the confirmation status of your post.
