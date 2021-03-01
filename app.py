#library imports
import requests
import sys
import os
import numpy as np
import face_recognition
import glob
import math
import json
from imdb import IMDb
from imdb import helpers
from bs4 import BeautifulSoup
from PIL import Image
from PIL import Image, ImageDraw
import pyscreenshot as ImageGrab
from IPython.display import display
from pathlib import Path
from PIL import Image 
from flask import Flask, flash, request, redirect, url_for
from flask import jsonify ,render_template
from flask_cors import CORS
import base64
import io
from PIL import Image
from unidecode import unidecode
import pickle as P


from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/screenshot'
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_folder='static')
CORS(app)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

actors_dict = { 'test':'test1'}

#----------------------------------------------------------------------
#Get actors data
#----------------------------------------------------------------------

#clean headshot url
def url_clean(url):
    base, ext = os.path.splitext(url)
    i = url.count('._')
    s2 = url.split('._')[0]
    url = s2 + ext
    return url

#get movie
def get_movie(name, ia):
    movies = ia.search_movie(name)
    id = movies[0].movieID
    movie = ia.get_movie(id)
    movie_title = movie['title']
    return movie, movie_title
	


#get actors data from json 

def actor_json(actors_name, movie_title):
	all_actors = {}
	for i in actors_name:
		all_actors[i] = {}
		filename = "data/" + movie_title + "/"+i+"/"+i+".json"
		with open(filename, 'rb') as f:
			actor_data = json.load(f)
			del actor_data['biography'], actor_data['trade mark'], actor_data['trivia'], actor_data['filmography']
		all_actors[i] = actor_data
	return all_actors
			
	


def recognition(image_path, movie_title):
    known_face_encodings = []
    known_face_names = []
    name_list = []
    for filename in glob.glob('data/' + movie_title + '/**/*.pickle'): #assuming jpg files
        #face_image = face_recognition.load_image_file(filename)
            #face_encoding = face_recognition.face_encodings(face_image)[0]
        with open(filename, 'rb') as f:
            face_encoding = P.load(f)
            filename_str = str(filename)
            known_face_names.append(os.path.basename(str(Path(filename_str).parent)))
            # Create arrays of known face encodings and their names
            known_face_encodings.append(face_encoding)
        print('Learned encoding for', len(known_face_encodings), 'images.')
    
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
        acc = 0
        acc_stred = '0'

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if face_distances.size == 0:
            print("No actors found")

        dist = face_distances[0] - face_distances[1]
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            name_list.append(name)
            acc = format(face_distance_to_conf(dist), '.2f')
            acc_stred = str(acc)
    # Name :
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(153, 27, 0))
        
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=check_dist(acc), outline=check_dist(acc))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        
    # Accuracy :
        if acc == 0:
            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=check_dist(acc))

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(acc_stred)
            draw.rectangle(((right - 15 , top - text_height - 10), (right, top)), fill=check_dist(acc), outline=check_dist(acc))
            draw.text((right - 15 + 6, top - text_height - 5), acc_stred, fill=(255, 255, 255, 255))
        if acc != 0: 
            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=check_dist(acc))

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(acc_stred)
            draw.rectangle(((right - 40 , top - text_height - 10), (right, top)), fill=check_dist(acc), outline=check_dist(acc))
            draw.text((right - 40 + 6, top - text_height - 5), acc_stred, fill=(255, 255, 255, 255))
    
    # Remove the drawing library from memory as per the Pillow docs
    del draw
	
    # Display the resulting image
    return(pil_image, actor_json(name_list, movie_title))


#----------------------------------------------------------------------
#Face recognition processing
#----------------------------------------------------------------------


def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return (linear_val)*100
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2)))*100
    
def check_dist(distance):
    distance = float(distance)
    if distance == 0:
        return (153, 27, 0)
    if distance > 90:
        return (19, 129, 12)

#----------------------------------------------------------------------
#Get actors info function
#----------------------------------------------------------------------

