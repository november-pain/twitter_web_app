from flask import Flask, render_template, request
from twitter_web_app import main

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def enter():
    if request.method == 'POST':
        acc = request.form["username"]
        number = request.form["num_friends"]

        son_jey = main(acc, number)
        return son_jey
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)