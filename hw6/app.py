from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        message_id = request.form["message_id"]
        output = subprocess.run(
            ["python3", "main.py", message_id], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")

    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run()
