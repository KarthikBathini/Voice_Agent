import google.generativeai as genai
import json
import re
import dotenv
GEMINI_API_KEY = "AIzaSyATnod56sv6n7LwPhJNY45eNk0Pz7HHB4k"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat()

prompt_template = """
You are an intent extractor for a voice assistant that performs:
1. Product ordering (Flipkart, Amazon)
2. Video playing (YouTube)
3. Food ordering (Swiggy, Zomato)
4. General topics (Google)
From the following command, extract the correct intent and entities.

Examples:
Command: "Order an iPhone 15 from Flipkart"
Response:
{{
  "intent": "OrderProduct",
  "entities": {{
    "product": "iPhone 15",
    "platform": "Flipkart"
  }}
}}

Command: "Play a trailer for Inception on YouTube"
Response:
{{
  "intent": "PlayVideo",
  "entities": {{
    "product": "Inception trailer",
    "platform": "YouTube"
  }}
}}

Command: "Order chicken biryani from Paradise in Hyderabad using Swiggy"
Response:
{{
  "intent": "OrderFood",
  "entities": {{
    "food_item": "chicken biryani",
    "restaurant": "Paradise",
    "location": "Hyderabad",
    "platform": "Swiggy"
  }}
}}

Now extract from:
Command: "{command}"

Respond only in JSON.
"""



def extract_intent(command):
    try:
        prompt = prompt_template.format(command=command)
        print("📝 Sending prompt to Gemini:\n", prompt[:300], "...\n")

        response = chat.send_message(prompt)

        if not response:
            print("❌ No response object returned.")
            return None, {}

        if not hasattr(response, "text"):
            print("⚠️ Response has no .text attribute. Response object:", response)
            return None, {}

        text = response.text.strip()
        print("🔍 Raw Gemini response:\n", text)

        # Regex to extract JSON with "intent" and "entities"
        json_match = re.search(r'\{\s*"intent"\s*:\s*".+?",\s*"entities"\s*:\s*\{.*?\}\s*\}', text, re.DOTALL)

        if not json_match:
            print("⚠️ No valid JSON block found in response.")
            return None, {}

        json_text = json_match.group(0)
        print("📦 Extracted JSON:\n", json_text)

        data = json.loads(json_text)
        return data.get("intent"), data.get("entities")

    except Exception as e:
        print("❌ Error parsing intent:", e)
        return None, {}
