# Fabriquer l'image
```
docker build -t docker-example .
```

# Démarrer le conteneur
```
docker run -p 127.0.0.1:5000:5000/tcp -it docker-example
```

 cd front_service 
export FLASK_APP=front_service
export FLASK_DEBUG=1          
cd ..
