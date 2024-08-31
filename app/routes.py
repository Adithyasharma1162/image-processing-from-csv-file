from flask import render_template, request, jsonify
from app import app, mysql
from app.services import process_images_request_product_wise, generate_save_directory, generate_local_original_image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createRequestID', methods=['POST'])
def create_request_id():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        originalfilename = file.filename
        
        # Save the file
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename, file_extension = os.path.splitext(file.filename)
        new_filename = f"{filename}_{current_time}{file_extension}"
        
        file.save(os.path.join('files/', new_filename))

        conn = mysql.connection
        cursor = conn.cursor()
        
        query = "INSERT INTO requestfilemapping (filename, newfilename) VALUES (%s, %s)"
        cursor.execute(query, (originalfilename, new_filename))
        
        conn.commit()
        
        generated_request_id = cursor.lastrowid

        cursor.close()

        process_images_request_product_wise(new_filename, generated_request_id)

        return render_template('upload.html', message=f"Request ID Generated is: {generated_request_id}")
    else:
        return render_template('upload.html', message="Please upload a CSV file.")

@app.route('/upload')   #Upload API as well as webhook
def upload():
    return render_template('upload.html')

@app.route('/requests')
def request_page():
    conn = mysql.connection
    cursor = conn.cursor()

    query = "SELECT request_id, newfilename, current_date_time FROM REQUESTFILEMAPPING ORDER BY current_date_time DESC"
    cursor.execute(query)
    all_requests = cursor.fetchall()
        
    all_requests = [{'request_id': row[0], 'newfilename': row[1], 'current_date_time': row[2]} for row in all_requests]
    conn.commit()
    cursor.close()

    return render_template('request.html', all_requests=all_requests)

@app.route('/requestDetailpage/<int:request_id>')
def request_page_detail(request_id):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    conn = mysql.connection
    cursor = conn.cursor()

    query = "SELECT LocalOriginalImagePath, LocalProcessedImagePath FROM RequestProductImages WHERE RequestID = %s"
    cursor.execute(query, (request_id,))
    all_requests_images = cursor.fetchall()
        
    all_requests_images = [
        {
            'LocalOriginalImagePath': os.path.join(current_directory, row[0]),
            'LocalProcessedImagePath': os.path.join(current_directory, row[1])
        }
        for row in all_requests_images
    ]

    conn.commit()
    cursor.close()

    return render_template('requestDetail.html', request_id=request_id, all_requests_images=all_requests_images)

