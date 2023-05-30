# Problem Statement
 Build an appropriate Machine Learning Model that will help various Zomato Restaurants to predict their respective Ratings based on certain features.
 
The main goal of this project is to perform extensive Exploratory Data Analysis(EDA) on the Zomato Dataset and build an appropriate Machine Learning Model that will help various Zomato Restaurants to predict their respective Ratings based on certain features.

## How to run?

Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.


### Dataset information
The training set contains 57000 examples in total number of Attributes is 13.

## Tech Stack Used

1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions

## How to run?

Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## Project Pipeline
<p align="center">
  <img src="images\Ratings_training_pipline.png" width="500" title="hover text">
</p>

## Project Archietecture

![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)

## Deployment Archietecture

![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)

### Step 1: Clone the repository

```bash
git clone https://github.com/MaheshKumarMK/Restaurant-rating-prediction.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n venv python=3.7.6 -y
```

```bash
conda activate venv
```

### Step 3 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable

```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGODB_URL>

```

### Step 5 - Run the application server

```bash
python main.py
  or
uvicorn main:app
```

### Step 6. Train application

```bash
http://localhost:8080/train

```

```

## Run locally

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image

```
docker build -t ratings-predictions . 

```

3. Run the Docker image

```
docker run -d -e AWS_ACCESS_KEY_ID="${{ secrets.AWS_ACCESS_KEY_ID }}" -e AWS_SECRET_ACCESS_KEY="${{ secrets.AWS_SECRET_ACCESS_KEY }}" -e AWS_DEFAULT_REGION="${{ secrets.AWS_DEFAULT_REGION }}" -e MONGODB_URL="${{ secrets.MONGODB_URL }}" -p 8080:8080 ratings-predictions
```
