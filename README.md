# ClipoAI

ClipoAI is a Flask-based web application for managing video projects. It allows users to create, update, and delete video projects, upload video files, and perform basic video processing tasks.

## Features

- Create, update, get and delete video projects
- Upload video files associated with video projects
- Basic video processing functionalities:
  - Generate thumbnail images from video files
  - Extract metadata from video files

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/ClipoAI.git
cd ClipoAI
```

# Install dependencies

- Install Docker For Your System ( MacOS, Linux, Windows )

# Docker

- You should run the application in a Docker container

```bash
docker build -t clipoai .
docker run -p 5000:5000 -v /path/to/host/directory:/app/uploads clipoai
```

- Replace `/path/to/host/directory` ( Absolute Path ) with the directory where you downloaded the repository.

# Working Of API

## Get Access Token

- First create user with the below API

```py
requests.post('http://localhost:5000/api/signup', data={'email': 'test1@gmail.com', 'username': 'test1', 'password': 'test1'})
```
-- Responces
--- If Successful
```json
{'message': 'User created successfully'}
```
--- If Username already exists
```json
{'message': 'Username already exists'}
```
--- If Email already exists
```json
{'message': 'Email already exists'}
```
