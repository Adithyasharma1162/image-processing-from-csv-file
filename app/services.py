import os
import pandas as pd
import requests
from PIL import Image
from app import mysql

def process_images_request_product_wise(new_filename, generated_request_id):
    df = pd.read_csv(os.path.join('files', new_filename))
    conn = mysql.connection
    cursor = conn.cursor()

    for _, row in df.iterrows():
        serial_number = row['Serial Number']
        product = row['Product']
        images = row['Images'].split(',')

        cnt = 1
        for image in images:
            save_directory = generate_save_directory(generated_request_id)
            local_original_image_path = generate_local_original_image_path(generated_request_id, product, cnt)
            save_path = os.path.join(save_directory, local_original_image_path)
            os.makedirs(save_directory, exist_ok=True)
            cnt += 1

            local_original_image_path_to_save = download_image(image, save_path)
            local_processed_image_path = create_processed_image_and_save(save_path, generated_request_id, product, cnt)

            bool_is_processed = 1 if local_processed_image_path != "ERROR OCCURED" else 0

            query = """
            INSERT INTO RequestProductImages (RequestID, ProductName, SerialNumber, ImageURL, 
            LocalOriginalImagePath, LocalProcessedImagePath, IsProcessed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (generated_request_id, product, serial_number, image, local_original_image_path_to_save, local_processed_image_path, bool_is_processed))

    conn.commit()
    cursor.close()

def generate_save_directory(generated_request_id):
    return os.path.join('Images', 'OriginaImages', str(generated_request_id))

def generate_local_original_image_path(generated_request_id, product, cnt):
    return f"RequestID_{generated_request_id}_Product_{product}_Image{cnt}.jpg"

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return save_path
    
    except requests.exceptions.RequestException as e:
        return f"Failed to download image. Error: {e}"

def create_processed_image_and_save(save_path, generated_request_id, product, cnt):
    output_directory = generate_save_processed_directory(generated_request_id)
    os.makedirs(output_directory, exist_ok=True)

    try:
        file_name, file_extension = os.path.splitext(os.path.basename(save_path))
        new_file_name = f"{file_name}_Processed{file_extension}"
        new_save_path = os.path.join(output_directory, new_file_name)
        
        with Image.open(save_path) as img:
            if file_extension.lower() in ['.jpg', '.jpeg']:
                img.save(new_save_path, quality=50, optimize=True)
            else:
                img.save(new_save_path)
            
        return new_save_path
    
    except Exception as e:
        return "ERROR OCCURED"

def generate_save_processed_directory(generated_request_id):
    return os.path.join('Images', 'ProcessedImages', str(generated_request_id))
