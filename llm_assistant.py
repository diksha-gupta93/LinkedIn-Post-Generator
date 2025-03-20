import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from the .env file
load_dotenv()

# Initialize the ChatGroq model using the API key from environment variables
llm = ChatGroq(groq_api_key=os.getenv("Groq_key"), model_name="llama-3.2-90b-vision-preview")

if __name__ == "__main__":
    # Query the model with a sample question
    response = llm.invoke("What are the two main ingredients of Samosa?")
    print(response.content)
