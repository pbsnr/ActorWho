FROM python:3.6

WORKDIR /app

COPY requirements.txt .

ENV FLASK_APP=app.py

RUN apt-get update && \
    apt-get install -y --fix-missing \
    build-essential \
    cmake

# Install DLIB
RUN cd ~ && \
    git clone https://github.com/davisking/dlib.git && \
    cd dlib && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . && \
    cd .. && \
    python3 setup.py install

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["python", "-u", "app.py"]
