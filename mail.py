from database import Mongo


def add_contact(name, email, theme, question):
    Mongo.insert('journalist',{'name': name, 'email': email, 'theme': theme, 'question': question})

def get_contact():
    return Mongo.get_all('journalist')

