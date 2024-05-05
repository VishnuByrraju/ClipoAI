# ClipoAI Assignment

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
git clone https://github.com/VishnuByrraju/ClipoAI.git
cd ClipoAI
```

# Install dependencies

- Install Docker For Your System ( MacOS, Linux, Windows )

# Docker

- You should run the application in a Docker container

```bash
docker build . -t buildname
docker run -p 5000:5000 -v /path/to/host/directory:/app buildname
```

- Replace `/path/to/host/directory` ( Absolute Path ) with the directory where you downloaded the repository.
- Example Path `F:\InternShip\ClipoAI`
# MongoDB Connection String
- Before Starting The Project You Need To Change The MongoDB Connection String In app.py

# Working Of API

## Get Access Token

### First create user with the below API ( SignUp )

```py
requests.post('http://localhost:5000/api/signup', data={'email': 'test1@gmail.com', 'username': 'test1', 'password': 'test1'})
```
#### Responces
- If Successful
```bash
{'message': 'User created successfully'}
```
- If Username already exists
```bash
{'message': 'Username already exists'}
```
- If Email already exists
```bash
{'message': 'Email already exists'}
```
### Now Sign In With The Created User ( Sign In )
```py
requests.post('http://localhost:5000/api/login', data={'username': 'test1', 'password': 'test1'})
```
- If Successful

```bash
{'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDg5MjM5MSwianRpIjoiNTg0MzkxM2ItY2QwMS00MDRlLTgyOGUtNDI4Nzg1YjJhYmJhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QxIiwibmJmIjoxNzE0ODkyMzkxLCJjc3JmIjoiMGE3ZjI4NjUtMGU5MS00YmNlLWFkZjMtNGY5NzU3NjY5MDk0IiwiZXhwIjoxNzE0ODk1OTkxfQ.P9huc8DsNX4ljXqW2laKv7T1PgGaIL5y7nMl4oQ8rws'}
```
- If Wrong Credentials
```bash
{'message': 'Invalid credentials'}
```

## Create Video Project

### Create API

```py
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDg5MDMxNCwianRpIjoiMDU5OWNhZmMtNDdhYi00M2YzLThlYjItZjgwZGQyMWNhNzQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QxIiwibmJmIjoxNzE0ODkwMzE0LCJjc3JmIjoiNjliNWM0M2MtNThiMS00OWM1LWJkNjYtNjcxZmQ5M2E5ZDA3IiwiZXhwIjoxNzE0ODkzOTE0fQ.ij4WcHOsOQG1idhpsH4yCImSbFUOOLazQliZoAvavr8'
headers = {'Authorization': 'Bearer ' + access_token}
file_path = 'sample.mp4'
url = 'http://localhost:5000/api/video_projects'
response = requests.post(url, data={'project_id': '1', 'title': 'Project 1', 'status': 'active', 'description': 'sample description'}, files={'file': open(file_path, 'rb')}, headers=headers)
print(response.json())
```

- If Successful

```bash
{'message': 'Video project created successfully', 'project_id': '1'}
```

- If Video project already exists

```bash
{'message': 'Video project already exists'}
```

- If Token has expired

```bash
{'msg': 'Token has expired'}
```
## Get Video Project

### Get all Video Projects

```py
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDg5MDMxNCwianRpIjoiMDU5OWNhZmMtNDdhYi00M2YzLThlYjItZjgwZGQyMWNhNzQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QxIiwibmJmIjoxNzE0ODkwMzE0LCJjc3JmIjoiNjliNWM0M2MtNThiMS00OWM1LWJkNjYtNjcxZmQ5M2E5ZDA3IiwiZXhwIjoxNzE0ODkzOTE0fQ.ij4WcHOsOQG1idhpsH4yCImSbFUOOLazQliZoAvavr8'
headers = {'Authorization': 'Bearer ' + access_token}
responce = requests.get('http://localhost:5000/api/video_projects/all', headers=headers)
print(responce.text)
```
- If Token has expired

```bash
{'msg': 'Token has expired'}
```
- If Successful

```bash
[{"creation_date":"Sun, 05 May 2024 07:24:44 GMT","description":"sample description 2","project_id":"2","status":"active","thumbnail_path":"uploads/test1/2/thumbnail_sample.mp4.jpeg","title":"Project 2","user_id":"test1","video_path":"uploads/test1/2/sample.mp4"},{"creation_date":"Sun, 05 May 2024 07:26:58 GMT","description":"sample description 1","project_id":"1","status":"active","thumbnail_path":"uploads/test1/1/thumbnail_sample.mp4.jpeg","title":"Project 1","user_id":"test1","video_path":"uploads/test1/1/sample.mp4"}]
```

### Get Specific Video Project
- Change Specific Project ID

```py

