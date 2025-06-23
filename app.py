from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pdfkit  # For generating PDFs

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Google Gemini with API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Load hotel data
HOTEL_CSV_PATH = r"E:\travel_itinerary_generator\expedia1.csv"
hotels_df = pd.read_csv(HOTEL_CSV_PATH, encoding="ISO-8859-1")

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-pro-latest")


def extract_json_from_code_block(text):
    """Extract JSON from code block like ```json ... ```"""
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    return text.strip()


def extract_trip_details(query):
    query = query.lower()

    # Extract number of days
    days_match = re.search(r"(\d+)\s*(days?|nights?)", query)
    days = int(days_match.group(1)) if days_match else None

    # Extract budget
    budget_match = re.search(r"(budget\s*is|my\s*budget\s*is|with\s*a\s*budget\s*of)\s*(\d+)", query)
    budget = int(budget_match.group(2)) if budget_match else None

    # Extract location
    location_match = re.search(r"(trip\s*(to|for)\s+|visit\s+)([\w\s]+)", query)
    location = location_match.group(3).strip() if location_match else None

    if location and days and budget:
        return {"location": location, "days": days, "budget": budget}
    else:
        return None

ALLOWED_CITY = "Mumbai"

def get_budget_hotels(destination, budget):
    """Fetches budget hotels for Mumbai, else asks Gemini for suggestions."""
    
    if destination.lower() == ALLOWED_CITY.lower():
        # Mumbai: Filter budget hotels from CSV
        hotel_budget = int(budget * 0.50)  # 50-55% of total budget
        max_hotel_budget = int(budget * 0.55)

        filtered_hotels = hotels_df[
            (hotels_df["Location"].str.lower() == destination.lower()) &  # Ensure correct column
            (hotels_df["Price"] >= hotel_budget) & 
            (hotels_df["Price"] <= max_hotel_budget)
        ]

        hotels = [
            {
                "name": row["Hotel Name"],
                "price_per_night": row["Price"],
                "rating": row.get("Rating", "N/A"),  # Ensure 'rating' exists
                "address": row["Address"]
            }
            for _, row in filtered_hotels.iterrows()
        ]

        return hotels if hotels else [{"name": "No budget-friendly hotels found"}]

    else:
        # Other Cities: Use Gemini to suggest budget hotels
        prompt = f"""
        Suggest budget-friendly hotels (₹{int(budget * 0.5)} per night) in {destination}.
        Include hotel name, estimated price, and rating.
        """
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)

        # Dynamic fallback response
        fallback_response = [
            {
                "name": f"Explore areas in {destination} known for affordable accommodations. These locations often offer a variety of budget-friendly hotels and guesthouses, well-connected to major attractions. Check online travel platforms or contact hotels directly for the best deals."
            }
        ]

        # Convert response into structured list
        hotel_suggestions = response.text.split("\n")
        hotels = [{"name": hotel.strip()} for hotel in hotel_suggestions if hotel.strip()]
        
        return hotels if hotels else fallback_response

