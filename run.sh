#!/bin/bash
#Mansoorali Amiri
echo "Run docker file" 
#echo "TODO: fill in the docker run command"
#docker run --env-file .env --publish 5000:5000  ift6758
#docker run -it -p 127.0.0.1:5000:5000/tcp --env COMET_KEY=$COMET_KEY image_docker_personnalisee:$1
#gunicorn --bind 0.0.0.0:8080 app:app
gunicorn -c serving/app.py --bind 0.0.0.0:8080 app:app