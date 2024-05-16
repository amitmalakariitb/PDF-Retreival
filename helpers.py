import re
import nltk
import json
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    preprocessed_text = ' '.join(filtered_tokens)
    
    return preprocessed_text

def display_and_format_response(response):
    result=response["result"]
    try:
        result_dict = json.loads(result)
    except json.JSONDecodeError:
        st.error("Error parsing response. Invalid JSON format.")
        return
    
    if "answer" in result_dict:
        answer=result_dict["answer"]
        st.write(result_dict["answer"])
    else:
        st.warning("No answer available.")

    if "sources" in result_dict:
        sources = result_dict["sources"]
        if sources:
            st.write("Sources:")
            for idx, source in enumerate(sources, start=1):
                st.write(f"{idx}. {source}")
        else:
            st.warning("No sources available.")
    else:
        st.warning("No sources available.")

    formatted_response = {
        "answer": answer,
        "sources": sources
    }
    
    return formatted_response


def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload PDF data before starting the chat.")
        return

    response = st.session_state.conversation(user_question)
    # st.write(response)
    
    formatted_response=display_and_format_response(response=response)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat_history.append({
        'user_question': user_question,
        'response': formatted_response
    })

def display_chat_history():
    if st.session_state.chat_history:  
        st.write("Chat History:")
        for idx, entry in enumerate(st.session_state.chat_history):
            st.write(f"Question {idx + 1}: {entry['user_question']}")
            st.write(f"Response {idx + 1}: {entry['response']}")
    else:
        st.write("No chat history available.")
