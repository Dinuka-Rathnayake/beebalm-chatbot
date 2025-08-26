from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

from langchain_openai import AzureChatOpenAI

app = Flask(__name__)
# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

endpoint = "https://it212-me1y3ikc-eastus2.cognitiveservices.azure.com/"
model_name = "gpt-35-turbo"
deployment = "gpt-35-turbo"

import getpass
import os

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure: ")

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    openai_api_version= "2024-12-01-preview",
)
try:
    response = model.invoke("Hello, world!")
    print("Connection successful! Model response:", response)
except Exception as e:
    print("Connection failed:", e)


@app.route('/')
def home():
    return "Welcome to the Beebalm Banquet Hall Chatbot!"

#for local testing
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)