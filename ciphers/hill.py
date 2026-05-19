import numpy as np
import math

def hill_encrypt_with_steps(text, matrix_key):
    """
    Encrypts text using the Hill Cipher and returns the result and step-by-step breakdown.
    Requires numpy.
    """
    # matrix_key is expected to be a 2D list or numpy array
    matrix_key = np.array(matrix_key)
    n = len(matrix_key)
    
    # Validate the matrix
    det = int(round(np.linalg.det(matrix_key)))
    det_mod_26 = det % 26
    if det_mod_26 == 0 or math.gcd(det_mod_26, 26) != 1:
        raise ValueError("Matriks kunci tidak valid (determinannya tidak koprima dengan 26). Matriks ini tidak dapat diinvers modulo 26, silakan gunakan matriks lain.")
        
    # Clean the text (only alphabets, uppercase)
    clean_text = "".join([c.upper() for c in text if c.isalpha()])
    
    # Pad if necessary with 'X'
    pad_len = (n - len(clean_text) % n) % n
    clean_text += "X" * pad_len
    
    result_text = ""
    steps = []
    
    # Keep track of original text format (spaces, etc)? The user usually expects cleaned text for block ciphers like Hill.
    # To keep things straightforward and correct mathematically, we just output the cleaned & padded encrypted text.
    
    for i in range(0, len(clean_text), n):
        block = clean_text[i:i+n]
        p_vector = np.array([[ord(c) - ord("A")] for c in block])
        
        # Calculate C = (K * P) mod 26
        c_vector = np.dot(matrix_key, p_vector)
        c_vector_mod = c_vector % 26
        
        # Build block result
        block_result = "".join([chr(c[0] + ord("A")) for c in c_vector_mod])
        result_text += block_result
        
        # Generate educative step string for matrix multiplication
        matrix_str = "\\begin{bmatrix} " + " \\\\ ".join([" & ".join([str(val) for val in row]) for row in matrix_key]) + " \\end{bmatrix}"
        p_str = "\\begin{bmatrix} " + " \\\\ ".join([str(val[0]) for val in p_vector]) + " \\end{bmatrix}"
        c_str = "\\begin{bmatrix} " + " \\\\ ".join([str(val[0]) for val in c_vector_mod]) + " \\end{bmatrix}"
        
        # Detail step for multiplication
        mult_details = []
        for row_idx, row in enumerate(matrix_key):
            row_mult = []
            for col_idx, val in enumerate(row):
                row_mult.append(f"{val}({p_vector[col_idx][0]})")
            row_sum = sum(val * p_vector[col_idx][0] for col_idx, val in enumerate(row))
            mult_details.append(f"{' + '.join(row_mult)} = {row_sum} \\equiv {c_vector_mod[row_idx][0]} \\pmod{{26}}")
            
        details_str = " \\\\ ".join(mult_details)
        
        formula = f"""
\\begin{{aligned}}
\\text{{Blok: }} & \\text{{{block}}} \\rightarrow {p_str} \\\\
C &= K \\cdot P \\pmod{{26}} \\\\
C &= {matrix_str} \\cdot {p_str} \\pmod{{26}} \\\\
C &= \\begin{{bmatrix}} {details_str} \\end{{bmatrix}} \\\\
C &\\equiv {c_str} \\pmod{{26}} \\rightarrow \\text{{{block_result}}}
\\end{{aligned}}
        """
        
        steps.append({
            "block": block,
            "block_result": block_result,
            "formula": formula
        })
        
    return result_text, steps
