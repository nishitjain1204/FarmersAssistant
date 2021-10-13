import pyrebase

#Initialize Firebase
firebaseConfig={
  "apiKey": "AIzaSyCU7Z9cjEXMnhzdrh9FcoP57KjFbZO4rR4",

  "authDomain": "farmers-assistant-5b173.firebaseapp.com",

  "databaseURL": "https://farmers-assistant-5b173-default-rtdb.firebaseio.com",

  "projectId": "farmers-assistant-5b173",

  "storageBucket": "farmers-assistant-5b173.appspot.com",

  "messagingSenderId": "872170303948",

  "appId": "1:872170303948:web:e900f32dbac6e0e3c42d69",

  "measurementId": "G-2CQJ2645FK"

}


firebase=pyrebase.initialize_app(firebaseConfig)

db=firebase.database()

#Push Data
