from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Medicine Explainer API",
    description="Stage 1 MVP: manual medicine entry only. No OCR, no diagnosis.",
    version="0.1.0"
)

class MedicineRequest(BaseModel):
    medicine_name: str
    language: str = "English"

@app.get("/")
def home():
    return {"message": "Medicine Explainer API is running"}

@app.post("/explain")
def explain_medicine(request: MedicineRequest):
    medicine = request.medicine_name

    return {
        "medicine": medicine,
        "language": request.language,
        "what_it_does": f"{medicine} helps treat a specific health condition as prescribed by a doctor.",
        "why_doctors_prescribe_it": "Doctors prescribe it when they believe it supports recovery or controls symptoms.",
        "why_dosage_matters": "Taking the correct dose helps the medicine work safely and effectively.",
        "what_happens_if_skipped": "Skipping doses may reduce effectiveness or delay recovery.",
        "common_side_effects": "Some people may experience mild side effects. Ask a doctor or pharmacist if symptoms feel serious.",
        "food_instructions": "Follow the food instructions given by your doctor or pharmacist.",
        "role_in_treatment": "This medicine plays one part in your overall treatment plan.",
        "simple_explanation": f"{medicine} is being used to support your recovery. Take it exactly as instructed."
    }