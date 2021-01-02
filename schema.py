import mongoengine
from mongoengine import StringField, Document, connect, FileField

connect('imageRepo')

# black formatter python, download the package, add to env, run the black linter command on each python file

"""
Comments:
1. remove unnecessary comments
2. Spacing on each side of equal sign, except for paramters
3. Docstring comments python for each class and function
4. Add a space after commas
"""

class Image(Document):
    """
    MongoDB Document for the image Collection.

    title: string -- title of the image
    description: string -- description of the image
    photo: GridFS Object -- image stored in bytes, managed with GridFS
    """
    
    title = StringField(required=True)
    description= StringField(required=True)
    photo = FileField(required=True)
    meta = {'strict': False}

def addImage(filepath, title, description):
    image = Image(title='Dog')
    image.description = "dog in sweater"
    fileHandle= open("Dog.jpg", "rb")
    image.photo.put(fileHandle, filename='Dog.jpg')
    image.save()

if __name__ == "__main__":
    # instantiate variable to test the add image function
    filepath = "Dog"
    title = "Dog in sweater"
    description = "Dog.jpg"

    # run the addImage function
    addImage(filepath, title, description)
