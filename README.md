# ActorWho 

let's detect the actors on screen !

## Features

#### Find faces in pictures

Find all the faces that appear in a picture:

```python
import face_recognition
image = face_recognition.load_image_file("your_file.jpg")
face_locations = face_recognition.face_locations(image)
```

#### Identify faces in pictures

Recognize who appears in each pictures.

![](https://i.ibb.co/5cn3x1Q/readme.png)

```python
import face_recognition
known_image = face_recognition.load_image_file("biden.jpg")
unknown_image = face_recognition.load_image_file("unknown.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
```

## Installation

1. Clone the git repo
   ```sh
   git clone https://github.com/pbsnr/ActorWho.git
   ```
2. Install lib packages
   ```sh
   pip install imdbpy
   pip install cmake
   pip install dlib
   pip install face-recognition
   pip install pynput
   pip install pyscreenshot
   
   ```

## Running the project

GetActors.py should be used as follows :

```
python GetActors.py "<movie title>"
```
