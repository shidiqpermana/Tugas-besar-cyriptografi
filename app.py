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



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/caesar", methods=["GET", "POST"])
def caesar_page():
    context = {"input_text": "", "shift": 3, "result_text": "", "steps": []}
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        shift = int(request.form.get("shift", 0))
        result_text, steps = caesar_encrypt_with_steps(input_text, shift)
        add_to_history("Caesar", input_text, f"Shift: {shift}", result_text)
        context.update(
            {
                "input_text": input_text,
                "shift": shift,
                "result_text": result_text,
                "steps": steps,
            }
        )
    return render_template("caesar.html", **context)


@app.route("/vigenere", methods=["GET", "POST"])
def vigenere_page():
    context = {
        "input_text": "",
        "key": "",
        "result_text": "",
        "steps": [],
        "error_message": "",
    }
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        key = request.form.get("key", "")
        context["input_text"] = input_text
        context["key"] = key
        try:
            result_text, steps = vigenere_encrypt_with_steps(input_text, key)
            add_to_history("Vigenere", input_text, key, result_text)
            context["result_text"] = result_text
            context["steps"] = steps
        except ValueError as error:
            context["error_message"] = str(error)
    return render_template("vigenere.html", **context)


@app.route("/affine", methods=["GET", "POST"])
def affine_page():
    context = {
        "input_text": "",
        "key_a": 5,
        "key_b": 8,
        "result_text": "",
        "steps": [],
        "error_message": "",
    }
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        key_a = int(request.form.get("key_a", 5))
        key_b = int(request.form.get("key_b", 8))
        context["input_text"] = input_text
        context["key_a"] = key_a
        context["key_b"] = key_b
        try:
            result_text, steps = affine_encrypt_with_steps(input_text, key_a, key_b)
            add_to_history("Affine", input_text, f"a={key_a}, b={key_b}", result_text)
            context["result_text"] = result_text
            context["steps"] = steps
        except ValueError as error:
            context["error_message"] = str(error)
    return render_template("affine.html", **context)


@app.route("/hill", methods=["GET", "POST"])
def hill_page():
    context = {
        "input_text": "",
        "matrix_size": 2,
        "matrix_keys_dict": {},
        "result_text": "",
        "steps": [],
        "error_message": "",
    }
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        matrix_size = int(request.form.get("matrix_size", 2))
        
        # Reconstruct matrix
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
            
        context["input_text"] = input_text
        context["matrix_size"] = matrix_size
        context["matrix_keys_dict"] = matrix_keys_dict
        
        try:
            result_text, steps = hill_encrypt_with_steps(input_text, matrix_key)
            add_to_history("Hill", input_text, f"Matrix {matrix_size}x{matrix_size}", result_text)
            context["result_text"] = result_text
            context["steps"] = steps
        except ValueError as error:
            context["error_message"] = str(error)
            
    return render_template("hill.html", **context)


@app.route("/playfair", methods=["GET", "POST"])
def playfair_page():
    context = {
        "input_text": "",
        "key": "",
        "result_text": "",
        "steps": [],
        "matrix": [],
        "error_message": "",
    }
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        key = request.form.get("key", "")
        context["input_text"] = input_text
        context["key"] = key
        try:
            result_text, steps, matrix = playfair_encrypt_with_steps(input_text, key)
            add_to_history("Playfair", input_text, key, result_text)
            context["result_text"] = result_text
            context["steps"] = steps
            context["matrix"] = matrix
        except ValueError as error:
            context["error_message"] = str(error)
    return render_template("playfair.html", **context)


@app.route("/railfence")
def railfence_page():
    return render_template("coming_soon.html", algorithm_name="Rail Fence Cipher")


@app.route("/transposition")
def transposition_page():
    return render_template("coming_soon.html", algorithm_name="Columnar Transposition")


if __name__ == "__main__":
    app.run(debug=True)
