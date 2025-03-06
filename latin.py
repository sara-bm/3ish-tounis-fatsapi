# Dictionnaire de translittération latine vers arabe
latin_to_arabic = {
    "a": "ا", "b": "ب", "te": "ت", "th": "ث", "j": "ج", "7": "ح", "kh": "خ",
    "d": "د", "dh": "ذ", "r": "ر", "z": "ز", "s": "س", "ch": "ش",
    "sa": "ص", "D": "ض", "t": "ط", "Z": "ظ", "3": "ع", "gh": "غ",
    "f": "ف", "9": "ق", "k": "ك", "l": "ل", "m": "م", "n": "ن",
    "h": "ه", "w": "و", "y": "ي", "ou": "و", "i": "ي","5":"خ"
}
 
# Fonction de conversion
def latin_to_arabic_text(text):
    arabic_word = ""
    i = 0
    while i < len(text):
        # Vérifier les lettres doubles comme "ch", "kh", "th", "sa", "gh", "dh"
        if i < len(text) - 1 and text[i:i+2].lower() in latin_to_arabic:
            arabic_char = latin_to_arabic[text[i:i+2].lower()]
            arabic_word += arabic_char if text[i:i+2].islower() else arabic_char.upper()
            i += 2  # Sauter deux lettres
        elif text[i].lower() in latin_to_arabic:
            arabic_char = latin_to_arabic[text[i].lower()]
            arabic_word += arabic_char if text[i].islower() else arabic_char.upper()
            i += 1
        else:
            arabic_word += text[i]  # Conserver les caractères inconnus (espaces, ponctuation, etc.)
            i += 1
    return arabic_word
 
# # Exemple d'utilisation
# latin_word = "Wjhk tetb3 f Flous f teouns"
# arabic_word = latin_to_arabic_text(latin_word)
# print(arabic_word)  # Résultat attendu : "وجهك تطبع ف فلوس"
 
 # Dictionary for Arabic to Latin transliteration (reversed from your original)
arabic_to_latin = {
    "ا": "a", "ب": "b", "ت": "te","ة":"ta", "ث": "th", "ج": "j", "ح": "7", "خ": "kh",
    "د": "d", "ذ": "dh", "ر": "r", "ز": "z", "س": "s", "ش": "ch",
    "ص": "sa", "ض": "D", "ط": "t", "ظ": "Z", "ع": "3", "غ": "gh",
    "ف": "f", "ق": "9", "ك": "k", "ل": "l", "م": "m", "ن": "n",
    "ه": "h", "و": "w", "ي": "y"  # Note: "ou" and "i" mapped to "و" and "ي" removed to avoid ambiguity
}

def arabic_to_latin_text(text):
    latin_word = ""
    for char in text:
        # Convert Arabic character to Latin if it exists in the dictionary
        if char in arabic_to_latin:
            latin_word += arabic_to_latin[char]
        else:
            # Keep non-mapped characters (spaces, punctuation, etc.) as is
            latin_word += char
    return latin_word

# # Example usage
# arabic_text = "وجهك تطبع ف فلوس"
# latin_text = arabic_to_latin_text(arabic_text)
# print(latin_text)  # Expected output: "wjhk tetb3 f flws"

# # More test cases
# test_cases = [
#     "هاني لهنا برك ما عندي برشة بش نفرطرها",
# ]
# for test in test_cases:
#     print(f"Arabic: {test} -> Latin: {arabic_to_latin_text(test)}")