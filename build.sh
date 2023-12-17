#!/bin/bash
#Mansoorali Amiri
#echo "TODO: fill in the docker build command"
echo "Create docker build file" 
#docker build -t nhl_serving -f Dockerfile.serving .
#docker build -t nhl_streamlit -f Dockerfile.streamlit .
docker build -t ift6758 -f Dockerfile.serving .
docker build -t ift6758 -f DockerFile.streamlit .
