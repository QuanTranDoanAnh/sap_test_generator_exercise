import streamlit as st
import openai

# --- Page Configuration ---
# Set the title and a fun icon for the browser tab.
st.set_page_config(page_title="SAP Test Case Generator", page_icon="🧪")

# --- Initialize Session State ---
# This creates a "memory" for the app to store the last generated test case.
if 'last_generated_case' not in st.session_state:
    st.session_state.last_generated_case = ""
if 'last_generated_data' not in st.session_state:
    st.session_state.last_generated_data = ""


# --- Securely access the API key ---
# Streamlit will automatically look for the key in the .streamlit/secrets.toml file
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"] 
)

# --- The Core Function (Updated) ---
# The function now accepts a 'test_type' argument
def generate_test_steps(transaction_code, test_case_title, test_type):
    """Calls the OpenAI API to generate detailed test steps."""
    prompt = f"""
    Write a detailed '{test_type}' test case for the SAP transaction '{transaction_code}'.
    The test case title is: '{test_case_title}'.

    - If this is a 'Positive (Happy Path)' test, the steps must lead to a successful transaction completion.
    - If this is a 'Negative (Error Handling)' test, the steps must intentionally include an incorrect action or invalid data to trigger a specific, predictable error message.

    Please provide the following sections:
    1.  **Objective:** A one-sentence goal for this test case.
    2.  **Prerequisites:** Any data or configuration that must be ready.
    3.  **Test Steps:** A numbered list of clear, step-by-step actions.
    4.  **Final Expected Result:** The overall successful or failed outcome.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior SAP Quality Assurance engineer who writes detailed, structured test cases."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- NEW: Function to generate test data ---
def generate_test_data(test_case_text):
    """Calls the OpenAI API to generate sample data for a given test case."""
    prompt = f"""
    Based on the following SAP test case, generate a simple table of realistic, sample test data.
    The data should include plausible values for the key input fields mentioned in the test steps.
    Format the output as a clean markdown table.

    Test Case:
    ---
    {test_case_text}
    ---
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates sample test data for SAP test cases."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


# --- NEW: Function to generate Robot Framework script ---
def generate_robot_script(test_case_text, test_data_text):
    """Generates a Robot Framework script from a test case and data."""
    prompt = f"""
    Act as an expert QA automation engineer specializing in Robot Framework for SAP.
    Convert the following natural language test case and its test data into a complete Robot Framework script (.robot file).

    Follow these instructions:
    1.  Assume a hypothetical library named `SAPLibrary` is being used.
    2.  Use the provided Test Data to create scalar variables in the `*** Variables ***` section.
    3.  Translate the natural language steps from the test case into logical keywords in the `*** Test Cases ***` section.
    4.  The keywords should be plausible for SAP automation (e.g., `Open Transaction`, `Input Text In Field`, `Click SAP Button`, `Verify Status Bar Message`).
    5.  Wrap the final script in a markdown code block.

    Test Case:
    ---
    {test_case_text}
    ---

    Test Data:
    ---
    {test_data_text}
    ---
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # A more advanced model is better for code generation
            messages=[
                {"role": "system", "content": "You are an expert QA automation engineer specializing in Robot Framework and SAP."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the code from the markdown block if it exists
        response_text = response.choices[0].message.content
        if "```robotframework" in response_text:
            return response_text.split("```robotframework")[1].split("```")[0].strip()
        elif "```" in response_text:
            return response_text.split("```")[1].strip()
        else:
            return response_text
    except Exception as e:
        return f"An error occurred: {e}"

# --- UI Elements (Updated) ---
st.title("SAP Test Case Detail Generator 📝")

sap_transaction = st.text_input(
    "Enter the SAP Transaction Code:", 
    placeholder="e.g., ME21N"
)
test_case_title = st.text_input(
    "Enter the Test Case Title:",
    placeholder="e.g., Create a standard Purchase Order"
)
test_type = st.selectbox(
    "Select the type of test case:",
    ("Positive (Happy Path)", "Negative (Error Handling)")
)

if st.button("Generate Detailed Steps"):
    if sap_transaction and test_case_title:
        with st.spinner("AI is crafting the steps... ✍️"):
            # Clear old data when generating a new case
            st.session_state.last_generated_data = ""
            st.session_state.last_generated_case = generate_test_steps(sap_transaction, test_case_title, test_type)
    else:
        st.error("Please enter both an SAP transaction code and a test case title.")

# Display the generated test case if it exists
if st.session_state.last_generated_case:
    st.success("Here is your detailed test case:")
    st.markdown(st.session_state.last_generated_case)
    # If data hasn't been generated yet for this case, show the button
    if not st.session_state.last_generated_data:
        if st.button("Generate Test Data 📊"):
            with st.spinner("AI is generating sample data... 🔢"):
                st.session_state.last_generated_data = generate_test_data(st.session_state.last_generated_case)

# Display the generated data if it exists
if st.session_state.last_generated_data:
    st.markdown(st.session_state.last_generated_data)
    st.info("Now you can generate the Robot Framework script.")
    if st.button("Generate Robot Script 🤖"):
        with st.spinner("AI is building the Robot script... 🦾"):
            generated_script = generate_robot_script(st.session_state.last_generated_case, st.session_state.last_generated_data)
            st.code(generated_script, language='robotframework')


