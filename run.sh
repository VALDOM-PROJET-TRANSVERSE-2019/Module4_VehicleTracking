docker build -t tracker .
docker run -it -p 5000:5000 --name track tracker