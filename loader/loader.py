import os

from flask import Blueprint, render_template, request, flash, redirect, url_for

from utils import posts, allowed_extension, MyException
from utils import logging
loader = Blueprint("loader", __name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = "uploads/images"


@loader.route("/post", methods=["POST", "GET"])
def page_post_upload():
    if request.method == "GET":
        return render_template("post_form.html")
    elif request.method == "POST":
        picture = request.files.get("picture")
        content = request.form.get("content")
        if picture.filename and allowed_extension(picture.filename):
            img = os.path.join('..', UPLOAD_FOLDER, picture.filename)
            try:
                picture.save(os.path.join(UPLOAD_FOLDER, picture.filename))
                logging.info('изображение сохранено')
            except FileNotFoundError:
                logging.error('не удалось сохранить изображение')
                flash("не удалось сохранить изображение ")
                return redirect(url_for('loader.page_post_upload'))

            try:
                data = {'pic': img,
                        'content': content}
                posts.add_post(data)
                return render_template("post_uploaded.html", img=img, content=content)
            except MyException as exc:
                logging.error(exc)
                flash("Не удалось сохранить json файл ")
                return redirect(url_for('loader.page_post_upload'))
        else:
            flash("отсутствует изображение! Или неправильный формат! ")
            return redirect(url_for('loader.page_post_upload'))
