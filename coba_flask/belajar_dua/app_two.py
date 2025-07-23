from flask import Flask, redirect

app=Flask(__name__)


@app.route("/admin")
def hello_admin():
    return "<h1>Hello Admin</h1>"


if  __name__ == "__main__":
    app.run(debug=True)
