# Dockerized Express frontend + Flask backend

Structure:

- frontend/: Express app serving a contact form and forwarding submissions to the Flask backend
- backend/: Flask app that accepts form submissions
- docker-compose.yaml: builds and runs both services on a shared network

Quick start (replace placeholders for pushing images):

Build & run locally with Docker Compose:
```bash
cd "C:/Users/Sumukh/OneDrive/Desktop/Tutedude Devops/Docker"
docker-compose build
docker-compose up
```

Frontend: http://localhost:3000
Backend: http://localhost:5000

Build, tag and push images to Docker Hub (example):
```bash
# build images via compose
docker-compose build

# tag images (replace DOCKERHUB_USER)
docker tag flask_backend:latest DOCKERHUB_USER/flask-backend:latest
docker tag express_frontend:latest DOCKERHUB_USER/express-frontend:latest

# login and push
docker login
docker push DOCKERHUB_USER/flask-backend:latest
docker push DOCKERHUB_USER/express-frontend:latest
```

Push code to GitHub:
```bash
git init
git add .
git commit -m "Add dockerized frontend and backend"
git remote add origin https://github.com/<your-username>/<repo>.git
git branch -M main
git push -u origin main
```

Notes:
- The Express frontend forwards form POSTs server-side to the Docker Compose service name `backend:5000` so cross-container traffic works.
- Replace `DOCKERHUB_USER` and GitHub URL with your values before pushing.
