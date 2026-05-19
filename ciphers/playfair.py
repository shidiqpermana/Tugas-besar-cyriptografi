def generate_playfair_matrix(key):
    """Generates a 5x5 matrix for Playfair Cipher, combining I and J."""
    key = "".join([c.upper() for c in key if c.isalpha()])
    key = key.replace("J", "I")
    
    matrix_str = ""
    for char in key:
        if char not in matrix_str:
            matrix_str += char
            
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in matrix_str:
            matrix_str += char
            
    matrix = [list(matrix_str[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return -1, -1

def playfair_encrypt_with_steps(text, key):
    if not key:
        raise ValueError("Kunci Playfair tidak boleh kosong.")
        
    matrix = generate_playfair_matrix(key)
    
    # Process text
    clean_text = "".join([c.upper() for c in text if c.isalpha()])
    clean_text = clean_text.replace("J", "I")
    
    if not clean_text:
        return "", [], matrix
        
    digraphs = []
    i = 0
    while i < len(clean_text):
        char1 = clean_text[i]
        if i + 1 < len(clean_text):
            char2 = clean_text[i+1]
            if char1 == char2:
                # If same char, insert X
                char2 = 'X' if char1 != 'X' else 'Q'
                i += 1
            else:
                i += 2
        else:
            char2 = 'X' if char1 != 'X' else 'Q'
            i += 1
        digraphs.append(char1 + char2)
        
    result_text = ""
    steps = []
    
    for dig in digraphs:
        c1, c2 = dig[0], dig[1]
        r1, col1 = find_position(matrix, c1)
        r2, col2 = find_position(matrix, c2)
        
        rule = ""
        if r1 == r2:
            enc1 = matrix[r1][(col1 + 1) % 5]
            enc2 = matrix[r2][(col2 + 1) % 5]
            rule = "Baris Sama (geser kanan)"
        elif col1 == col2:
            enc1 = matrix[(r1 + 1) % 5][col1]
            enc2 = matrix[(r2 + 1) % 5][col2]
            rule = "Kolom Sama (geser bawah)"
        else:
            enc1 = matrix[r1][col2]
            enc2 = matrix[r2][col1]
            rule = "Persegi (tukar sudut kolom)"
            
        result_text += enc1 + enc2
        steps.append({
            "digraph": dig,
            "encrypted": enc1 + enc2,
            "rule": rule,
            "pos1": (r1, col1),
            "pos2": (r2, col2)
        })
        
    return result_text, steps, matrix