def generate_itinerary_llm(destination, days, budget, hotels):
    """Generates a detailed itinerary using Google Gemini AI with real budget hotels."""

    accommodation_budget = int(budget * 0.45)
    per_night_budget = int(accommodation_budget / days)

    # If hotels exist, format them as text for Gemini
    if hotels:
        hotel_details = "\n".join([
            f"- {hotel.get('name', 'Unknown Hotel')} (**{hotel.get('rating', 'N/A')} rating**) - ₹{hotel.get('price_per_night', 'N/A')} per night, Address: {hotel.get('address', 'Unknown Address')}"
            for hotel in hotels
        ])
        hotel_text = f"Here are some budget-friendly hotels in {destination}:\n{hotel_details}\n\n"
    else:
        hotel_text = f"No budget-friendly hotels found in our database for {destination}. Please check local guesthouses and dormitories."

    prompt = f"""
    You are an expert travel planner. Please generate a detailed, engaging, day-by-day itinerary for a {days}-day trip to {destination} with a total budget of {budget} INR.

    - Accommodation Budget: ₹{per_night_budget}/night (₹{accommodation_budget} total for {days} days).
    - Hotels/Dormitories: {hotel_text}
    - Additional Details:
      - Suggest tourist attractions, local food options, and cultural experiences.
      - Format the response clearly with day labels (e.g., "Day 1", "Day 2", etc.).
      - Ensure hotel recommendations match the budget range.
      - Do not mention external links—only real hotel names within the budget.
    """

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    # Dynamically add symbols to the generated itinerary and clean up unwanted characters
    itinerary = response.text

    symbol_mapping = {
        "Day ": "📅",
        "Accommodation": "🏨",
        "Transportation": "🚍",
        "Food": "🍴",
        "Morning": "🌅",
        "Afternoon": "🍴",
        "Evening": "🎶",
        "Note": "💡"
    }

    # Replace symbols dynamically
    for keyword, symbol in symbol_mapping.items():
        itinerary = itinerary.replace(f"**{keyword}**", f"{symbol} {keyword}")  # Replace **keyword** with symbol + keyword
        itinerary = itinerary.replace(f"#{keyword}", f"{symbol} {keyword}")  # Replace #keyword with symbol + keyword
        itinerary = itinerary.replace(keyword, f"{symbol} {keyword}")  # Replace plain keyword with symbol + keyword

    # Remove any remaining '**' or '*' characters
    itinerary = itinerary.replace("**", "").replace("*", "")

    return itinerary

@app.route('/')
def home():
    """Serve the main front-end HTML page (indexs.html)."""
    return render_template('indexs.html')


@app.route('/plan-itinerary')
def plan_itinerary():
    """Redirect to the itinerary planner (index.html)."""
    return render_template('index.html')


@app.route('/generate_itinerary', methods=['POST'])
def generate():
    data = request.json
    user_query = data.get("input_text")

    if not user_query:
        return jsonify({"error": "Missing required query input."}), 400

    trip_details = extract_trip_details(user_query)
    
    if not trip_details:
        print("❌ ERROR: Could not extract trip details from query:", user_query)
        return jsonify({"error": "Could not extract trip details."}), 400

    destination = trip_details["location"]
    days = trip_details["days"]
    budget = trip_details["budget"]

    # Generate the itinerary synchronously
    # Generate the itinerary synchronously
    hotels = get_budget_hotels(destination, budget)
    itinerary = generate_itinerary_llm(destination, days, budget, hotels)

    return jsonify({"itinerary": itinerary})

# Specify the path to wkhtmltopdf
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    """Generate and download the itinerary as a PDF."""
    data = request.json
    itinerary = data.get("itinerary")

    if not itinerary:
        return jsonify({"error": "Missing itinerary content."}), 400

    # Save the itinerary as an HTML file with UTF-8 encoding
    html_content = f"""
    <html>
        <head>
        <title>Itinerary</title>
        <meta charset="UTF-8"> <!-- Ensure proper encoding -->
        <style>
            body {{
                font-family: 'Noto Sans', 'Arial Unicode MS', sans-serif; /* Ensure Unicode support */
                line-height: 1.6;
                color: #333;
            }}
            h1 {{
                text-align: center;
                color: #4a90e2;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <h1>Your Travel Itinerary</h1>
        <pre>{itinerary}</pre>
    </body>
    </html>
    """
    with open("itinerary.html", "w", encoding="utf-8") as file:  # Specify UTF-8 encoding
        file.write(html_content)

    # Convert the HTML file to a PDF
    pdfkit.from_file("itinerary.html", "itinerary.pdf", configuration=PDFKIT_CONFIG)

    # Send the PDF file to the user
    return send_file("itinerary.pdf", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)  # Use Flask's default run method
