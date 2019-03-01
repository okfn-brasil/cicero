import unicodedata


def normalize(text):
    if not text:
        return ""

    chars = (
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    return "".join(chars)
