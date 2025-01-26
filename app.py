from flask import Flask, render_template, request, send_file, redirect, url_for, abort
import os
import zipfile
from werkzeug.utils import secure_filename
from converters.pdf_to_word import convert_pdf_to_word
from converters.compress_pdf import convert_compress_pdf
from converters.pdf_to_powerpoint import convert_pdf_to_powerpoint
from converters.csv_to_excel import convert_csv_to_excel
from converters.csv_to_database import convert_csv_to_database
from converters.csv_cleaning import clean_csv
from converters.excel_to_pdf import convert_excel_to_pdf
from converters.ppt_to_pdf import convert_ppt_to_pdf
from converters.pdf_to_jpg import convert_pdf_to_jpg
from converters.sign_pdf import sign_pdf
from converters.watermark_pdf import add_text_watermark, add_image_watermark
VALID_TOOLS = [
    "pdf-to-word",
    "pdf-to-powerpoint",
    "csv-to-excel",
    "csv-to-database",
    "compress-pdf",
    "excel-to-csv",
    "clean-csv",
    "excel-to-pdf",
    "ppt-to-pdf",
    "pdf-to-jpg",
    "jpg-to-pdf",
    "sign-pdf",
    "watermark-pdf"
]

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'xlsx', 'xls', 'pptx', 'txt', 'jpg', 'jpeg', 'png'}

# Flask app configuration
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
CONVERTED_FOLDER = 'uploads/converted_files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

# Ensure the converted files directory exists
if not os.path.exists(CONVERTED_FOLDER):
    os.makedirs(CONVERTED_FOLDER)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tool/<tool_name>', methods=['GET', 'POST'])
def tool(tool_name):
    """Dynamic route for all tools."""
    
    if tool_name not in VALID_TOOLS:
        return render_template('error.html', message=f"Tool '{tool_name}' not found."), 404

    if request.method == 'POST':
        file = request.files['file']
        if not file or file.filename == '':
            return "No file uploaded", 400

        if not allowed_file(file.filename):
            return "Invalid file type", 400

        # Secure the filename and save it
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        table_name = os.path.splitext(filename)[0]

        # Tool logic based on tool_name
        try:
            if tool_name == "pdf-to-word":
                result_path = convert_pdf_to_word(upload_path, app.config['CONVERTED_FOLDER'])
            elif tool_name == "pdf-to-powerpoint":
                result_path = convert_pdf_to_powerpoint(upload_path, app.config['CONVERTED_FOLDER'])
            elif tool_name == "csv-to-excel":
                result_path = convert_csv_to_excel(upload_path, app.config['CONVERTED_FOLDER'])
            elif tool_name == "csv-to-database":
                result_path = convert_csv_to_database(upload_path, app.config['CONVERTED_FOLDER'], table_name)
            elif tool_name == "compress-pdf":
                result_path = convert_compress_pdf(upload_path, app.config['CONVERTED_FOLDER'])
            elif tool_name == "clean-csv":
                result_path = clean_csv(upload_path, app.config['CONVERTED_FOLDER'])
            elif tool_name == "excel-to-pdf":
                result_path = convert_excel_to_pdf(upload_path, app.config['CONVERTED_FOLDER'])
            elif tool_name == "ppt-to-pdf":
                result_path = convert_ppt_to_pdf(upload_path, app.config['CONVERTED_FOLDER'])
            elif tool_name == "sign-pdf":
                signature_text = request.form['signature_text']
                output_pdf_path = os.path.join(app.config['CONVERTED_FOLDER'], f"signed_{file.filename}")
                result_path = sign_pdf(upload_path, output_pdf_path, signature_text)
            elif tool_name == "pdf-to-jpg":
                result_path = convert_pdf_to_jpg(upload_path, app.config['CONVERTED_FOLDER'])
                # Create a zip of JPG files
                zip_filename = os.path.join(app.config['CONVERTED_FOLDER'], f"{os.path.basename(upload_path)}_images.zip")
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for image_file in os.listdir(result_path):
                        zipf.write(os.path.join(result_path, image_file), image_file)
                
                # Remove the original uploaded file after conversion is done
                if os.path.exists(upload_path):
                    os.remove(upload_path)

                # Remove the folder after zipping its contents
                if os.path.exists(result_path):
                    for file in os.listdir(result_path):
                        os.remove(os.path.join(result_path, file))
                    os.rmdir(result_path)  # Remove the now-empty folder

                return send_file(zip_filename, as_attachment=True, download_name=os.path.basename(zip_filename), mimetype='application/zip')

        except Exception as e:
            # Ensure to clean up temporary files in case of an error
            if os.path.exists(upload_path):
                os.remove(upload_path)
            return render_template('error.html', message=str(e)), 500

        # Send the processed file to the user
        return send_file(result_path, as_attachment=True, download_name=os.path.basename(result_path), mimetype='application/octet-stream')

    # Render upload page for the specific tool
    return render_template('upload.html', tool_name=tool_name)

if __name__ == '__main__':
    app.run(debug=True)
