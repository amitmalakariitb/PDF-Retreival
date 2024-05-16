import os
import tempfile
import asyncio
import streamlit as st
from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from htmlTemplates import css,hide_st_style, footer
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import create_qa_with_sources_chain, RetrievalQA
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from helpers import preprocess_text, handle_userinput, display_chat_history



load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB = os.getenv("MONGODB_DB")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

client = MongoClient(MONGODB_URL)
db = client[MONGODB_DB]
collection = db[MONGODB_COLLECTION]


async def preprocess_data(file): 
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    pages = loader.load_and_split()
    
    
    for i, page in enumerate(pages):
        processed_text=preprocess_text(page.page_content)
        page_content = processed_text
        source = page.metadata["source"]
        page_number = page.metadata["page"]
        document = {
            "text_chunk": page_content,
            "source": source,
            "page": page_number,
        }
        collection.insert_one(document)
    return pages


def get_vectorstore(pages):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(pages, embedding_function)
    return db

def get_conversation_chain(db):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    qa_chain = create_qa_with_sources_chain(llm)
    
    doc_prompt = PromptTemplate(
        template="Content: {page_content} \n Page:{page}", 
        input_variables=["page_content","page"],
    )
    final_qa_chain = StuffDocumentsChain(
            llm_chain=qa_chain,
            document_variable_name='context',
            document_prompt=doc_prompt,
    )
    retrieval_qa = RetrievalQA(
            retriever=db.as_retriever(),
            combine_documents_chain=final_qa_chain
        )
    
    return retrieval_qa

   
async def main():
    load_dotenv()
    st.set_page_config(page_title="PDF Retreival",
                    page_icon="icon.jpeg")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with AI with PDF Data 🚀")
    user_question = st.text_input("Ask a question from your PDF:")

    with st.sidebar:
        st.subheader("Your documents")
        file = st.file_uploader(
            "Upload your Data here  in PDF format and click on 'Process'", accept_multiple_files=True, type=['pdf'])

        if st.button("Process"):
            if file is None:
                st.error("Please upload at least one PDF file.")
            else:
                with st.spinner("Processing"):
                    pages = await preprocess_data(file)
                    db = get_vectorstore(pages)
                    st.session_state.conversation = get_conversation_chain(db)
                    st.session_state.chat_history = []
                    st.success("Your Data has been processed successfully")

    if user_question:
        handle_userinput(user_question)

    display_chat_history()

    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == '__main__':
    asyncio.run(main())
