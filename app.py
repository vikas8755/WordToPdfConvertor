from flask import Flask, request, render_template, send_file
import os
import logging
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def convert_word_to_pdf(input_file, output_file):
    try:
        # Read the Word document
        doc = Document(input_file)
        # Create a PDF file
        pdf = canvas.Canvas(output_file, pagesize=letter)
        width, height = letter
        # Write the content of the Word document to the PDF file
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        pdf.drawString(30, height - 30, text)
        pdf.save()
    except Exception as e:
        logging.error(f"Error during conversion: {e}")
        raise e

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file")
        return 'No selected file', 400
    
    if file:
        try:
            uploads_dir = os.path.join(app.root_path, 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            
            input_filepath = os.path.join(uploads_dir, file.filename)
            file.save(input_filepath)
            
            output_filename = file.filename.replace('.docx', '.pdf')
            output_filepath = os.path.join(uploads_dir, output_filename)
            
            logging.info(f"Saved input file to: {input_filepath}")
            logging.info(f"Will save output file to: {output_filepath}")

            convert_word_to_pdf(input_filepath, output_filepath)
            
            return send_file(output_filepath, as_attachment=True)
        
        except Exception as e:
            logging.error(f"Failed to convert file: {e}")
            return f"Failed to convert file: {e}", 500

#if __name__ == "__main__":
#    app.run(debug=True)
