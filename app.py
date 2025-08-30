import streamlit as st

# --- Page Configuration ---
# Set the title and a fun icon for the browser tab.
st.set_page_config(page_title="SAP Test Case Generator", page_icon="🧪")

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
        # We will add the OpenAI logic here in the next step!
    else:
        # Show an error if the user clicks the button without entering a code.
        st.error("Please enter an SAP transaction code.")
