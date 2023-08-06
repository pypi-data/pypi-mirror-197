

def is_paywalled(*, text: str) -> bool:
    """
    attempts to detect paywall by looking for certain strings
    in the text body of the article
    :param text: text body of article
    :return: True if paywall detected, False if unknown
    """
    if "are you a robot" in text.lower():
        return True
    if "please verify you're not a robot" in text.lower():
        return True
    if "what is included in my trial?" in text.lower():
        return True
    return False
