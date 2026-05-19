import streamlit as st
import requests

st.set_page_config(page_title="Medicine Explainer", page_icon="💊")

st.title("💊 Medicine Explainer AI")
st.write("Understand your medicine in simple language.")

medicine_name = st.text_input("Enter medicine name", placeholder="Example: Azithromycin 500mg")

language = st.selectbox(
    "Choose language",
    ["English", "Hindi", "Gujarati", "Tamil", "Telugu", "Marathi", "Kannada", "Bengali"]
)

if st.button("Explain Medicine"):
    if not medicine_name.strip():
        st.warning("Please enter a medicine name.")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/explain",
            json={
                "medicine_name": medicine_name,
                "language": language
            }
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader(data["medicine"])

            st.markdown(f"**What it does:** {data['what_it_does']}")
            st.markdown(f"**Why doctors prescribe it:** {data['why_doctors_prescribe_it']}")
            st.markdown(f"**Why dosage matters:** {data['why_dosage_matters']}")
            st.markdown(f"**What happens if skipped:** {data['what_happens_if_skipped']}")
            st.markdown(f"**Common side effects:** {data['common_side_effects']}")
            st.markdown(f"**Food instructions:** {data['food_instructions']}")
            st.markdown(f"**Role in treatment:** {data['role_in_treatment']}")
            st.info(data["simple_explanation"])
        else:
            st.error("Backend error. Check if FastAPI is running.")