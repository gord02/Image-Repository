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

# Allows use to add to the database in mongoDB called covid-checkin
connect(db='imageRepo')

app = Flask("__main__")

# Setup logging config
logging.basicConfig(level=logging.INFO)

@app.route("/")
def displayAllImages():
    """
    This route is used to display the images from the MongoDB database in the jinja2 frontend template.
    """
    images = list() 
    # Gets documents from Image collection
    mongoengineObjects = Image.objects()
    for obj in mongoengineObjects:
        imageObject = {
            "title": obj.title,
            "description": obj.description,
            "image": obj.photo.read(),  # Reads image as binary 
            "id": obj.id
        }
        # Allows only type bytes to be added to image list
        if(type(imageObject['image']) is bytes):
            # Converts bytes into base64 to be displayed in html
            imageObject['image'] = b64encode(imageObject['image']).decode("utf-8")
            # Pushes displayable images into list
            images.append(imageObject)
        else:
            logging.error( "this image is not of type bytes", imageObject)
           
    # Sends list of images to frontend for rendering
    return render_template("allImages.html", images=images)

@app.route("/", methods=['POST'])
def search():
    """
    This route is used to limit the results displayed in the frontend allowing user to filter through all the pictures in the database based on a specifc word search
    """
    images = list()
    if request.method == "POST":
        searchValue = request.form["searchValue"]
        mongoengineObjects = Image.objects.search_text(searchValue)

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
                logging.error("this image is not of type bytes", imageObject)

    return render_template("show.html", images=images)

@app.route("/addImage", methods=['GET','POST'])
def addImageToDB():
    """
    Route for adding an image to the database
    """
    if request.method == "POST":
        searchValue = request.form["searchValue"]
        description = request.form["description"]
        file = request.files["file"].read()

        # creates a document for image in collection Image
        image = Image(title=searchValue)
        image.description = description
        image.photo.put(file, filename=(searchValue+".jpg"))
        image.save()
        return redirect("/")

    return render_template("form.html")

@app.route("/image/<id>", methods=['GET'])
def displayIndividualImage(id):
    """
    Route for displaying a single image based on id

    id: string -- id of image to be displayed in database
    """
    # redis configuration
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Checks if the image is in Redis first, if the image is not found in Redis, the image is searched for in mongoDB
    if r.hgetall(id) == {}:
        mongoengineObject = Image.objects(id=id).first()

        # If the image is not found in MongoDB, an error is logged and error page is rendered
        if mongoengineObject is None:
            logging.error("The user has tried to display image that is not available, image id doesn't correspond to an image Id: '", id "' was not found")
            return render_template("error.html")

        imageObject = {
            "title": mongoengineObject.title, 
            "description": mongoengineObject.description,
            "image": mongoengineObject.photo.read(), 
            "id": str(mongoengineObject.id)
        }
        imageObject['image'] = b64encode(imageObject['image']).decode("utf-8")

        # Adds the image to Redis so that the next time it is retrived in this route it will be found in Redis which is a faster process than MongoDB
        r.hmset(id, imageObject)
        imgObjectToSendToHtml = imageObject
    else:
        # If the image was found in Redis it will be retrived and send to frontend
        redisValue = r.hgetall(id) 
        image = decode_redis(redisValue)
        imgObjectToSendToHtml = image

    return render_template("anImage.html", image=imgObjectToSendToHtml)

@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    """
    Route for deleting images from the database based on the id passed through url of post request

    id: string -- id of image to be deleted in database
    """
    if request.method == 'POST':
        # Image is deleted and the if statement verifies that it was successful
        if(Image.objects(id=id).delete() != 1):
            logging.error("User tried to delete an image unsuccessfully. Id: ", id)

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
