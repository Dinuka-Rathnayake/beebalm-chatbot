from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from openai import AzureOpenAI
import os


app = Flask(__name__)
# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

endpoint = "https://it212-me1y3ikc-eastus2.cognitiveservices.azure.com/"
model_name = "gpt-35-turbo"
deployment = "gpt-35-turbo"



client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://it212-me1y3ikc-eastus2.cognitiveservices.azure.com/",
    api_key=OPENAI_API_KEY,
)

while True:
    
    # get user input
    print("Ask a question about Beebalm Banquet Hall (type 'bye' to exit):")
    question = input("user: ")
    if question.lower() == "bye":
        print("Exiting the chatbot. Goodbye!")
        break
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": question,
            }
        ],
        max_tokens=50,
        temperature=0.3,
        n=1,
        top_p=1.0,
        model=deployment
    )

    for choice in response.choices:
        print(f"AI: {choice.message.content}")



@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_question = data.get('question', '')
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": user_question}],
        max_tokens=50,
        temperature=0.3,
        n=1,
        top_p=1.0,
        model=deployment
    )
    answer = response.choices[0].message.content
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)