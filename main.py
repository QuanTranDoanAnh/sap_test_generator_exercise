from dotenv import load_dotenv
import os
import openai

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")
# --- Configuration ---
# This is where you set up your connection to OpenAI.
# Make sure to replace "YOUR_API_KEY_HERE" with your actual secret key.
client = openai.OpenAI(api_key=api_key)

# --- The AI's Instruction ---
# Here, we tell the AI what we want it to do.
# The 'system' role sets the AI's persona or main goal.
# The 'user' role is the specific prompt we're giving it right now.
print("Sending prompt to OpenAI...")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialized in generating software test cases."},
        {"role": "user", "content": "Generate 3 test case titles for SAP transaction VA01."}
    ]
)

# --- Display the Result ---
# The AI's answer is inside the response object. This line extracts and prints it.
ai_message = response.choices[0].message.content
print("\n--- AI Response ---")
print(ai_message)
print("-------------------")