"""Caesar cipher logic module."""


def _shift_char(char: str, shift: int) -> str:
    if not char.isalpha():
        return char

    base = ord("A") if char.isupper() else ord("a")
    normalized = ord(char) - base
    shifted = (normalized + shift) % 26
    return chr(base + shifted)


def caesar_encrypt_with_steps(text: str, shift: int) -> tuple[str, list[dict]]:
    """Encrypt text with Caesar cipher and return detailed per-char steps."""
    result_chars: list[str] = []
    steps: list[dict] = []

    normalized_shift = shift % 26
    for index, char in enumerate(text):
        encrypted_char = _shift_char(char, normalized_shift)
        result_chars.append(encrypted_char)

        step = {
            "index": index,
            "original": char,
            "shift": normalized_shift,
            "result": encrypted_char,
            "is_alpha": char.isalpha(),
        }
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            step["formula"] = f"({ord(char) - base} + {normalized_shift}) mod 26 = {ord(encrypted_char) - base}"
        else:
            step["formula"] = "Non-huruf, karakter tidak diubah."
        steps.append(step)

    return "".join(result_chars), steps
