# Face Recognition based on [FaceNet](https://arxiv.org/abs/1503.03832) paper by Google researchers

A simple Face recognition AI coupled with Node.js server.
Following Technologies were used while building the software

#### Machine Learning
* [Python](https://www.python.org/)
* [Tensorflow](https://www.tensorflow.org/)
* [Keras](https://keras.io/)
* [Anaconda](https://anaconda.org/)

#### Image Processing
* [dlib](http://dlib.net/)
* [OpenCV](https://opencv.org/)

#### Server
* [Node.js](https://nodejs.org/)
* [Express.js](https://expressjs.com/)

#### Pub/Sub
* [Redis](https://redis.io/)


## API end point

[localhost:3000/]()

* #### Request Body to train
You can send upto 10 images for each person
image is an array of image files 

note: you have to prepend "images/" to each file name 
`I am planning to change this in future`

```
{
    "type": "train",
    "data": {
        "name": "String",
        "image": ["images/file1", "images/file2"]
    }
}
```

* #### Request Body to test

note: you have to prepend "images/" to each file name 
`I am planning to change this in future`

```
{
    "type": "train",
    "data": "images/file"
}
```
        
## How to run on your own machine

1. Before You start make sure you have every thing setuped
    * Install Anaconda
    * Create a Conda environment
    * Install Keras and Tensorflow
    * Install Opencv and dlib
    * Install Node.js
    * Install Redis
    
2. Next cd to faceReco dir

    ```cd /path/to/faceReco```

3. Start redis server

    ```redis-server --daemonize yes```

4. Start Node server

    ```npm install```

    ```node server.js```
    
5. Activate Conda environment

    ```source activate environmentName```

6. Start AI

    ```python pubsub.py```