def get_info(a, actor, movie):
    film = []
    try:
        for i in actor['filmography']['actress']:
            film.append(i['title'])
    except:
        for i in actor['filmography']['actor']:
            film.append(i['title'])
            
    try: name = actor['name']
    except : name = " "
        
    try: currentRole = a.currentRole['name']
    except : currentRole = " "
    
    try: birthName = actor['birth name']
    except: birthName = " "
        
    try: birthDate = actor['birth date']
    except: birthDate = " "
    
    try: birthPlace = actor['birth info']["birth place"]
    except : birthPlace = " "
        
    try: height = actor['height']
    except: height = " "
    
    try: bio = actor['biography'][0]
    except : bio = " "
        
    try: trademark = actor['trade mark'][0]
    except: trademark = " "
    
    try: trivia = actor['trivia']
    except : trivia = " "
    
    listOfKeys = ["name", "current role", "birth name" , "birth date", \
                  "birth place", "height", "biography", "trade mark" , "trivia", "filmography"]

    listOfValues = [name, currentRole, birthName, birthDate, birthPlace, height, bio, trademark, trivia, film]
    
    dictOfWords = dict(zip(listOfKeys, listOfValues))
    
    return dictOfWords

#----------------------------------------------------------------------
#Recognition main function
#----------------------------------------------------------------------

def recog(movie_input, image_to_recog):
    i = 0

    ia = IMDb()
    movie, movie_title = get_movie(movie_input, ia)
    #get actors headshots
    if not (os.path.isdir('data/' + movie_title)):
        os.mkdir('data/' + movie_title)
        print('Downloading pictures of ' + movie_title  + '...')
        for a in movie['cast']:
            if i > 30:
                break
            actor_id = a.personID
            actor = ia.get_person(actor_id)
            actor_name = a['name']

            try:
                image = url_clean(actor['headshot'])
                pic = requests.get(image)
                ext = image.split('.')[-1]
                try:
                    if pic.status_code == 200:
                        os.mkdir('data/' + movie_title + '/' + actor_name)
                        with open('data/' + movie_title + '/' + actor_name + '/' + actor_name + '.' + ext, 'wb') as f:
                            f.write(pic.content)
                            print('Downloaded picture of ' + actor_name)
                            i += 1
                        face_image = face_recognition.load_image_file('data/' + movie_title + '/' + actor_name + '/' + actor_name + '.' + ext)
                        if len(face_recognition.face_encodings(face_image)):
                            face_encoding = face_recognition.face_encodings(face_image)[0]
                            with open('data/'+ movie_title + '/' +actor_name+'/encoded.pickle', 'wb') as handle:

                                P.dump(face_encoding, handle)

                    dictInfo = get_info(a, actor, movie)
                    with open('data/' + movie_title + '/' + actor_name + '/' + actor_name + '.json', "w") as outfile:  
                        json.dump(dictInfo, outfile) 
                except:
                    pass
            except:
                print("No picture found for " + actor_name)
                pass
        print("All pictures dowloaded !")
    else:
        print("Pictures already downloaded !")


    image_to_recog.save("static/screenshot_recog.png")
    img_done, actors_dict = recognition("static/screenshot_recog.png", movie_title)
    img_done.save("static/screenshot_recog.png")
    return img_done, actors_dict

def url_to_title(link):
    if 'netflix.com' in link:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        movies = soup.findAll('title')
        title = str(movies)
        title = title.replace('[<title>','')
        title = title.replace('| Netflix</title>]','')
        return title
    elif 'primevideo.com' in link: 
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        movies = soup.findAll('title')
        title = str(movies[0])
        title = title.replace('<title>Prime Video:','')
        title = title.replace('</title>','')
        return title
    else:
        return None
    

@app.route('/<url>')
def home(url):
    print(actors_dict)
    return render_template('index.html', movie = url_to_title(url.replace("(","/")), actors_dict=actors_dict)

"""@app.route('/recognize', methods=['POST'])
def detect():
    #get the image and preprocess.
    file = request.files['image']
    # Read image
    image = recognition(file)"""


@app.route('/upload', methods=['POST'])
def upload():
    #file = Image.open('screenshot/images.jpg')
    #file = request.get_data()
    file = request.get_json(force=True)
    
    decoded = (file["img"])
    decoded_done = base64.b64decode(decoded[22:])

    
    with io.BytesIO(decoded_done) as fh:
        image = Image.open(fh)
        #display(image)
        #image.show()
        global actors_dict
        print(actors_dict)
        img, actors_dict = recog(file["title"], image)
        #img.show()
	
        #return render_template('index.html', actors_dict=actors_dict , image_to_show=img, init=True)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r




if __name__ == '__main__':
    app.run(debug=False,
            use_reloader=False,
            host="0.0.0.0",
            port=4000)







