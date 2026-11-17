import os
import requests
import streamlit as st

st.set_page_config(page_title="AI Email Classifier", page_icon="📧", layout="centered")
st.title("📧 LangGraph AI Email Classifier")
st.caption("Classify an email and create a reply draft. This demo does not send or delete emails.")

api_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

with st.form("email_form"):
    subject = st.text_input("Email subject", placeholder="Urgent: Client meeting tomorrow")
    email_body = st.text_area(
        "Email body",
        height=220,
        placeholder="Paste the email content here...",
    )
    submitted = st.form_submit_button("Classify email", type="primary")

if submitted:
    if not subject.strip() or not email_body.strip():
        st.warning("Please enter both an email subject and body.")
    else:
        try:
            with st.spinner("LangGraph is analyzing the email..."):
                response = requests.post(
                    f"{api_url}/classify",
                    json={"subject": subject, "email_body": email_body},
                    timeout=90,
                )
                response.raise_for_status()
                result = response.json()

            st.subheader("Classification result")
            category = result["category"]
            if category == "Important":
                st.success(f"Category: {category}")
            elif category == "Spam":
                st.error(f"Category: {category}")
            else:
                st.info(f"Category: {category}")

            st.write("**Reason:**", result["reason"])
            st.subheader("Suggested action")
            st.write(result["response"])

            if result["reply_created"]:
                st.warning("Review and edit this draft before sending it. No email has been sent.")
            else:
                st.warning("Do not reply to suspected spam. Review it manually before taking action.")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the API. Start the FastAPI server and check API_URL.")
        except requests.exceptions.HTTPError as exc:
            try:
                st.error(exc.response.json().get("detail", "The API returned an error."))
            except Exception:
                st.error("The API returned an error.")
        except requests.exceptions.RequestException:
            st.error("The request failed. Check the API server and try again.")

st.divider()
st.caption("For production Gmail integration, add OAuth, access controls, audit logging, and human approval.")
