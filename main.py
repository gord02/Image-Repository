import mongoengine
from mongoengine import *
from flask import (Flask, render_template, request, send_file)

from mongoengine import connect
from schema import Image

import json
import io
from base64 import b64encode

# allows use to add to the database in mongoDB called covid-checkin
connect(db='imageRepo')

app = Flask("__main__")

@app.route("/")
def my_index():
    # obj = Image.objects(title='cat.jpg').first()
    # objs = Image.objects()
    # # print(objs, type(objs))
    # json_data = objs.to_json()
    # dicts = json.loads(json_data)
    # print(dicts, type(dicts))
    # # pic= obj.photo.read()
    # print("0: ", dicts[0])
    # print("photo: ", dicts[0]['photo'], type(dicts[0]['photo']) )
    # pic=dicts[0].photo.read()
    # print("pic: ", pic)

    # print(dicts[0])
    # List =[]
    # List.append(dicts[0])
    # print(List, type(List))
    pics=[]
    objs = Image.objects()
    for x in objs:
        # print(x)
        pics.append(x.photo.read())
    # print("pics: ", pics)
    images=[]
    for x in pics:
        images.append(b64encode(x).decode("utf-8"))


    # json= objs.to_json()
    # print("json: ", json)

    # obj = Image.objects(title='cat.jpg').first()
    # "$regex": "Alex"
    # pic= obj.photo.read()
    # # pic= obj.picutre.read()
    # # decoding bytes
    # image = b64encode(pic).decode("utf-8")
    # # print(type(image), "image: ", image)
    # return render_template("index.html", image= image)
    return render_template("allImages.html", images=images)

@app.route("/add")
def addImage():
    return render_template("form.html")


@app.route("/search")
def search():
    # obj = Image.objects(title='cat.jpg').first()
    obj = Image.objects(title='cat').first()
    pic= obj.photo.read()
    # decoding bytes
    image = b64encode(pic).decode("utf-8")
    # print(type(image), "image: ", image)
    return render_template("index.html", image= image)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'ok'
app.run(debug=True)
