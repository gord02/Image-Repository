from mongoengine import connect, Document, FileField, StringField

connect("imageRepo")

class Image(Document):
    """
    MongoDB Document for the image Collection.

    title: string -- title of the image
    description: string -- description of the image
    photo: GridFS Object -- image stored in bytes, managed with GridFS
    """
    
    title = StringField(required=True)
    description = StringField(required=True)
    photo = FileField(required=True)
    meta = {"strict": False}

def addImage(filepath, title, description):
    """
    Creates image in the MongoDB database based on parameters

    title: string -- title of the image
    description: string -- description of the image
    photo: GridFS Object -- image in suffishent file format
    """
    image = Image(title=title)
    image.description = description
    fileHandle = open(filepath, "rb")
    image.photo.put(fileHandle, filename=filepath)
    image.save()

if __name__ == "__main__":
    # instantiate variable to test the add image function
    filepath = "Dog"
    title = "Dog in sweater"
    description = "Dog.jpg"

    # run the addImage function
    addImage(filepath, title, description)
