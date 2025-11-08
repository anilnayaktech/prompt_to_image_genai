# scripts/safety.py

def is_safe_prompt(prompt: str) -> bool:
    """
    Simple content safety filter to block NSFW or harmful prompts.
    (You can extend this list later.)
    """
    banned_words = ["nude", "blood", "kill", "weapon", "violence", "sex", "nsfw"]
    for word in banned_words:
        if word.lower() in prompt.lower():
            return False
    return True
