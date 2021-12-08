pip install requirements.txt

#Dans un terminal :
export FLASK_APP=backend
export FLASK_DEBUG=1
cd ..
flask run -p 5001


#Pour la dockerisation (TODO)
# Fabriquer l'image
```
docker build -t docker-example .
```

# Démarrer le conteneur
```
docker run -p 127.0.0.1:5000:500/tcp -it docker-example
```

