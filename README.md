# Image Processing From CSV

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
  - [Upload API](#upload-api)
  - [Requests API](#requests-api)
  - [Request Detail API](#request-detail-api)
- [Database Schema](#database-schema)
  - [Request File Mapping Table](#request-file-mapping-table)
  - [Request Product Images Table](#request-product-images-table)

## Introduction

This project is a Flask-based image processing application that handles CSV files containing product information and associated image URLs. The system performs the following tasks:
1. Receives and validates CSV files uploaded by users.
2. Processes images by downloading and saving them, then compressing them if needed.
3. Stores file and image details in a MySQL database.
4. Provides APIs to upload files, view request details, and manage image processing status.

## Features

- File upload and CSV processing.
- Image downloading and local saving.
- Image processing and storage.
- Database management for tracking file and image details.
- User-friendly API endpoints.

## Tech Stack

- **Backend**: Flask
- **Database**: MySQL
- **Image Processing**: PIL (Pillow)
- **HTTP Requests**: Requests
- **CSV Handling**: pandas

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-processing-from-csv.git
   cd image-processing-from-csv

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt

## Configuration
Database Setup: Ensure MySQL is installed and running. Create a database and tables using the SQL commands provided in the Database Schema section.

Flask Configuration: Update the app/config.py file with your MySQL database credentials. Ensure that your MySQL database credentials match those in the configuration file.

## Running the Application

Start the Flask application using following command:
    ```bash
    python run.py

The application will be accessible at http://127.0.0.1:5000/.

## API Documentation

- Upload API
  - Endpoint: POST /createRequestID
  - Description: Uploads a CSV file and processes it.
  - Required Fields: The CSV should contain Serial Number, Product, and Images (comma-separated URLs).

- Requests API
  - Endpoint: GET /requests
  - Description: Retrieves a list of all file upload requests and their details.

- Request Detail API
  - Endpoint: GET /requestDetailpage/<int:request_id>
  - Description: Retrieves details of a specific request, including image paths.

## Database Schema

Request File Mapping Table
- Table Name: requestfilemapping
- Columns:
  - request_id: Primary Key, Auto Increment
  - filename: Original filename
  - newfilename: Saved filename
  - current_date_time: Timestamp of upload

Request Product Images Table
- Table Name: RequestProductImages
- Columns:
  - id: Primary Key, Auto Increment
  - RequestID: Foreign Key, references requestfilemapping(request_id)
  - ProductName: Name of the product
  - SerialNumber: Serial number of the product
  - ImageURL: URL of the image
  - LocalOriginalImagePath: Path where the original image is saved
  - LocalProcessedImagePath: Path where the processed image is saved
  - IsProcessed: Flag indicating if the image is processed