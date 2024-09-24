import streamlit as st
import subprocess
import os

def query_llama3(question):
    # Ensure you have the command correct as per your environment
    command = f'python query_data.py "{question}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def main():
    st.title("Llama3 Question Answering")
    st.write("Enter your question below and get an answer from the Llama3 model.")

    question = st.text_input("Your Question:")

    if st.button("Get Answer"):
        if question:
            with st.spinner("Getting answer..."):
                answer = query_llama3(question)
                st.write("**Answer:**")
                st.write(answer)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()
