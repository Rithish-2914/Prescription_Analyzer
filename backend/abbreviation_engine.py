import re

# Comprehensive mapping of common medical abbreviations
ABBREVIATIONS = {
    # Frequency
    "OD": "Once daily",
    "BD": "Twice daily",
    "BID": "Twice daily",  # Alternative for BD
    "TDS": "Three times daily",
    "TID": "Three times daily", # Alternative for TDS
    "QID": "Four times daily",
    "QDS": "Four times daily", # Alternative for QID
    "SOS": "Only when needed",
    "PRN": "As needed",
    "STAT": "Immediately",
    "Q4H": "Every 4 hours",
    "Q6H": "Every 6 hours",
    "Q8H": "Every 8 hours",
     
    # Timing / Food
    "HS": "Before sleeping",
    "BT": "Bedtime",
    "AC": "Before food",
    "PC": "After food",
    "BM": "Before meals", # Alternative for AC
    "AM": "Morning",
    "PM": "Evening",
    
    # Form/Route
    "TAB": "Tablet",
    "CAP": "Capsule",
    "SYR": "Syrup",
    "INJ": "Injection",
    "OINT": "Ointment",
    "CRM": "Cream",
    "GTT": "Drops",
    
    # Administration
    "PO": "By mouth",
    "IV": "Intravenous",
    "IM": "Intramuscular",
    "SC": "Subcutaneous",
    "TOP": "Topical"
}

def clean_text(text: str) -> str:
    """Cleans the input text by removing extra spaces and special chars (except those needed)."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def expand_abbreviations(text: str) -> str:
    """
    Replaces common abbreviations in the text with their full meanings.
    Case-insensitive replacement that preserves valid surrounding text.
    """
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    expanded_words = []
    
    for word in words:
        # Strip trailing punctuation for dictionary check
        clean_word = re.sub(r'[.,;:]+$', '', word).upper()
        if clean_word in ABBREVIATIONS:
            # Replace the word but keep trailing punctuation if any existed
            replacement = ABBREVIATIONS[clean_word]
            # Simple check to restore punctuation if needed, though usually medical lists don't mix them tightly
            original_punctuation = word[len(clean_word):] if len(word) > len(clean_word) else ""
            expanded_words.append(replacement + original_punctuation)
        else:
            expanded_words.append(word)
            
    return " ".join(expanded_words)

# Timing mappings used for structured generation based on specific keywords found
def get_timing_instructions(text: str) -> tuple[str, str, str]:
    """Extracts logical timing, frequency, and custom instructions based on matching tokens."""
    upper_text = text.upper()
    timing = ""
    frequency = ""
    instructions = ""
    
    # Frequency Logic (Prioritize common ones)
    if any(term in upper_text.split() for term in ["BD", "BID"]):
        frequency = "Twice daily"
        timing = "Morning and Evening"
    elif any(term in upper_text.split() for term in ["TDS", "TID"]):
        frequency = "Three times daily"
        timing = "Morning, Afternoon, and Evening"
    elif any(term in upper_text.split() for term in ["OD"]):
        frequency = "Once daily"
    elif any(term in upper_text.split() for term in ["QID", "QDS"]):
        frequency = "Four times daily"
    elif any(term in upper_text.split() for term in ["SOS", "PRN"]):
        frequency = "When needed"
        timing = "Varies"
        
    # Instruction Logic
    instruction_parts = []
    if any(term in upper_text.split() for term in ["AC", "BM"]):
        instruction_parts.append("Take before food")
    if any(term in upper_text.split() for term in ["PC"]):
        instruction_parts.append("Take after food")
    if any(term in upper_text.split() for term in ["HS", "BT"]):
        instruction_parts.append("Take before sleeping")
        timing = "Night" if not timing else timing + " (and Night)"
        
    if instruction_parts:
        instructions = " and ".join(instruction_parts)
    elif "after food" in text.lower():
         instructions = "Take after food"
    elif "before food" in text.lower():
         instructions = "Take before food"
        
    return frequency, timing, instructions
