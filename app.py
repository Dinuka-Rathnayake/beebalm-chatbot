from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
import uuid
from flask_cors import CORS
# Disable ChromaDB before importing CrewAI
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"

# crew ai imports
from crewai import Agent, Crew, LLM, Task
from crewai_tools import WebsiteSearchTool
from crewai_tools import PDFSearchTool
from crewai_tools import ScrapeWebsiteTool

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables from .env file
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

endpoint = "https://it212-me1y3ikc-eastus2.cognitiveservices.azure.com/"
model_name = "gpt-35-turbo"
deployment = "gpt-35-turbo"



client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://it212-me1y3ikc-eastus2.cognitiveservices.azure.com/",
    api_key=OPENAI_API_KEY,
)

# crew ai setup
llm = LLM(
    model=model_name,
    api_key=OPENAI_API_KEY,
    api_base=endpoint,
    deployment_id=deployment
)

# Use ScrapeWebsiteTool instead (simpler, no embedding required)
scrape_tool = ScrapeWebsiteTool(website_url="https://www.beebalm.lk/")

# research agent
researcher = Agent(
    role="Research Agent",
    goal="Provide accurate consistent answers to question by reading website : {query}.",
    backstory="you are skilled at finding key insights quickly and accurately from a website.",
    tools=[scrape_tool],
    verbose=False,
    llm=llm    
)

# research task
research_task = Task(
    description=""""Answer questions about Beebalm Banquet Hall.
    
    Query: {query}
    
    Provide as much details as possible, even if partial.""",
    expected_output="A clear and concise answer to the user's question with support from the provided website.",
    agent=researcher,
)

# crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=False,
    memory=False,  # Disable memory for this crew
)
#for testing locally
# result = crew.kickoff(inputs={
#     "query": "where is beebalm banquet hall?",
    
# })
# print("Crew result:", result)

@app.route('/api/messages', methods=['POST'])
def messages():
    activity = request.json
    # Only respond to message activities
    if activity.get("type") == "message":
        user_text = activity.get("text", "")
        # Call OpenAI
        print("User text:", user_text)
        try:

            result = crew.kickoff(inputs={
                "query": user_text,
                
            })
            print("Crew result:", result)
            answer = str(result)
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