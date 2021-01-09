import io
import json
import time
import logging
from base64 import b64encode

import redis
from mongoengine import connect
from flask import (Flask, render_template, request, send_file, redirect)

from schema import Image
from decoder import decode_redis

"""
Comments:
1. remove unnecessary comments
2. Spacing on each side of equal sign, except for paramters
3. Declarative instantiation for lists and dictionary
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

# setup logging config
logging.basicConfig(level=logging.INFO)

@app.route("/")
def allImages():
    """
    AllImages function used for displaying the images from the MongoDB database to be displayed in the flask template frontend component.
    """
    images = list() 
    # Gets documents from Image collection
    mongoengineObjects = Image.objects()
    for obj in mongoengineObjects:
        imageObject = {
            "title": obj.title,
            "description": obj.description,
            # reads image as binary
            "image": obj.photo.read(),   
            "id": obj.id
        }
        # allows only type bytes to be added to image list
        if(type(imageObject['image']) is bytes):
            # converts bytes into base64 to be displayed in html
            imageObject['image'] = b64encode(imageObject['image']).decode("utf-8")
            # pushes displayable images into list
            images.append(imageObject)
        else:
            logging.error(imageObject)
           
    # sends list of images to html
    return render_template("allImages.html", images=images)

@app.route("/", methods=['POST'])
def search():
    """
    Search function is used to limit the results displayed in the frontend allowing user to filter thorugh all the pictures in the database based on a specifc word search
    """
    if request.method == "POST":
        searchedValue = request.form["searchValue"]
        images = list()
        mongoengineObjects = Image.objects.search_text(searchedValue)

        for obj in mongoengineObjects:
            imageObject = {
                "title": obj.title,
                "description": obj.description,
                "image": obj.photo.read(),   
                "id": obj.id
            }
            if(type(imageObject['image']) is bytes):
                imageObject['image'] = b64encode(imageObject['image']).decode("utf-8")
                images.append(imageObject)
            else:
                logging.error(imageObject)

    return render_template("show.html", images=images)

@app.route("/addImage", methods=['GET','POST'])
def addImageToDB():
    """
    Route for adding an image to the database
    """
    if request.method == "POST":
        title = request.form["searchValue"]
        description = request.form["description"]
        file = request.files["file"].read()

        # creates a document for image in collection Image
        image = Image(title=title)
        image.description = description
        image.photo.put(file, filename=(title+".jpg"))
        image.save()
        return redirect("/")
    return render_template("form.html")

@app.route("/image/<id>", methods=['GET'])
def individualImage(id):
    """
    Route for displaying a single image based on id

    id: string -- id of image to be displayed in database
    """
    # redis configuration
    r = redis.Redis(host='localhost', port=6379, db=0)
    # ENV MAKE A DOT.ENV

    # ---------------------------------------------


    # Verifies if image is in reddis, if not it is added and object is stored in Redis
    if r.hgetall(id) == {}:
        mongoengineObject = Image.objects(id=id).first()

        if mongoengineObject is None:
            logging.error("The user has tried to display image that is not available, image id doesn't correspond to an image")
            return render_template("error.html")

        imageObject = {
            "title": mongoengineObject.title, 
            "description": mongoengineObject.description,
            "image": mongoengineObject.photo.read(), 
            "id": str(mongoengineObject.id)
        }
        imageObject['image'] = b64encode(imageObject['image']).decode("utf-8")

        r.hmset(id, imageObject)
        imgObjectToSendToHtml = imageObject
    else:
        redisValue = r.hgetall(id) 
        image = decode_redis(redisValue)
        imgObjectToSendToHtml = image

    return render_template("anImage.html", image=imgObjectToSendToHtml)

# DELETE route for images in database
@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    """
    Route for deleting images from the database based on the id passed through url of post request

    id: string -- id of image to be deleted in database
    """
    if request.method == 'POST':
        # Image is deleted and the if statement verifies that it was successful
        if(Image.objects(id=id).delete() == 0):
            logging.error("User tried to delete an image unsuccessfully")
    return redirect("/")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """
    Route created to redirect to homepage of application if route is not already specified 

    path: string -- undefined url
    """
    return redirect("/")
app.run(debug=True)
