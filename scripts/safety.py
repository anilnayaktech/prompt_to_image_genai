# # scripts/safety.py

# def is_safe_prompt(prompt: str) -> bool:
#     """
#     Simple content safety filter to block NSFW or harmful prompts.
#     (You can extend this list later.)
#     """
#     banned_words = ["nude", "blood", "kill", "weapon", "violence", "sex", "nsfw"]
#     for word in banned_words:
#         if word.lower() in prompt.lower():
#             return False
#     return True



#==================================================================================


# scripts/safety.py

def is_safe_prompt(prompt: str) -> bool:
    """
    Simple content safety filter to block NSFW or harmful prompts.
    Logs which banned word triggered the block.
    You can extend this list later.
    """
    banned_words = [
        "nude", "blood", "kill", "weapon", "violence", "sex", "nsfw",
        "gore", "murder", "suicide", "drugs"  # extra examples
    ]

    for word in banned_words:
        if word.lower() in prompt.lower():
            print(f"Safety filter triggered: found banned word '{word}' in prompt.")
            return False

    print("Prompt passed safety filter.")
    return True
