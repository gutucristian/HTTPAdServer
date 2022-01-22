#! bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 255286435885.dkr.ecr.us-east-1.amazonaws.com

echo 'Building Docker image...'
docker build -t http-ad-server .

echo 'Tagging image as latest...'
docker tag http-ad-server:latest 255286435885.dkr.ecr.us-east-1.amazonaws.com/http-ad-server:latest

echo 'Pushing image to ECR...'
docker push 255286435885.dkr.ecr.us-east-1.amazonaws.com/http-ad-server:latest