import requests
import sys
import os
from bs4 import BeautifulSoup


def get_pic(s , movie):
    s2 = s.replace(' ','_')
    s2 = 'https://fr.wikipedia.org/wiki/' + s2

    req = requests.get(s2)
    soup = BeautifulSoup(req.text, "lxml")

    #with open('txt.html', 'w+') as file:
        #file.write(str(soup))

    for a in soup.find_all("div", {"class":"infobox_v3 large"}):
        #print(str(a) + "\n")
        pic = a.select("img")[0]
        #print('https:' + str(pic['src']))
        ext = str(pic['src']).split('.')[-1]
        #print(ext)
        pic = requests.get('https:' + str(pic['src']))
        #print(pic)
    os.mkdir('data/' + movie + '/' + s)

    try:
        
        with open('data/' + movie + '/' + s + '/' + s + '.' + ext, 'wb+') as file:
            #file.write(pic.text)
            for block in pic.iter_content(1024):
                    if not block:
                        break
                    file.write(block)
        
    except:
        #os.remove(movie + '/' + s + '/' + s + '.' + ext)
        os.rmdir('data/' + movie + '/' + s)
                
s = sys.argv[1]
if not (os.path.isdir('data/' + s)):
    os.mkdir('data/' + s)
    s2 = s.replace(' ','+')
    s2 = 'https://www.google.com/search?q=' + s + '+film+distribution'
    req = requests.get(s2)
    soup = BeautifulSoup(req.text, "lxml")
    r = 0
    print('Downloading pictures of ' + s  + '...')
    for a in soup.find_all("a", {"class":"BVG0Nb"}):
        #print(str(a) + "\n")
        for actor in a.select("div", {"class":"BNeawe s3v9rd AP7Wnd"}):
            if str(actor).count('div') < 3 and 'img' not in str(actor):
                if r % 2 == 0:
                    get_pic(actor.text, s)
                #print(actor.text)
                r += 1

from PIL import Image
import face_recognition
import numpy as np
from PIL import Image, ImageDraw
from IPython.display import display
import glob
from pathlib import Path
import os

def recognition(image_path):
    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(image_path)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(153, 27, 0))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(153, 27, 0), outline=(153, 27, 0))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    return(pil_image)

known_face_encodings = []
known_face_names = []

for filename in glob.glob('data/' + s + '/**/*.jpg'): #assuming jpg files
    face_image = face_recognition.load_image_file(filename)
    if len(face_recognition.face_encodings(face_image)):
        face_encoding = face_recognition.face_encodings(face_image)[0]
        filename_str = str(filename)
        known_face_names.append(os.path.basename(str(Path(filename_str).parent)))
        # Create arrays of known face encodings and their names
        known_face_encodings.append(face_encoding)
        
    print('Learned encoding for', len(known_face_encodings), 'images.')


print('You can take a picture of your current movie...')
from PIL import ImageGrab
from PIL import Image 
import keyboard
while True:
    try:
        if keyboard.is_pressed('space'):
            image = ImageGrab.grab(bbox =(0, 80, 1920, 1020))
            image.save("screenshot/screenshot.png")
            img = recognition("screenshot/screenshot.png")
            img.save("screenshot_recognized/screenshot_recognized.png")
            img.show() 
            break
        else:
            pass
    except:
        break