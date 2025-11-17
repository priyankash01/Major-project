import sys
import time

# Try to import transformers pipeline
try:
    from transformers import pipeline
    try:
        sentiment_analyzer = pipeline("sentiment-analysis")
    except Exception as e:
        print("Model download/load error:", e)
        sentiment_analyzer = None
except Exception:
    sentiment_analyzer = None

# Fallback simple lists if model not available
POS_WORDS = ["happy","good","great","fine","relieved","better","okay","joy","love"]
NEG_WORDS = ["sad","depressed","anxious","anxiety","stressed","angry","hurt","lonely","tired","hopeless"]

CRISIS_KEYWORDS = [
    "suicide","kill myself","end my life","want to die","die","kill me",
    "hurt myself","self-harm","cut myself","hang myself","i can't go on",
    "i am done","i want to die"
]

PHQ9_QUESTIONS = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
    "Trouble concentrating on things, such as reading or watching television?",
    "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so restless that you’ve been moving around a lot more?",
    "Thoughts that you would be better off dead or of hurting yourself in some way?"
]

def lower_contains_any(text, patterns):
    t = text.lower()
    for p in patterns:
        if p in t:
            return True
    return False

def simple_sentiment(text):
    t = text.lower()
    pos = sum(1 for w in POS_WORDS if w in t)
    neg = sum(1 for w in NEG_WORDS if w in t)
    if pos > neg:
        return {"label": "POSITIVE", "score": 0.8}
    if neg > pos:
        return {"label": "NEGATIVE", "score": 0.8}
    return {"label": "NEUTRAL", "score": 0.6}

def analyze_sentiment(text):
    # First check crisis keywords
    if lower_contains_any(text, CRISIS_KEYWORDS):
        return {"crisis": True, "label": "CRISIS", "score": 1.0}
    # Try model
    if sentiment_analyzer is not None:
        try:
            res = sentiment_analyzer(text[:512])[0]
            return {"crisis": False, "label": res.get("label","NEUTRAL"), "score": res.get("score",0.0)}
        except Exception:
            pass
    # Fallback
    res = simple_sentiment(text)
    return {"crisis": False, "label": res["label"], "score": res["score"]}

def crisis_response():
    msg = (
        "\n💙 I’m really sorry that you're feeling this way. "
        "If you are in immediate danger, please call your local emergency number right now.\n"
        "You are not alone — reaching out to a trusted friend, family member, or a mental health professional could really help.\n"
        "I’m here to listen. Would you like me to share some calming exercises or helpline resources?\n"
    )
    return msg

def empathetic_reply(label, score):
    if label == "POSITIVE":
        return "That's wonderful to hear! 🌸 If you’d like, we can talk more."
    elif label == "NEGATIVE":
        return "I'm sorry you're going through this. 💙 Would you like to try a short breathing exercise or a PHQ-9 check?"
    else:
        return "Thanks for opening up. I'm here to listen — share whatever’s on your mind."

def run_phq9():
    print("\nPHQ-9 Screening: For each question enter 0 (Not at all), 1 (Several days), 2 (More than half the days), 3 (Nearly every day).")
    total = 0
    for i, q in enumerate(PHQ9_QUESTIONS, start=1):
        while True:
            try:
                ans = input(f"{i}. {q}\nYour answer (0-3): ").strip()
                if ans.lower() in ["exit","quit"]:
                    print("Exiting PHQ-9.")
                    return None
                val = int(ans)
                if 0 <= val <= 3:
                    total += val
                    break
            except ValueError:
                pass
            print("Please enter a number 0, 1, 2, or 3 (or type exit).")
    # interpret score
    print("\nCalculating score...")
    time.sleep(0.8)
    print("PHQ-9 total score:", total)
    if total <= 4:
        level = "Minimal or none (0-4)"
    elif total <= 9:
        level = "Mild (5-9)"
    elif total <= 14:
        level = "Moderate (10-14)"
    elif total <= 19:
        level = "Moderately severe (15-19)"
    else:
        level = "Severe (20-27)"
    print("Interpretation:", level)
    print("\nNote: This is not a diagnosis. It's a screening tool to help identify if further evaluation by a professional might be useful.")
    return total

def chat_loop():
    print("\nYou can type 'menu' to return, or 'exit' to quit.")
    while True:
        user = input("\nYou: ").strip()
        if not user:
            continue
        if user.lower() in ["exit","quit"]:
            print("MindSync: Take care 💙 Remember, if you're in danger, contact emergency services.")
            return
        if user.lower() == "menu":
            return
        # Analyze
        res = analyze_sentiment(user)
        if res.get("crisis"):
            print("\nMindSync:", crisis_response())
            continue
        # normal reply
        reply = empathetic_reply(res["label"], res["score"])
        print("\nMindSync:", reply)

def main():
    print("🧠 Welcome to MindSync (Console Prototype)")
    print("Type 'menu' anytime to return, or 'exit' to quit.\n")
    if sentiment_analyzer is None:
        print("Note: Sentiment model not loaded. Using simple keyword fallback. (First run may download a model and take time.)\n")
    while True:
        print("\nMenu:")
        print("1) Chat with MindSync")
        print("2) Take PHQ-9 screening")
        print("3) Exit")
        choice = input("Choose (1/2/3): ").strip()
        if choice == "1":
            chat_loop()
        elif choice == "2":
            run_phq9()
        elif choice == "3":
            print("Goodbye — take care 💙 If you are in immediate danger, please call emergency services.")
            break
        else:
            print("Please choose 1, 2 or 3.")

if __name__ == "__main__":
    main()
