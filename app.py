from flask import Flask, render_template, request

from ciphers.caesar import caesar_encrypt_with_steps
from ciphers.vigenere import vigenere_encrypt_with_steps

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
