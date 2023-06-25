# vector_store
This is an example of how to create a vector store using langchain

You will require the following libraries:
- langchain
- numpy
- pickle
- openai (you dont need it, just in case you want to query LLM with this)

Dont forget to put OPENAI_API_KEY as env var

First step. Load pdf into ./pdf folder

Second step. Run:
python3 pdf_ingestor.py

This will load pdf files, split them into chunks and create a vector database faiss_store.pkl 

then change the question/model in chatbot_index.py and run 

python3 chatbot_index.py

you will get an answer in you terminal
