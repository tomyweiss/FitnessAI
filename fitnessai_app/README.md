Fineness-AI App

DataBase - 

Docker Requirements (Windows users):
1. Download Docker Desktop - If you cannot open the Docker Desktop Application (You gets warning and the app     closes) - Perform stages 2 to 5.

2. Enable windows hyper-v
3. Download WSL2 - https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
4. Run the following command in the powershell:wsl --set-default-version 2
5. Make sure you can open Docker Desktop
6. Run the following command from the powershell:docker run -d -p 27017:27017 --name mongodb mongo

How to run? 
1. docker run -d -p 27017:27017 --name mongodb mongo


Server:

Prerequisite - TBD

How to run?
1. cd fitnessai-app
2. python server.py

Client - 

Prerequisite - TBD

How to run?
1. cd fitnessai-app
2. cd client
3. npm install
4. npm start