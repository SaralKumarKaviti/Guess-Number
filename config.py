from mongoengine import connect

client = connect('game',host='localhost',port=27017)