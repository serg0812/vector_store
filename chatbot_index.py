
import pickle
import os
#needed for Claude's code
#import requests

from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
#from langchain.chains import VectorDBQAWithSourcesChain
from langchain.chains import RetrievalQAWithSourcesChain
import openai

# Load the vectore store from disk.
with open("faiss_store.pkl", "rb") as f:
    vector_store = pickle.load(f)
openai.api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
#llm=ChatOpenAI(temperature=0.1, max_tokens=1500, model_name='gpt-4')
llm=ChatOpenAI(temperature=0, max_tokens=1500, model_name='gpt-3.5-turbo')
#llm=OpenAI(temperature=0, max_tokens=1500, model_name='text-davinci-003')
chain = RetrievalQAWithSourcesChain.from_llm(llm, retriever=vector_store.as_retriever()) 
# Run the chain. 
print(chain({"question": "your question goes here"}, return_only_outputs=True))
#, return_only_outputs=True
# Print the answer and the sources.
