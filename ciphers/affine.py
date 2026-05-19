import math

def affine_encrypt_with_steps(text, a, b):
    """
    Encrypts text using the Affine Cipher and returns the result and step-by-step breakdown.
    Formula: C = (a * P + b) mod 26
    """
    if math.gcd(a, 26) != 1:
        raise ValueError(f"Kunci 'a' ({a}) tidak koprima dengan 26. Nilai 'a' yang valid: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25.")

    result_text = ""
    steps = []

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            p = ord(char.upper()) - ord("A")
            c = (a * p + b) % 26
            c_char = chr(c + ord("A"))
            
            if not is_upper:
                c_char = c_char.lower()
                
            result_text += c_char
            
            steps.append({
                "char": char,
                "is_alpha": True,
                "p": p,
                "c": c,
                "c_char": c_char,
                "formula": rf"C = ({a} \cdot {p} + {b}) \pmod{{26}} = {(a * p + b)} \pmod{{26}} = {c}"
            })
        else:
            result_text += char
            steps.append({
                "char": char,
                "is_alpha": False
            })

    return result_text, steps
