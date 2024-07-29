from flask import Flask, request, render_template, send_file
import os
import subprocess

app = Flask(__name__)

def convert_word_to_pdf(input_file, output_file):
    try:
        # Use unoconv to convert the Word document to PDF
        subprocess.run(['unoconv', '-f', 'pdf', '-o', output_file, input_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        raise e

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        uploads_dir = os.path.join(app.root_path, 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        input_filepath = os.path.join(uploads_dir, file.filename)
        file.save(input_filepath)
        
        output_filename = file.filename.replace('.docx', '.pdf')
        output_filepath = os.path.join(uploads_dir, output_filename)
        
        print(f"Saved input file to: {input_filepath}")
        print(f"Will save output file to: {output_filepath}")

        convert_word_to_pdf(input_filepath, output_filepath)
        
        return send_file(output_filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
