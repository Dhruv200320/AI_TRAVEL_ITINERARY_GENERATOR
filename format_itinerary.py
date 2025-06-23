import json

# Load itinerary JSON file
with open("itinerary.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract the itinerary text
itinerary_text = data["itinerary"]

# Split the itinerary into sections based on day-wise headers
sections = itinerary_text.split("**")

# Create a structured output
formatted_itinerary = []
current_section = ""

for section in sections:
    section = section.strip()
    if section.startswith("Day"):
        if current_section:
            formatted_itinerary.append(current_section.strip())  # Store previous section
        current_section = f"\n## {section}"  # Start new section
    else:
        current_section += f"\n{section}"

# Append the last section
if current_section:
    formatted_itinerary.append(current_section.strip())

# Save formatted itinerary to a new file
output_text = "\n".join(formatted_itinerary)

with open("formatted_itinerary.txt", "w", encoding="utf-8") as out_file:
    out_file.write(output_text)

print("Formatted itinerary saved as 'formatted_itinerary.txt'")
