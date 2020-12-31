import mongoengine
from mongoengine import *
from flask import (Flask, render_template, request, send_file)

from mongoengine import connect
from schema import Image

import json
import io
import base64
from base64 import b64encode

# allows use to add to the database in mongoDB called covid-checkin
connect(db='imageRepo')

app = Flask("__main__")

@app.route("/")
def allImages():

    Dict = {}
    # print("Dict: ", type(Dict))
    # {'key': 'value'}

    # pics=[]
    objs = Image.objects()
    jsonObj= objs.to_json()
    Json = json.loads(jsonObj)

    for x in objs:
        # data['a'] = 1
        Dict[x['_id']] = x['photo'].read()
    print (Dict)
    for x in Json:
        # using dictionary instead of list allows the photo to be attached to its id in the database
       
        # Dict[x._id] = (x['photo']).read()
        Dict[x._id] = (x['photo'].read())
        
        Dict[x._id] =  base64.b64encode(bytes(x['photo'], 'utf-8'))
        # pics.append(x.photo.read())
    images={}
    for x in Dict:
        images[x] = b64encode(Dict[x]).decode("utf-8")
        # images.append(b64encode(x).decode("utf-8"))
    # print("image: ", images[0], "====type: ", type(images[0]))
    print(images)
    return render_template("allImages.html", images=images)

@app.route("/", methods=['POST'])
def search():
    if request.method == "POST":
        title = request.form["searchValue"]
        print("title: ", title)

        Dict = {}
        objs = Image.objects.search_text(title)
        # objs = Image.objects()
        # print("obj: ", objs.to_json())

        for x in objs:
            # print(x)
            Dict[x._id] = Dict[x].photo.read()
            # pics.append(x.photo.read())
        # print("pics: ", pics)
        images={}
        for x in Dict:
            images[x] = b64encode(Dict[x]).decode("utf-8")
            # images.append(b64encode(x).decode("utf-8"))

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
    return render_template("show.html", images= images)

@app.route("/add")
def addImage():
    return render_template("form.html")
# combine routes, better namming
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

@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':
        image= request.form['delete']
        print("image: ", image)
    return render_template("search.html")




@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'ok'
app.run(debug=True)
