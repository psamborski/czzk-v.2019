# Czarny Ziutek z Killerami
A website designed and created for music band Czarny Ziutek z Killerami.
Soon you'll have the possibility to see it on http://czzk.pl/ ;)

### Some features of CMS
  - CRUD for concerts, merch, albums
  - C&D for galleries
  - update for some other stuff

### Tech

This app uses technologies like:
* [Python3.6](https://www.python.org/) - basic programming language
* [Flask 1.0.2](http://flask.pocoo.org/) - my favourite microframework for Python
* [blueImp Gallery](https://github.com/blueimp/Gallery) - my favourite library for galleries
* and maybe some other but I don't remember now ;)

### Installation

It requires Python 3.6 to run. 

Firsty, create somewhere your virtual environment for this project [check this out](https://docs.python.org/3/library/venv.html) and activate it:
```sh
$ python3 -m venv /path/to/new/virtual/environment
$ source  [path]/venv/bin/activate
```
Then, using *pip*, install all dependencies from included file [check this out](https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a):
```sh
$ pip install -r /path/to/requirements.txt
```
(I'll add this file later)

You may need *setup-tools* if you don't have it.
Then run the app on *localhost* (*Ubuntu*):
```sh
$ python3 path/to/project/run.py
```
### Credits
All rights deserved to Patryk Samborski &#169; 2019. Nevertheless - get inspired :D

I also recommend tutorials by [Corey Schafer](https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g) - they helped me a lot while doing my project! [(his Github)](https://github.com/CoreyMSchafer)
