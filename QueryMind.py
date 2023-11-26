from openai import OpenAI
from flask import Flask, request, render_template, url_for
import os
from dotenv import load_dotenv

app = Flask(__name__, static_url_path='/static')

load_dotenv()

# CHANGE 
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def read_file(file_path, encoding='latin-1'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        return content
    except UnicodeDecodeError:
        # If the specified encoding doesn't work, handle the error or try different encodings
        print("Failed to read using specified encoding. Trying another one.")
        return None

def ask_openai(question, context):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]
    )

    return(completion.choices[0].message.content)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML template

@app.route('/ask_openai', methods=['POST'])
def chat():
    file_path = request.form['filePath']
    question = request.form['question']
    file_content = read_file(file_path)

    if file_content:
        answer = ask_openai(question, file_content)
        return answer
    else:
        return "Error: Failed to read file content."

if __name__ == '__main__':
    app.run()
