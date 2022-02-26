from flask import Blueprint, render_template, request, flash, redirect, url_for

from utils import posts

main = Blueprint('main', __name__, static_folder='static', template_folder='templates')


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/list", methods=['GET'])
def page_tag():
    search_string = request.args.get("s")
    if search_string:
        data = posts.get_post(search_string)
        if data:
            return render_template("post_list.html", data=data, search_string=search_string)
        else:
            flash(f"постов содержащих '{search_string}' не найдено!")
            return redirect(url_for("main.index"))
    else:
        flash("Введите критерий поиска")
        return redirect(url_for("main.index"))