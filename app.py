import streamlit as st
import openai

# --- Page Configuration ---
# Set the title and a fun icon for the browser tab.
st.set_page_config(page_title="SAP Test Case Generator", page_icon="🧪")

# --- Securely access the API key ---
# Streamlit will automatically look for the key in the .streamlit/secrets.toml file
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"] 
)

# --- The Core Function ---
# We wrap our AI logic in a function to make it reusable.
def generate_test_cases(transaction_code):
    """Calls the OpenAI API to generate test cases for a given SAP transaction."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior SAP Quality Assurance engineer. Your task is to generate clear, concise, and relevant test case titles for SAP transactions."},
                {"role": "user", "content": f"Generate 5 critical functional test case titles for the SAP transaction '{transaction_code}'."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


# --- UI Elements ---
# This creates the main title on the page.
st.title("SAP Test Case Generator 🧪")

# This creates a text input box where the user can type the transaction code.
# The text they type will be stored in the 'sap_transaction' variable.
sap_transaction = st.text_input(
    "Enter the SAP Transaction Code (e.g., VA01, ME21N):", 
    placeholder="e.g., VA01"
)

# This creates a button. For now, it doesn't do anything when clicked.
if st.button("Generate Test Cases"):
    if sap_transaction:
        st.write(f"Generating test cases for: **{sap_transaction}**")
        # Show a "loading" message while we wait for the AI
        with st.spinner(f"AI is thinking... 🧠 Generating test cases for **{sap_transaction}**..."):
            generated_cases = generate_test_cases(sap_transaction)
            # Display the result in a styled box
            st.success("Here are your generated test cases:")
            st.markdown(generated_cases)
    else:
        # Show an error if the user clicks the button without entering a code.
        st.error("Please enter an SAP transaction code.")
