import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name="ap-south-1")  
table = dynamodb.Table('Users')
@app.get("/")
def read_root():
    return {"message": "FastAPI with DynamoDB on AWS Lambda"}
@app.get("/users/{name}")
def get_user(name: str):
    response = table.get_item(Key={'name': name})
   
    if 'Item' in response:
        user_data = response['Item']
        age = user_data.get("age", "Not provided")  
        company = user_data.get("company", "Not provided")
        project = user_data.get("project", "Not provided")
        return {
            "message": f"hello {name}, you are {age} years old.",
            "company": company,
            "project": project
        }
   
    return {"message": "User not found"}

# Change the handler name to match your SAM template
lambda_handler = Mangum(app)