access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDg5MDMxNCwianRpIjoiMDU5OWNhZmMtNDdhYi00M2YzLThlYjItZjgwZGQyMWNhNzQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QxIiwibmJmIjoxNzE0ODkwMzE0LCJjc3JmIjoiNjliNWM0M2MtNThiMS00OWM1LWJkNjYtNjcxZmQ5M2E5ZDA3IiwiZXhwIjoxNzE0ODkzOTE0fQ.ij4WcHOsOQG1idhpsH4yCImSbFUOOLazQliZoAvavr8'
headers = {'Authorization': 'Bearer ' + access_token}
responce = requests.get('http://localhost:5000/api/video_projects/<Specific Project ID>', headers=headers)
print(responce.text)
```
#### If Specific Project ID == 1
- If Successful
 ```bash
{"creation_date":"Sun, 05 May 2024 07:26:58 GMT","description":"sample description 1","project_id":"1","status":"active","thumbnail_path":"uploads/test1/1/thumbnail_sample.mp4.jpeg","title":"Project 1","user_id":"test1","video_path":"uploads/test1/1/sample.mp4"}
```
- If Token has expired

```bash
{'msg': 'Token has expired'}
```
## Update  Video Project

- You Can Update Single Field Also
```py
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDg5MDMxNCwianRpIjoiMDU5OWNhZmMtNDdhYi00M2YzLThlYjItZjgwZGQyMWNhNzQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QxIiwibmJmIjoxNzE0ODkwMzE0LCJjc3JmIjoiNjliNWM0M2MtNThiMS00OWM1LWJkNjYtNjcxZmQ5M2E5ZDA3IiwiZXhwIjoxNzE0ODkzOTE0fQ.ij4WcHOsOQG1idhpsH4yCImSbFUOOLazQliZoAvavr8'
headers = {'Authorization': 'Bearer ' + access_token}
responce = requests.put('http://localhost:5000/api/video_projects/2', json={'project_id': '1', 'title': 'Project 1', 'status': 'active', 'description': 'sample description'}, headers=headers)
print(responce.json())
```
- If Successful
```bash
{'message': 'Video project updated successfully'}
```
- If Token has expired

```bash
{'msg': 'Token has expired'}
```

## Delete Video Project
- Change Specific Project ID
```py

access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDg5MDMxNCwianRpIjoiMDU5OWNhZmMtNDdhYi00M2YzLThlYjItZjgwZGQyMWNhNzQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QxIiwibmJmIjoxNzE0ODkwMzE0LCJjc3JmIjoiNjliNWM0M2MtNThiMS00OWM1LWJkNjYtNjcxZmQ5M2E5ZDA3IiwiZXhwIjoxNzE0ODkzOTE0fQ.ij4WcHOsOQG1idhpsH4yCImSbFUOOLazQliZoAvavr8'
headers = {'Authorization': 'Bearer ' + access_token}
responce = requests.get('http://localhost:5000/api/video_projects/<Specific Project ID>', headers=headers)
print(responce.json())
```
- If Token has expired

```bash
{'msg': 'Token has expired'}
```
- If Successful
```bash
{'message': 'Video project deleted successfully'}
```
