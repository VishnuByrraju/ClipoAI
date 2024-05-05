import requests
import os
import json

# Sign up
responce = requests.post('http://localhost:5000/api/signup', data={'email': 'test1@gmail.com', 'username': 'test1', 'password': 'test1'})
print(responce.json())

# Login and get access token
responce = requests.post('http://localhost:5000/api/login', data={'username': 'test1', 'password': 'test1'})
print(responce.json())

# Create a video project
headers = {'Authorization': 'Bearer ' + responce.json()['access_token']}

# Create a video project
file_path = 'sample.mp4'
url = 'http://localhost:5000/api/video_projects'
response = requests.post(url, data={'project_id': '1', 'title': 'Project 1', 'status': 'active', 'description': 'sample description 1'}, files={'file': open(file_path, 'rb')}, headers=headers)
print(response.json())


# Get all video projects
responce = requests.get('http://localhost:5000/api/video_projects/all', headers=headers)
print(responce.text)

# Get a specific video project
responce = requests.get('http://localhost:5000/api/video_projects/1', headers=headers)
print(responce.text)

# Update a video project
responce = requests.put('http://localhost:5000/api/video_projects/2', json={'project_id': '1', 'title': 'Project 1', 'status': 'active', 'description': 'sample description'}, headers=headers)
print(responce.json())

# Delete a video project Specific project
responce = requests.delete('http://localhost:5000/api/video_projects/1', headers=headers)
print(responce.json())

