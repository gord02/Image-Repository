import io
import json
import time
import base64 # WHICH ONE IS THIS
from base64 import b64encode # WHICH ONE IS THIS

#import mongoengine
# from mongoengine import *

import redis
from mongoengine import connect
from flask import (Flask, render_template, request, send_file, redirect)

from schema import Image
from decoder import decode_redis

"""
Comments:
1. remove unnecessary comments
2. Spacing on each side of equal sign, except for paramters
3. Declarative instatiation for lists and dictionary
4. Docstring comments python for each class and function
5. Add a space after commas
6. For routes, check for each type If GET, else if POST
    -> ELSE throw an error
7. consistent quotes
8. Better and more descriptive variable names
9. condense get and post routes into one, and log an error if not get/post go to catch all and log 'unexpected request'
10. Add line break before comment lines
11. Remove print statements
12. Add redis
"""

# allows use to add to the database in mongoDB called covid-checkin
connect(db='imageRepo')

app = Flask("__main__")

@app.route("/")
def allImages():
    images=[] # images = list()
    # Gets documents from Image collection
    objs = Image.objects()
    for x in objs:
        obj = {
            'title': x.title,
            "description": x.description,
            # reads image as binary
            "image": x.photo.read(),   
            "id": x.id
        }
        # allows only type bytes to be added to image list
        if(type(obj['image']) is not bytes):
            # flip order, log an error instead of throw
            print(obj)
        else:
            # converts bytes into base64 to be displayed in html
            obj['image']= b64encode(obj['image']).decode("utf-8")
            # pushes displayable images into list
            images.append(obj)
    # sends list of images to html
    return render_template("allImages.html", images=images)

@app.route("/", methods=['POST'])
def search():
    if request.method == "POST":
        title = request.form["searchValue"]
        images=[]
        objs = Image.objects.search_text(title)

        for x in objs:
            obj = {
                'title': x.title,
                "description": x.description,
                "image": x.photo.read(),   
                "id": x.id
            }
            if(type(obj['image']) is not bytes):
                # flip and log
                print(obj)
            else:
                obj['image']= b64encode(obj['image']).decode("utf-8")
                images.append(obj)

    return render_template("show.html", images= images)


@app.route("/add")
def addImage():
    return render_template("form.html")

@app.route("/add", methods=['POST'])
def addImagePost():
    if request.method == "POST":
        title = request.form["searchValue"]
        descriptiton = request.form["descriptiton"]
        file = request.files['file'].read()

        # creates a document for image in collection Image
        image = Image(title=title)
        image.description = descriptiton
        image.photo.put(file, filename= (title+'.jpg'))
        image.save()
    return redirect("/")

# WRONG, INCORRECT
@app.route("/image/<id>", methods=['GET'])
def individualImgae(id):

    """
    1. change naming
    """
    # THEORETICAL W REDIS
    # 1. Fetch redis with the ID
    # 2. If the image is there, then display that image / use that data
    # 3. Otherwise, fetch from database

    # get the first item in the objects corresponding to the id
    start = time.time()
    img_obj = Image.objects(id="5aece64431b4b78caaa65d4c").first()
    end = time.time()
    db_load_time = end - start

    if img_obj is None:
        # log that the image id dosent correspond to an image
        print("hello")
        # redirect (essentially a return)
    
    # do what you need to do w image retrived

    # REDO THE STUFF BELOW

    for obj in Image.objects(id=id):
        newObj = {
            'title': obj.title, 
            "description": obj.description,
            "image": obj.photo.read(), 
            "id": str(obj.id)
        }
    object_id = newObj['id']
    # object_id = str(newObj['id'])
    # print ("objectId: ", object_id, type(object_id))
    newObj['image']= b64encode(newObj['image']).decode("utf-8")

    r = redis.Redis(host='localhost', port=6379, db=0)
    print("\n\n\n")

    r.hmset(id, newObj)

    print("Keys:", r.keys())

    print("\n\nCACHE HIT:")

    start = time.time()
    redisValue = r.hgetall(id)
    end = time.time()
    redis_load_time = end - start

    print("DB LOAD TIME:", db_load_time, "\nREDIS LOAD TIME:", redis_load_time, "\nSPEED UP:", (db_load_time) / redis_load_time)

    a = decode_redis(redisValue)

    print("\n\nCACHE MISS:")

    start = time.time()
    img_obj = Image.objects(id="5aece64431b4b78caaa65d4c").first()
    end = time.time()
    db_load_time = end - start

    start = time.time()
    redisValue = r.hgetall(id)
    end = time.time()
    redis_load_time = end - start

    print("DB LOAD TIME:", db_load_time, "\nREDIS LOAD TIME:", redis_load_time, "\nSPEED UP:", (db_load_time) / redis_load_time)

    return render_template("anImage.html", image=a)

# DELETE route for images in database
@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    if request.method == 'POST':
        print("delete")
        x = Image.objects(id=id).delete()
        print("DELTED:", x, "<-- is this null ?")
    return redirect("/")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # add docstring explanation
    # redirect
    return 'ok'
app.run(debug=True)

