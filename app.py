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

# --- The Core Function (Updated) ---
def generate_test_steps(transaction_code, test_case_title):
    """Calls the OpenAI API to generate detailed test steps."""
    # This new prompt is much more specific about the desired output format.
    prompt = f"""
    Write a detailed test case for the SAP transaction '{transaction_code}'.
    The test case title is: '{test_case_title}'.

    Please provide the following sections:
    1.  **Prerequisites:** Any data or configuration that must be ready before testing.
    2.  **Test Steps:** A numbered list of clear, step-by-step actions. For each step, include the action to perform, any data to enter, and the expected result.
    3.  **Final Expected Result:** The overall successful outcome of the test case.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a slightly more capable model can improve detailed responses
            messages=[
                {"role": "system", "content": "You are a senior SAP Quality Assurance engineer. Your task is to write detailed, step-by-step test cases for SAP transactions in a clear, structured format."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- UI Elements ---
# This creates the main title on the page.
st.title("SAP Test Case Detail Generator 📝")

st.info("First, generate test case titles, then use one of those titles here to get the detailed steps.")

# This creates a text input box where the user can type the transaction code.
# The text they type will be stored in the 'sap_transaction' variable.
sap_transaction = st.text_input(
    "Enter the SAP Transaction Code (e.g., VA01, ME21N):", 
    placeholder="e.g., VA01"
)

# New input field for the test case title
test_case_title = st.text_input(
    "Enter the Test Case Title you want to detail:",
    placeholder="e.g., Create Sales Order with Valid Customer"
)

# --- Button Logic (Updated) ---
if st.button("Generate Detailed Steps"):
    # Check if both fields have input
    if sap_transaction and test_case_title:
        with st.spinner(f"AI is crafting the steps for '{test_case_title}'... ✍️"):
            generated_steps = generate_test_steps(sap_transaction, test_case_title)
            st.success("Here is your detailed test case:")
            st.markdown(generated_steps)
    else:
        st.error("Please enter both an SAP transaction code and a test case title.")

