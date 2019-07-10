# coding: utf-8
import os
from flask import (
    Flask, request, current_app, send_from_directory, render_template
)

app = Flask("n")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT, 'media_files')


@app.route("/noticias/cadastro", methods=["GET", "POST"])
def cadastro():
    return render_template('cadastro.html', title=u"Inserir nova noticia")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    return render_template('noticia.html', noticia=noticia)


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)