# Travel Itinerary Generator

## Overview
The **Travel Itinerary Generator** is a Flask-based web application that helps users plan their trips. It uses Google Gemini AI to generate personalized itineraries and suggest budget-friendly hotels.

## Features
- Extracts trip details (destination, days, budget) from user input.
- Suggests budget-friendly hotels from a CSV file or Google Gemini AI.
- Generates a detailed day-by-day itinerary.
- Allows users to download the itinerary as a PDF.

## Requirements
- Python 3.8+
- Flask
- pandas
- pdfkit
- google-generativeai
- wkhtmltopdf (installed on your system)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/travel-itinerary-generator.git
   cd travel-itinerary-generator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root:
     ```plaintext
     GEMINI_API_KEY=your_google_gemini_api_key
     ```
   - Replace `your_google_gemini_api_key` with your actual API key.

5. Install `wkhtmltopdf`:
   - Download and install from [wkhtmltopdf Downloads](https://wkhtmltopdf.org/downloads.html).
   - Ensure the executable is in your system's PATH or update the `PDFKIT_CONFIG` in `app.py`.

## Usage
1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Use the interface to generate itineraries and download PDFs.

## Project Structure
```
travel-itinerary-generator/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html         # Itinerary planner page
│   └── indexs.html        # Home page
├── static/                # Static files (CSS, JS, images)
├── expedia1.csv           # Hotel data
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not included in repo)
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## License
This project is licensed under the MIT License.
