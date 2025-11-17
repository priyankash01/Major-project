from typing import List


CRISIS_KEYWORDS: List[str] = [
    "suicidal", "suicide", "kill myself", "want to die", "hopeless", "worthless",
    "can't go on", "give up", "ending it all", "no reason to live"
]

SAFETY_MESSAGE =(
    "It sounds like you're going through a really tough time."
    "You're not alone, and there are people who want to help you."
    "Please consider reaching out to a mental health professional or contacting a helpline: \n\n"
    "***India: 9152987821 (iCall), 1800-599-0019 (Vandrevala Foundation)\n"
    "**USA:** 988 (Suicide & Crisis Lifeline)\n"        
    "**UK:** 116 123 (Samaritans)\n\n"
    "You Matter. 🫀"                   
)

def contains_crisis_keywords(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CRISIS_KEYWORDS)
