import os
from langchain.document_loaders import PyPDFLoader
#import openai #new
#we dont need pickle, let it be here just in case
import faiss #new
import numpy as np #new

pdf_directory = "./pdf"
#content = "./pdf/volume1.pdf"  # That's where we will store text from pdf

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import pickle

pdf_files = os.listdir(pdf_directory)  # list all files in the directory

all_pages = []

for pdf_file in pdf_files:
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, pdf_file)  # create the full path to the PDF file
        loader = PyPDFLoader(pdf_path)  # load the PDF
        pages = loader.load_and_split()  # split the PDF into pages
        all_pages.append(pages)  # add the pages to our list
#flattening to get 1 dim array of objects
all_pages_flat = [paragraph for page in all_pages for paragraph in page]
# flattening further to get an array of strings
all_pages_flat_content = [doc.page_content for doc in all_pages_flat]

from langchain.text_splitter import CharacterTextSplitter
#split all_pages into as per defined splitter rules
splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)

docs = splitter.create_documents(all_pages_flat_content) #could not split the list somewhere deep, converted to string

from langchain.text_splitter import Document

# First, split the page_content of each Document in all_pages_flat into chunks.
chunks = [chunk for doc in all_pages_flat for chunk in splitter.split_text(doc.page_content)]

# Now, chunks is a list of strings, where each string is a chunk of page_content from a Document in all_pages_flat.

# Next, create new Documents from the chunks, and copy the metadata from the original Documents to the new Documents.
docs = []
for original_doc in all_pages_flat:
    for chunk in splitter.split_text(original_doc.page_content):
        # Create a new Document with the chunk as its page_content, and the metadata of original_doc.
        new_doc = Document(page_content=chunk, metadata=original_doc.metadata.copy())
        docs.append(new_doc)

# Now, docs is a list of Documents, where each Document has a chunk of page_content and the same metadata as the original Document from which the chunk came.


OpenAI.api_key = os.getenv("OPENAI_API_KEY")
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
#REMOVE COMMENTS IN BELOW THREE LINES
vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())

with open("faiss_store.pkl", "wb") as f:
    pickle.dump(vector_store, f)
