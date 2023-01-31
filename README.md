# This is course CS 419 source code - Image Retrieval

**DESCRIPTION:** This project is using pretrained model at: https://github.com/filipradenovic/cnnimageretrieval-pytorch on Oxford5k dataset - A dataset of building, so that it would only perform accurately with building images when testing.

## Prerequisites
In order to run this app you will need:

1. Docker + WSL2
1. pip
1. All the rest (data + networks) is automatically downloaded with our scripts


## To run the application, please follow these below steps:

- Step 0: Download and install VSCode, install "Live server" extension to host the UI, start docker desktop
- Step 1: Clone the repo
- Step 2: Run ```cd CS419``` to access into the repo's directory
- Step 3: Run ```source start_app.sh``` to start the app image and automatically download the dataset to test (default is oxford5k dataset)
- Step 4: Open file index.html with Live server extension to start testing
- Step 5: Choose image, crop the interested area and hit the submit, then wait about a second to see the retrieved result

## Please note that: 

> The default number of image to be returned is 16, so the backend will automatically return top 16 matched images. The mechanism is letting backend to extract feature vector for each of images in the dataset (took long time), then save these features in backend/features.pt along with all_images.txt is the image file paths respectively. The current feature.pt & all_images.txt are belonging to oxford5k dataset, if you would like to using another dataset, please follow the instrucion to prepare the features:

- Step 1: Place dataset folder which contains images into backend/data
- Step 2: Adjust the DATASET_PATH to recently added image folder
- Step 3: Run ```cd backend; docker-compose -f docker/docker-compose.yml up --build``` to rebuild and start backend
- Step 4: Run ```curl --location --request POST 'localhost:8000/app/v1/extract-feature'``` to start extracting dataset
- Step 5: If extract process successfully, you can start tesing new dataset and images
