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
# The function now accepts a 'test_type' argument
def generate_test_steps(transaction_code, test_case_title, test_type):
    """Calls the OpenAI API to generate detailed test steps based on test type."""
    
    # We create a more dynamic prompt based on the user's choice
    prompt = f"""
    Write a detailed '{test_type}' test case for the SAP transaction '{transaction_code}'.
    The test case title is: '{test_case_title}'.

    - If this is a 'Positive (Happy Path)' test, the steps must lead to a successful transaction completion.
    - If this is a 'Negative (Error Handling)' test, the steps must intentionally include an incorrect action or invalid data to trigger a specific, predictable error message.

    Please provide the following sections:
    1.  **Objective:** A one-sentence goal for this test case.
    2.  **Prerequisites:** Any data or configuration that must be ready.
    3.  **Test Steps:** A numbered list of clear, step-by-step actions. For each step, include the action, data to enter, and the expected result (which could be an error message for a negative test).
    4.  **Final Expected Result:** The overall successful or failed outcome.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior SAP Quality Assurance engineer. Your task is to write detailed, step-by-step test cases for SAP transactions in a clear, structured format, differentiating between positive and negative scenarios."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- UI Elements (Updated) ---
st.title("SAP Test Case Detail Generator 📝")

sap_transaction = st.text_input(
    "Enter the SAP Transaction Code:", 
    placeholder="e.g., VA01"
)

test_case_title = st.text_input(
    "Enter the Test Case Title:",
    placeholder="e.g., Create Sales Order with an invalid material"
)

# --- NEW: Dropdown to select test type ---
test_type = st.selectbox(
    "Select the type of test case:",
    ("Positive (Happy Path)", "Negative (Error Handling)")
)

# --- Button Logic (Updated) ---
if st.button("Generate Detailed Steps"):
    if sap_transaction and test_case_title:
        with st.spinner(f"AI is crafting the '{test_type}' steps for '{test_case_title}'... ✍️"):
            # We now pass the 'test_type' to our function
            generated_steps = generate_test_steps(sap_transaction, test_case_title, test_type)
            st.success("Here is your detailed test case:")
            st.markdown(generated_steps)
    else:
        st.error("Please enter both an SAP transaction code and a test case title.")


