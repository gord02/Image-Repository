import mongoengine
from mongoengine import StringField, IntField, ListField, Document, connect, EmbeddedDocument, EmbeddedDocumentField, ImageField, FloatField, FileField

connect('imageRepo')

class Image(Document):
    title= StringField(required=True)
    description= StringField(required=True)
    photo = FileField(required=True)
    # picture = ImageField()

    # meta = {'indexes': [
    #     {'fields': ['$title', "$description", 'photo'],
    #      'default_language': 'english',
    #      'weights': {'title': 10, 'content': 2}
    #     }
    # ]}
    meta = {'strict': False}

# class Pic(Document):
#     title= StringField(required=True)
#     description= StringField(required=True)
#     photo = FileField(required=True)
#     # picture = ImageField()
    # (size=(800, 600, True)

def addImage():
    print("inside")
    # --------------------
    # image = Image(title='Dog')
    # image.description = "Dog in sweater "
# rb, r is for read, b is for binary so it is read the file as binary code
    # my_image= open('Dog.jpg', 'rb')
    # image.picture.replace(my_image, filename="Dog.jpg")
    # with open('Dog.jpg', 'rb') as fd:
    #     image.photo.put(fd, content_type = 'image/jpeg')
    # image.save()
    # --------------------

    image = Image(title='Dog')
    image.description = "dog in sweater "
    fileHandle= open("Dog.jpg", "rb")
    image.photo.put(fileHandle, filename='Dog.jpg')
    # image.picture.put(open("Snake.jpg", "rb"))
    image.save()


# addImage()
