from flask import Flask,render_template

app=Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def tugasSatu():
    return render_template('index_tugas_1.html')

@app.route("/coba")
def coba():
    return "coba saja"

@app.route("/hot-reload")
def hot():
    return "coba berubah"

@app.route("/tugas-2")
def tugasDua():
    return render_template('index_tugas_2.html')


if  __name__ == "__main__":
    app.run(debug=True)
