from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
import uuid
from flask_cors import CORS


# crew ai imports
from crewai import Agent, Crew, LLM, Task
from crewai_tools import PDFSearchTool

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
    azure_endpoint= endpoint,
    api_key=OPENAI_API_KEY
)

# crew ai setup
llm = LLM(
    model=model_name,
    api_key=OPENAI_API_KEY,
    api_base=endpoint,
    deployment_id=deployment
    
)

# import ragtool
#pdf_rag_tool = PDFSearchTool(pdf = "beebalmlk.pdf")

# # research agent
# researcher = Agent(
#     role="Research Agent",
#     goal="extract relevant information from the provided PDF document.",
#     backstory="you are skilled at finding key insights quickly and accurately from a PDF document.",
#     tools=[pdf_rag_tool],
# )

# # writer agent
# writer = Agent(
#     role="Content generation Assistant",
#     goal="create clear, engaging well structured written related to   query: {query}.",
#     backstory="You are passionate about tuning ideas and facts into compelling easy to read.",
#     llm=llm,
# )

# research task
# research_task = Task(
#     name="Researching Information",
#     description="Extract relevant information from the provided PDF document.",
#     expected_output="A summary of the key points related to the query.",
#     agent=researcher,
# )

# # writing task
# writing_task = Task(
#     name="Writing Content",
#     description="Generate clear, engaging content based on the research findings.",
#     expected_output="A polished, three section report in markdown format with an .",
#     agent=writer,
#     output_file="report.md",
# )

qa_agent = Agent(
    role="Question Answering Agent",
    goal="Provide accurate consistent answers to question : {query}",
    backstory="You serve as a relible guide to help users navigage infomation overload and find the answers they need.",
    description="An agent that answers questions about Beebalm Banquet Hall.",
    llm=llm,
    tools=[],
)

qa_task = Task(
    name="Answering Questions",
    description="Answer questions about Beebalm Banquet Hall.",
    expected_output="A clear and concise answer to the user's question with support from the provided PDF document.",
    agent=qa_agent
)

# crew
crew = Crew(
    agents=[qa_agent],
    tasks=[qa_task],
    verbose=True,
)

result = crew.kickoff(inputs={
    "query": "where is beebalm banquet hall?",
    
})
print("Crew result:", result)

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



# @app.route('/api/messages', methods=['POST'])
# def messages():
#     activity = request.json
#     # Only respond to message activities
#     if activity.get("type") == "message":
#         user_text = activity.get("text", "")
#         # Call OpenAI
#         print("User text:", user_text)
#         try:
#             response = client.chat.completions.create(
#                 messages=[{"role": "system", "content": user_text}],
#                 max_tokens=50,
#                 temperature=0.3,
#                 n=1,
#                 top_p=1.0,
#                 model=deployment
#             )
#             answer = response.choices[0].message.content
#             print("AI response:", answer)
#         except Exception as e:
#             print("Error calling OpenAI:", e)
#             answer = "Sorry, I couldn't process your request at the moment."
#         # Build a Bot Framework-compatible reply
#         reply = {
#             "type": "message",
#             "text": answer,
#             "from": activity.get("recipient", {"id": "bot"}),
#             "recipient": activity.get("from", {"id": "user"}),
#             "replyToId": activity.get("id"),
#             "conversation": activity.get("conversation"),
#             "id": str(uuid.uuid4())
#         }
#         print("Replying with:", reply)
#         return jsonify(reply)
#     # Respond to other activity types with 200 OK and no body
#     print("Received non-message activity")
#     return '', 200


@app.route('/')
def home():
    return "Welcome to the Beebalm Banquet Hall Chatbot!"

#for local testing
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)