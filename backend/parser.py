import re
from typing import Dict, Any
from abbreviation_engine import expand_abbreviations, get_timing_instructions

def parse_prescription(text: str) -> Dict[str, Any]:
    """
    Parses a raw medical prescription string into structured components.
    Example: "Tab Paracetamol 500mg BD x 5 days"
    """
    
    # Initialize defaults
    structured_data = {
        "medicine": "Unknown",
        "dosage": "Not specified",
        "frequency": "Not specified",
        "timing": "Not specified",
        "duration": "Not specified",
        "instructions": "Follow doctor's advice"
    }

    original_text = text.strip()
    if not original_text:
        return {"error": "Empty prescription text."}

    # 1. Expand Abbreviations for the Simple Explanation Output
    expanded_text = expand_abbreviations(original_text)
    
    # 2. Extract Duration (e.g., "x 5 days", "for 1 week", "* 5 days")
    duration_match = re.search(r'(?:x|times|\*|for)\s*(\d+\s*(?:days|day|weeks|week|months|month))', original_text, re.IGNORECASE)
    if duration_match:
        structured_data["duration"] = duration_match.group(1).strip()
        
    # 3. Extract Medicine Name and Form (e.g., "Tab Paracetamol", "Syr CoughSyrup")
    # Matches patterns starting with typical medicine forms and captures words until a number (dosage) is found.
    form_rx = r'\b(Tab|Cap|Syr|Inj|Oint|Crm|Gtt)\b'
    
    # Try to find the form (tablet, syrup, etc)
    form_match = re.search(form_rx, original_text, re.IGNORECASE)
    
    # Try to find dosage (numbers followed by mg, ml, g, mcg)
    dosage_rx = r'(\d+(?:\.\d+)?\s*(?:mg|ml|mcg|g|ui|iu))'
    dosage_match = re.search(dosage_rx, original_text, re.IGNORECASE)
    
    if dosage_match:
        structured_data["dosage"] = dosage_match.group(1).strip()
        
    # Identify the medicine name boundary based on form and dosage
    if form_match and dosage_match:
        # Extract everything between form and dosage
        start_idx = form_match.end()
        end_idx = dosage_match.start()
        med_name = original_text[start_idx:end_idx].strip()
        
        # Format the full medicine name (e.g., Paracetamol 500mg)
        full_name = f"{med_name}".strip()
        # Ensure we capture cases with no explicit form keyword correctly below
        if full_name:
            structured_data["medicine"] = f"{full_name} {structured_data['dosage']}".strip()
    elif form_match and not dosage_match:
         # Form found but no dosage, assume next words are medicine.
         # For simplicity in rule-based: take next 1-2 words.
         parts = original_text[form_match.end():].split()
         if parts:
             structured_data["medicine"] = f"{parts[0]}".strip()
    elif not form_match and dosage_match:
         # No explicit form, but dosage found. Target words before dosage.
         parts = original_text[:dosage_match.start()].split()
         if parts:
             # Just grab the last word or two before dosage as medicine name
             structured_data["medicine"] = " ".join(parts[-2:]).strip() + f" {structured_data['dosage']}"
    else:
        # Fallback if neither form nor dosage matched cleanly
        parts = original_text.split()
        if len(parts) >= 2:
            structured_data["medicine"] = f"{parts[0]} {parts[1]}"
            

    # 4. Extract Frequency and Timing and Instructions
    freq, timing, instr = get_timing_instructions(original_text)
    if freq: structured_data["frequency"] = freq
    if timing: structured_data["timing"] = timing
    if instr: structured_data["instructions"] = instr

    return structured_data

def generate_simple_explanation(structured_data: Dict[str, Any]) -> str:
    """Combines structured data into a human-readable sentence."""
    if "error" in structured_data:
        return "Could not understand the prescription format."

    med = structured_data.get("medicine", "the medicine")
    freq = structured_data.get("frequency", "as directed").lower()
    dur = structured_data.get("duration", "treatment period")
    tim = structured_data.get("timing", "appropriate times").lower()
    ins = structured_data.get("instructions", "").lower()
    
    explanation = f"Take {med} {freq} for {dur}."
    
    details = []
    if tim != "not specified":
        details.append(f"specifically in the {tim}")
    if ins and ins != "follow doctor's advice":
        # Remove 'take ' if it exists so it flows better
        clean_ins = ins.replace("take ", "")
        details.append(f"and remember to {ins}")
        
    if details:
        explanation += " " + ", ".join(details).capitalize() + "."
        
    return explanation.strip()

# Quick manual test if run directly
if __name__ == "__main__":
    sample = "Tab Paracetamol 500mg BD x 5 days PC"
    print(f"Input: {sample}")
    data = parse_prescription(sample)
    print(f"Parsed: {data}")
    print(f"Explanation: {generate_simple_explanation(data)}")
