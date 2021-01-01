import mongoengine
from mongoengine import *
from flask import (Flask, render_template, request, send_file)

from mongoengine import connect
from schema import Image

import json
import io
import base64
from base64 import b64encode

# to convert json object to object
from collections import namedtuple
from types import SimpleNamespace

# allows use to add to the database in mongoDB called covid-checkin
connect(db='imageRepo')

app = Flask("__main__")

@app.route("/")
def allImages():
    pics=[]
    objs = Image.objects()

    for x in objs:
        # print("1")
        obj = {
            'title': x.title,
            "description": x.description,
            "image": x.photo.read(),   
            "id": x.id
        }

        if(type(obj['image']) is not bytes):
            print("HERE")
            print(obj)
        else:
            # print("good")
            pics.append(obj)
        # pics.append(x.photo.read())

    # print(pics)

    images=[]

    for x in pics:
        # print("54: ", x.title)
        # print("55: ", type(x['image']))
        x['image']= b64encode(x['image']).decode("utf-8")
        # images.append(b64encode(x.image).decode("utf-8"))
        # objsJson['photo']= b64encode(x).decode("utf-8")
        # loaded['photo']= b64encode(x).decode("utf-8")
    # print("image: ", images[0], "====type: ", type(images[0]))
    # print("objsJson: ", objsJson, objsJson[0])
    # return render_template("allImages.html", images=images)
    return render_template("allImages.html", images=pics)

@app.route("/", methods=['POST'])
def search():
    if request.method == "POST":
        title = request.form["searchValue"]
        print("title: ", title)

        pics=[]
        objs = Image.objects.search_text(title)
        # objs = Image.objects()
        # print("obj: ", objs.to_json())

        for x in objs:
            # print(x)
            obj = {
                'title': x.title,
                "description": x.description,
                "image": x.photo.read(),   
                "id": x.id
            }
            if(type(obj['image']) is not bytes):
                print("HERE")
                print(obj)
            else:
                # print("good")
                pics.append(obj)
            # pics.append(x.photo.read())
        # print("pics: ", pics)
        images=[]
        for x in pics:
            # images.append(b64encode(x).decode("utf-8"))
            x['image']= b64encode(x['image']).decode("utf-8")

# ===============
        # obj = Image.objects.search_text(title).first()
        # obj = Image.objects.search_text(title).first()
        # # print("obj: ", obj.to_json())
        # pic= obj.photo.read()
        # # decoding bytes
        # image = b64encode(pic).decode("utf-8")
        # base64_bytes = image.encode('ascii')
# =============
    # print(type(image), "image: ", image)
    return render_template("show.html", images= pics)


@app.route("/add")
def addImage():
    return render_template("form.html")

@app.route("/add", methods=['POST'])
def addImagePost():
    if request.method == "POST":
        title = request.form["searchValue"]
        descriptiton = request.form["descriptiton"]
        file = request.files['file'].read()

        # picture =base64.b64encode(file)

        image = Image(title=title)
        image.description = descriptiton
        # fileHandle= open(file, "rb")
        image.photo.put(file, filename= (title+'.jpg'))
        # image.picture.put(open("Snake.jpg", "rb"))
        image.save()
    return "ok"

# @app.route("/")
# def searchForImage():

#     return render_template("search.html")




@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'ok'
app.run(debug=True)
