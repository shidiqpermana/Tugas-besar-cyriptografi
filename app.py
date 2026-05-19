from flask import Flask, render_template, request

from ciphers.caesar import caesar_encrypt_with_steps
from ciphers.vigenere import vigenere_encrypt_with_steps
from ciphers.affine import affine_encrypt_with_steps
from ciphers.hill import hill_encrypt_with_steps

app = Flask(__name__)


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
            context["result_text"] = result_text
            context["steps"] = steps
        except ValueError as error:
            context["error_message"] = str(error)
            
    return render_template("hill.html", **context)


@app.route("/playfair")
def playfair_page():
    return render_template("coming_soon.html", algorithm_name="Playfair Cipher")


@app.route("/railfence")
def railfence_page():
    return render_template("coming_soon.html", algorithm_name="Rail Fence Cipher")


@app.route("/transposition")
def transposition_page():
    return render_template("coming_soon.html", algorithm_name="Columnar Transposition")


if __name__ == "__main__":
    app.run(debug=True)
