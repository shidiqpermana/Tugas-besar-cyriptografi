"""Vigenere cipher logic module."""


def _shift_alpha(char: str, shift: int) -> str:
    base = ord("A") if char.isupper() else ord("a")
    normalized = ord(char) - base
    shifted = (normalized + shift) % 26
    return chr(base + shifted)


def vigenere_encrypt_with_steps(text: str, key: str) -> tuple[str, list[dict]]:
    """Encrypt text with Vigenere cipher and return pairing process details."""
    if not key:
        raise ValueError("Kunci Vigenere tidak boleh kosong.")

    cleaned_key = "".join(char for char in key if char.isalpha())
    if not cleaned_key:
        raise ValueError("Kunci harus mengandung minimal satu huruf.")

    result_chars: list[str] = []
    steps: list[dict] = []
    key_index = 0

    for index, char in enumerate(text):
        if not char.isalpha():
            result_chars.append(char)
            steps.append(
                {
                    "index": index,
                    "plain_char": char,
                    "key_char": "-",
                    "key_shift": 0,
                    "result": char,
                    "formula": "Non-huruf, karakter tidak diubah.",
                }
            )
            continue

        current_key_char = cleaned_key[key_index % len(cleaned_key)]
        key_shift = ord(current_key_char.lower()) - ord("a")
        encrypted = _shift_alpha(char, key_shift)
        result_chars.append(encrypted)

        base = ord("A") if char.isupper() else ord("a")
        steps.append(
            {
                "index": index,
                "plain_char": char,
                "key_char": current_key_char.upper(),
                "key_shift": key_shift,
                "result": encrypted,
                "formula": f"({ord(char) - base} + {key_shift}) mod 26 = {ord(encrypted) - base}",
            }
        )
        key_index += 1

    return "".join(result_chars), steps
