from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
import uuid

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

# while True:
    
#     # get user input
#     print("Ask a question about Beebalm Banquet Hall (type 'bye' to exit):")
#     question = input("user: ")
#     if question.lower() == "bye":
#         print("Exiting the chatbot. Goodbye!")
#         break
    
#     response = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": question,
#             }
#         ],
#         max_tokens=50,
#         temperature=0.3,
#         n=1,
#         top_p=1.0,
#         model=deployment
#     )

#     for choice in response.choices:
#         print(f"AI: {choice.message.content}")



@app.route('/api/messages', methods=['POST'])
def messages():
    activity = request.json
    # Only respond to message activities
    if activity.get("type") == "message":
        user_text = activity.get("text", "")
        # Call OpenAI
        print("User text:", user_text)
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": user_text}],
                max_tokens=50,
                temperature=0.3,
                n=1,
                top_p=1.0,
                model=deployment
            )
            answer = response.choices[0].message.content
            print("AI response:", answer)
        except Exception as e:
            print("Error calling OpenAI:", e)
            answer = "Sorry, I couldn't process your request at the moment."
        # Build a Bot Framework-compatible reply
        reply = {
            "type": "message",
            "text": answer,
            "from": activity.get("recipient", {"id": "bot"}),
            "recipient": activity.get("from", {"id": "user"}),
            "replyToId": activity.get("id"),
            "conversation": activity.get("conversation"),
            "id": str(uuid.uuid4())
        }
        print("Replying with:", reply)
        return jsonify(reply)
    # Respond to other activity types with 200 OK and no body
    print("Received non-message activity")
    return '', 200


@app.route('/')
def home():
    return "Welcome to the Beebalm Banquet Hall Chatbot!"

#for local testing
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)