from flask import Flask,render_template

app=Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/respon")
def respon():
    return render_template("respon.html")

if  __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
