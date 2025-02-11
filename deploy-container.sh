#!/bin/bash

# Set variables
AWS_ACCOUNT_ID="031675943015"  # Replace with your AWS account ID
AWS_REGION="us-east-1"       # Replace with your AWS region
ECR_REPO="031675943015.dkr.ecr.us-east-1.amazonaws.com/study-buddy/src"
IMAGE_TAG="latest"

# Build the Docker image
echo "Building Docker image..."
docker build -t my-app ./src

# Tag the Docker image
echo "Tagging Docker image..."
docker tag my-app ${ECR_REPO}:${IMAGE_TAG}

# Authenticate Docker with ECR
echo "Authenticating with ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}

# Push the Docker image to ECR
echo "Pushing Docker image to ECR..."
docker push ${ECR_REPO}:${IMAGE_TAG}

echo "Successfully pushed Docker image to ECR: ${ECR_REPO}:${IMAGE_TAG}"
