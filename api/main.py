from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World! I love my mom and my dad</p>"


app.run(debug=True, host="0.0.0.0", port=5000)
