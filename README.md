# Flack

> A simple chatroom utilizing HTML, CSS, Javascript and Socket.IO. This project was made for CS50W.

## Usage

- Sign in using a username.

![SIGNIN GIF](http://g.recordit.co/rMVoZm9xyK.gif)

- Create a chatroom. 

![CREATE CHATROOM GIF](http://g.recordit.co/VuesKBi4ZI.gif)

- View all channels and users.

![VIEW GIF](http://g.recordit.co/uxBnCWszyx.gif)

- Join any chatrooms and interact with other users.

![JOIN GIF](http://g.recordit.co/W31ku9nYuO.gif)

- Personal touch: send an alert message to a specific user.

![ALERT GIF](http://g.recordit.co/lmBLR7QGzj.gif)

- Remembers you and the channel you were on even if you closed the window/browser.

![REMEMBER GIF](http://g.recordit.co/fMML27YEXM.gif)

## Local Deployment

- All the `code` required to get started

### Clone

- Clone this repo to your local machine using `https://github.com/joiellantero/Flack.git`

### Setup

- After cloning run the following code to get started:

> Open terminal and navigate to the directory of the cloned repo

```shell
$ cd Flack-<branchname>

# example - if on branch master
$ cd Flack-master
```

> Activate your virtual environment

```shell
$ virtualenv env
$ source env/bin/activate
```

> Install the required modules

```shell
$ pip3 install -r requirements.txt
```

> Setup flask and database

```shell
$ export FLASK_APP=application.py
$ export FLASK_ENV=development
$ export SECRET_KEY="secret"
```

> Run flask

```shell
$ flask run
```

### Resources

- Image from Freepik.com
- Favicon from https://gauger.io/fonticon/
- Bootstrap v4.4.1
- Material Design for Bootstrap 4
- Font Awesome v5.8.2
