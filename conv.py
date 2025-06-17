import random

def random_text():
    responses = [
        "At your service, sir.",
        "Yes, I'm listening.",
        "Ready to go!",
        "Awaiting your command.",
        "Here I am, what can I do?",
        "All systems online.",
        "Just say the word, boss!"
    ]
    return random.choice(responses)
