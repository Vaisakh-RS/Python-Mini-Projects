FROM python:3.12-slim

#container's working dir
WORKDIR /app 
#copy requirements.txt to app folder
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
#copy everything into the project folder
COPY . .
CMD [ "python", "-m" , "src.LogReader" ]
