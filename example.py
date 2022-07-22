from pynput import keyboard
from picamera import PiCamera
import numpy as np
from os.path import exists as file_exists
from time import sleep
from tensorflow.python import keras
from keras.models import load_model
from keras.preprocessing import image
import firebase_admin
from firebase_admin import credentials,db

databaseURL="Use your firebase URL"
cred = credentials.Certificate("GIVE DB Name followed by.json")
default_app=firebase=firebase_admin.initialize_app(cred,{
	'databaseURL':databaseURL
	})

print('env ready');

def on_press(key):
    if key==keyboard.Key.space:
        print('key pressed')
        camera = PiCamera()
        camera.start_preview()
	#add the path acordingly
        camera.capture('/home/pi/Desktop/ML/image.jpg')
        print(file_exists('/home/pi/Desktop/ML/image.jpg'))
        if(file_exists('/home/pi/Desktop/ML/image.jpg')):
            model=load_model(r"garbage.h5")
            img = image.load_img("image.jpg",target_size=(128,128))
            x=image.img_to_array(img)
            x=np.expand_dims(x,axis=0)
            prediction=model.predict(x)
            index=["cardbord","glass","metal","paper","plastic","trash"]
            result=str(index[prediction[0].tolist().index(1)])
            print(result)
            ref=db.reference('/garbage/category/'+result)
            data=ref.get()
            if data:
                ref.set({
                    result:data[result]+1
                })
            camera.stop_preview()
            camera.close()
            
            
def on_release(key):
    if key==keyboard.Key.esc:
        return False
    

with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()












        


