from flask import Flask, send_from_directory, redirect, url_for,render_template

from loader.loader import loader
from main.main import main

app = Flask(__name__)
app.secret_key = "som_key"

app.register_blueprint(loader, url_prefix='/loader')
app.register_blueprint(main, url_prefix='/main')


@app.route("/")
def page_index():
    return redirect(url_for("main.index"))


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)

app.run()
