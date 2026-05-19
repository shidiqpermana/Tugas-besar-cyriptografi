from flask import Flask, render_template, request, session
import secrets

from ciphers.caesar import caesar_encrypt_with_steps
from ciphers.vigenere import vigenere_encrypt_with_steps
from ciphers.affine import affine_encrypt_with_steps
from ciphers.hill import hill_encrypt_with_steps
from ciphers.playfair import playfair_encrypt_with_steps

app = Flask(__name__)
app.secret_key = "cipher_lab_secret_key" # Replace with a real secret in production

def add_to_history(algorithm, input_text, key_used, result_text):
    if 'history' not in session:
        session['history'] = []
    
    history = session['history']
    history.insert(0, {
        'algorithm': algorithm,
        'input': input_text[:20] + ('...' if len(input_text) > 20 else ''),
        'key': str(key_used),
        'result': result_text[:20] + ('...' if len(result_text) > 20 else '')
    })
    session['history'] = history[:5]


@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize context with default values for all forms
    context = {
        "active_tab": "",
        "c_input_text": "", "c_shift": 3, "c_result_text": "", "c_steps": [],
        "v_input_text": "", "v_key": "", "v_result_text": "", "v_steps": [], "v_error": "",
        "a_input_text": "", "a_key_a": 5, "a_key_b": 8, "a_result_text": "", "a_steps": [], "a_error": "",
        "h_input_text": "", "h_matrix_size": 2, "h_matrix_keys_dict": {}, "h_result_text": "", "h_steps": [], "h_error": "",
        "p_input_text": "", "p_key": "", "p_result_text": "", "p_steps": [], "p_matrix": [], "p_error": ""
    }

    if request.method == "POST":
        action = request.form.get("action")
        context["active_tab"] = action

        if action == "caesar":
            input_text = request.form.get("c_input_text", "")
            shift = int(request.form.get("c_shift", 0))
            result_text, steps = caesar_encrypt_with_steps(input_text, shift)
            add_to_history("Caesar", input_text, f"Shift: {shift}", result_text)
            context["c_input_text"] = input_text
            context["c_shift"] = shift
            context["c_result_text"] = result_text
            context["c_steps"] = steps

        elif action == "vigenere":
            input_text = request.form.get("v_input_text", "")
            key = request.form.get("v_key", "")
            context["v_input_text"] = input_text
            context["v_key"] = key
            try:
                result_text, steps = vigenere_encrypt_with_steps(input_text, key)
                add_to_history("Vigenere", input_text, key, result_text)
                context["v_result_text"] = result_text
                context["v_steps"] = steps
            except ValueError as error:
                context["v_error"] = str(error)

        elif action == "affine":
            input_text = request.form.get("a_input_text", "")
            key_a = int(request.form.get("a_key_a", 5))
            key_b = int(request.form.get("a_key_b", 8))
            context["a_input_text"] = input_text
            context["a_key_a"] = key_a
            context["a_key_b"] = key_b
            try:
                result_text, steps = affine_encrypt_with_steps(input_text, key_a, key_b)
                add_to_history("Affine", input_text, f"a={key_a}, b={key_b}", result_text)
                context["a_result_text"] = result_text
                context["a_steps"] = steps
            except ValueError as error:
                context["a_error"] = str(error)

        elif action == "hill":
            input_text = request.form.get("h_input_text", "")
            matrix_size = int(request.form.get("h_matrix_size", 2))
            
            matrix_key = []
            matrix_keys_dict = {}
            for i in range(matrix_size):
                row = []
                for j in range(matrix_size):
                    key_name = f"k_{i}_{j}"
                    val = int(request.form.get(key_name, 0))
                    row.append(val)
                    matrix_keys_dict[key_name] = val
                matrix_key.append(row)
                
            context["h_input_text"] = input_text
            context["h_matrix_size"] = matrix_size
            context["h_matrix_keys_dict"] = matrix_keys_dict
            
            try:
                result_text, steps = hill_encrypt_with_steps(input_text, matrix_key)
                add_to_history("Hill", input_text, f"Matrix {matrix_size}x{matrix_size}", result_text)
                context["h_result_text"] = result_text
                context["h_steps"] = steps
            except ValueError as error:
                context["h_error"] = str(error)

        elif action == "playfair":
            input_text = request.form.get("p_input_text", "")
            key = request.form.get("p_key", "")
            context["p_input_text"] = input_text
            context["p_key"] = key
            try:
                result_text, steps, matrix = playfair_encrypt_with_steps(input_text, key)
                add_to_history("Playfair", input_text, key, result_text)
                context["p_result_text"] = result_text
                context["p_steps"] = steps
                context["p_matrix"] = matrix
            except ValueError as error:
                context["p_error"] = str(error)

    return render_template("home.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
