from flask import Flask, render_template, request, session
import subprocess
import os
import time
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_random_secret_key_123'  # Set a secret key for session encryption

# Set session timeout to the amount of time you want
app.permanent_session_lifetime = timedelta(minutes=30)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Query the Llama3 model
def query_llama3(question, session_data_file=None):
    try:
        # Ensure the command is running in the correct directory
        script_path = os.path.join(os.path.dirname(__file__),
                                   'C:/Users/amar_/Desktop/Amar/rag-tutorial-v2-main/query_data.py')  #Change this to your directory
        if not os.path.exists(script_path):
            return f"Error: {script_path} not found"

        command = ['python', script_path, question]
        if session_data_file:
            command.append(session_data_file)

        result = subprocess.run(command, capture_output=True, text=True)

        # Log stdout and stderr for debugging
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0:
            return result.stdout.strip()  # Remove any extraneous whitespace
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Exception: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    error = None

    # Ensure session is permanent (to allow expiration after timeout)
    session.permanent = True

    if request.method == 'POST':
        question = request.form['question']

        # Handle file upload
        uploaded_file = request.files.get('pdf_file')
        if uploaded_file:
            # Save the uploaded file temporarily
            filename = secure_filename(uploaded_file.filename)
            temp_pdf_path = os.path.join('temp_uploads', filename)
            uploaded_file.save(temp_pdf_path)

            # Extract text from the uploaded PDF
            session_pdf_content = extract_text_from_pdf(temp_pdf_path)

            # Store the extracted text and PDF path in session
            session['pdf_content'] = session_pdf_content
            session['temp_pdf_path'] = temp_pdf_path
            session['start_time'] = time.time()  # Track session start time

        # Check if the session is still valid
        if 'start_time' in session:
            elapsed_time = time.time() - session.get('start_time', 0)
            if elapsed_time > app.permanent_session_lifetime.total_seconds():
                # Session expired, remove PDF content and delete the file
                session.pop('pdf_content', None)
                temp_pdf_path = session.pop('temp_pdf_path', None)
                if temp_pdf_path and os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)  # Delete the file after the timer ends
                return render_template('index.html', answer=None,
                                       error="Session expired. PDF file has been deleted. Please upload the PDF again.")

        # Check if there's PDF content in session
        #if 'pdf_content' not in session:
        """
        
        """

        session_data_file = None #os.path.join('../data',' ')
        if 'pdf_content' in session:
            session_data_file = os.path.join('temp_uploads', 'temp_session_data.txt')
            with open(session_data_file, 'w') as f:
                f.write(session['pdf_content'])

        # Query the Llama3 model with the question and session data file
        answer = query_llama3(question, session_data_file)
        if answer.startswith("Error:") or answer.startswith("Exception:"):
            error = answer
            answer = None

        # Clean up the session data file after use, but don't delete the PDF file
        if session_data_file:
            os.remove(session_data_file)

    return render_template('index.html', answer=answer, error=error)

@app.route('/clear_session', methods=['POST'])
def clear_session():
    # Remove the PDF content and file path from the session
    session.pop('pdf_content', None)
    temp_pdf_path = session.pop('temp_pdf_path', None)

    # Delete the temporarily saved PDF file if it exists
    if temp_pdf_path and os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)

    return render_template('index.html', answer=None, error=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    if not os.path.exists('temp_uploads'):
        os.makedirs('temp_uploads')
    app.run(debug=True)
