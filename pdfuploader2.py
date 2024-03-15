import io
import os
import PyPDF2
import openai
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual key
openai.api_key = ''

def truncate_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length]

def get_default_queries():
    return [
        "Minting Function",
        "Burning Function",
        "Transfer Function and Rights of Owner",
    ]

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        return render_template('upload1.html', default_queries=get_default_queries())
    elif request.method == 'POST':
        # Handle the case when the form is submitted using POST with a file upload
        pdf_file = request.files['pdf_file']
        queries = [
            request.form.get('query1', ''),
            request.form.get('query2', ''),
            request.form.get('query3', ''),
        ]

        if pdf_file and pdf_file.filename.lower().endswith(('.pdf')):
            # Save the uploaded file temporarily
            pdf_file_path = os.path.join("temp", pdf_file.filename)
            pdf_file.save(pdf_file_path)

            # Step 3: Extract text from uploaded PDF
            pdf_text = extract_text_from_pdf(pdf_file_path)

            # Step 4: Analyze PDF using OpenAI
            results = analyze_pdf(pdf_text, queries)

            # Step 5: Display analysis results
            return render_template('analysis_results1.html', results=results, queries=queries)
        else:
            return "Invalid file format. Please upload a PDF file."

def analyze_pdf(pdf_text, queries):
    # Use OpenAI API for analysis
    results = {}

    for i, query in enumerate(queries):
        if not query:
            query = get_default_queries()[i]

        # Truncate pdf_text and user's message to fit within the model's maximum context length
        truncated_pdf_text = truncate_text(pdf_text, 3097 - len(f"Query {i+1}: {query}\n"))
        truncated_user_message = truncate_text(truncated_pdf_text, 1111)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": truncated_user_message},
                {"role": "assistant", "content": f"Query {i+1}: {query}"}
            ],
            max_tokens=3097  # Set the maximum context length
        )

        results[f"Query {i+1}"] = response['choices'][0]['message']['content'].strip()

    return results

def extract_text_from_pdf(pdf_source):
    # Fetch PDF content
    pdf_content = fetch_pdf_content(pdf_source)

    # Extract text from PDF content
    pdf_text = get_pdf_text(pdf_content)

    return pdf_text

def fetch_pdf_content(pdf_source):
    # Read PDF content from local file
    with open(pdf_source, 'rb') as file:
        return file.read()

def get_pdf_text(pdf_content):
    if not pdf_content:
        return ""

    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
