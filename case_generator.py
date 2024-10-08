# Case generator.py 
# For now a case is interchangeable with a patient. 

import pydantic
from datetime import datetime
from typing import List, Dict, Any, Tuple

class Case(pydantic.BaseModel):
    # Static data
    name: str
    age: int
    gender: str
    chief_complaint: Dict[str, Any]
    history_of_present_illness: Dict[str, Any]
    past_medical_history: List[str]
    medications_allergies: Dict[str, List[str]]
    past_surgical_history: List[str]
    social_history: Dict[str, str]
    family_history: Dict[str, str]
    # Dynamic data with timestamps
    
    review_of_systems: Dict[str, Any]
    physical_exam: List[Tuple[Dict[str, str], str]]  # List of tuples (exam findings, timestamp)
    labs: Dict[str, Any]
    images: Dict[str, Any]
    consults: Dict[str, Any]
    vitals: Dict[str, Any]
    log: List[Dict[str, Any]] = []

    def update_dynamic_data(self, field: str, new_value: Any):
        """Update a dynamic field in the case and log the change with a timestamp."""
        if hasattr(self, field):
            if field == 'physical_exam':
                # Append new exam findings with timestamp
                timestamp = datetime.now().isoformat()
                self.physical_exam.append((new_value, timestamp))
                self.log_change(field, None, new_value, timestamp)
            else:
                old_value = getattr(self, field)['value']
                timestamp = datetime.now().isoformat()
                setattr(self, field, {'value': new_value, 'timestamp': timestamp})
                self.log_change(field, old_value, new_value, timestamp)
        else:
            raise AttributeError(f"Field {field} does not exist in the case.")

    def log_change(self, field: str, old_value: Any, new_value: Any, timestamp: str):
        """Log the change of a field with a timestamp."""
        self.log.append({
            "timestamp": timestamp,
            "field": field,
            "old_value": old_value,
            "new_value": new_value
        })

# Example instantiation and update
case_example = Case(
    name="John Doe",
    age=60,
    gender="Male",
    past_medical_history=["Hypertension"],
    medications_allergies={"Medications": ["Lisinopril"], "Allergies": ["Codeine", "Shellfish"]},
    past_surgical_history=["Hernia repair, age 22"],
    social_history={"EtOH": "Occasional", "Tobacco": "Denies", "Illicits": "Denies", "Occupation": "Ambassador to the U.S.", "Additional": "Married"},
    family_history={"Father": "Gastric cancer, expired age 80"},
    chief_complaint={"value": "Chest pain, 'There is an elephant sitting on my chest.'", "timestamp": datetime.now().isoformat()},
    history_of_present_illness={"value": (
        "Patient complains of crushing substernal chest pain radiating to his neck and jaw on the left side. "
        "Symptoms started one hour ago during a business meeting. Patient had to excuse himself from the "
        "meeting as he became obviously diaphoretic and pale. Patient reports nausea and lightheadedness "
        "after the onset of the 'crushing' chest pain. Patient denies fevers, chills, vomiting, and palpitations. "
        "Patient reports mild shortness of breath and one previous episode of chest pain that lasted about 15 "
        "minutes one week ago that resolved spontaneously while he was in Japan."
    ), "timestamp": datetime.now().isoformat()},
    review_of_systems={"value": {
        "Positive": ["Chest pain with radiation to neck/jaw", "mild shortness of breath", "diaphoresis", "nausea", "lightheadedness"],
        "Negative": ["Denies palpitations", "vomiting", "headache", "blurred vision", "numbness/motor weakness", "abdominal pain", "urinary symptoms", "fever/chills"]
    }, "timestamp": datetime.now().isoformat()},
    physical_exam=[],  # Start with an empty list
    labs={"value": ["Basic Metabolic Panel", "Cardiac Markers", "Coagulation Profile", "CBC with differential"], "timestamp": datetime.now().isoformat()},
    images={"value": ["ECG", "CT Scan, without contrast", "X-Ray"], "timestamp": datetime.now().isoformat()},
    consults={"value": {
        "Cardiology": (
            "ECG will be read as STEMI in leads V1-V6 and leads I and AVL. Cardiology will recommend preparing the patient for cardiac catheterization: "
            "aspirin, Plavix, heparin, and '... if it’s safe in light of the patient’s vital signs,' B-blocker and nitroglycerin. Indicate that the catheterization "
            "team will need about 20 minutes to get in and that the patient must be stabilized prior to catheterization."
        ),
        "Radiology": "CXR shows diffuse pulmonary edema consistent with congestive heart failure."
    }, "timestamp": datetime.now().isoformat()},
    vitals={"value": {"HR": 110, "BP": "88/60", "Temperature": 37.5, "O2 Sats": 92, "RR": 24}, "timestamp": datetime.now().isoformat()}
)

# Example of adding a new set of physical exam findings
case_example.update_dynamic_data('physical_exam', {
    "GENERAL": "A&OX3, moderate distress",
    "HEENT": "PERRL/EOMI",
    "NECK": "Supple, no JVD",
    "CV": "2/6 systolic apical murmur, tachycardia",
    "PULM": "Diffuse rales all lung fields",
    "ABD": "Soft, NT/ND, + BS",
    "EXT": "No C/C/E, palpable pulses all extremities",
    "NEURO": "WNL, MAE X 4, grossly intact"
})

# Adding another set of physical exam findings
case_example.update_dynamic_data('physical_exam', {
    "GENERAL": "A&OX3, mild distress",
    "HEENT": "PERRL/EOMI",
    "NECK": "Supple, no JVD",
    "CV": "1/6 systolic apical murmur, regular rhythm",
    "PULM": "Clear to auscultation bilaterally",
    "ABD": "Soft, NT/ND, + BS",
    "EXT": "No C/C/E, palpable pulses all extremities",
    "NEURO": "WNL, MAE X 4, grossly intact"
})