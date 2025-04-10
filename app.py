from flask import Flask, request, render_template
import pandas as pd
import os
from uens import branch_uens

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LATEST_FILENAME = 'latest_upload.csv'



@app.route('/', methods=['GET'])
def index():
    latest_file_path = os.path.join(UPLOAD_FOLDER, LATEST_FILENAME)

    return render_template('index.html', table=None)

@app.route('/submit-csv', methods=['POST'])
def submit_csv():
    file = request.files.get('csvFile')
    branch_key = request.form['branch']
    uen = branch_uens.get(branch_key, 'UNKNOWN_UEN')

    if not file or file.filename == '':
        return "No file selected."

    # Save the uploaded file with a fixed name to overwrite the previous one
    filepath = os.path.join(UPLOAD_FOLDER, LATEST_FILENAME)
    file.save(filepath)

    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(filepath)

        # Add a new column 'UEN' with the corresponding UEN value for each row
        df['UEN'] = uen

        # Convert the DataFrame to an HTML table string
        table_html = df.to_html(classes='csv-table', index=False)

        # Optionally, save the updated CSV (with UEN added) if needed
        updated_filepath = os.path.join(UPLOAD_FOLDER, LATEST_FILENAME)
        df.to_csv(updated_filepath, index=False)

        # Pass the table_html to the template
        return render_template('generate_qr.html', table=table_html)

    except Exception as e:
        return f"<h2>Error reading CSV: {e}</h2>"
    
if __name__ == '__main__':
    app.run(debug=True)