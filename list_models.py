import google.generativeai as genai

# Configure the API Key (Replace YOUR_API_KEY with your actual key)
genai.configure(api_key="AIzaSyDtwiSDYatsJvpBFKCgQsNU0lpQK1r1xT0")

# Fetch available models
models = genai.list_models()

# Print available models
print("Available Generative AI Models:")
for model in models:
    print(model.name)
