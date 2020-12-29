# import Store from schemas
import mongoengine 
from schema import Image
from mongoengine import StringField, IntField, ListField, Document, connect
# ross = User(email='ross@example.com')
# ross.first_name = 'Ross'
# ross.last_name = 'Lawley'
# ross.save()
connect(db='imageRepo')

print("outside")

def addImage():
    print("inside")
    image = Image(title='Dog')
    image.description = "Dog in sweater "
    # image.photo = 54.55
    # image.save()
    with open('Downloads/Dog.jpg', 'rb') as fd:
        image.photo.put(fd, content_type = 'image/jpeg')
    image.save()

# addImage()