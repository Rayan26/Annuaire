pip install requirements.txt
#Dans un terminal :
export FLASK_APP=frontend
export FLASK_DEBUG=1
cd ..
flask run -p 5000


#Pour la dockerisation (TODO)
# Fabriquer l'image
```
docker build -t docker-example .
```

# Démarrer le conteneur
```
docker run -p 127.0.0.1:5000:5000/tcp -it docker-example
```