import torch
import torch.nn as nn
import torchvision.transforms as transforms
import pickle
import numpy as np
from PIL import Image
import torch.nn.functional as F
import os

def test_squat():
    # Set the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define the network model
    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            
            self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
            self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
            self.fc1 = nn.Linear(32 * 32 * 32, 256)
            self.fc2 = nn.Linear(256, 128)
            self.fc3 = nn.Linear(128, 2)  # Assuming 2 classes: good and not good
            
        def forward(self, x):
            x = F.relu(self.conv1(x))
            x = F.max_pool2d(x, kernel_size=2, stride=2)
            x = F.relu(self.conv2(x))
            x = F.max_pool2d(x, kernel_size=2, stride=2)
            x = x.view(x.size(0), -1)  # Flatten the input tensor
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    # Create an instance of the network model
    net = Net().to(device)

    # Specify the file path of the weights
    weights_path = r'C:\Users\mosac\Git Repositories\FitnessAI\fitnessai_app\models\data\Squat\model_weights.pickle'
    #weights_path = '/Users/rotemcohen/FitnessAI/CNN - Accuracy/squats/model_weights.pickle'

    # Load the weights from the pickle file
    with open(weights_path, 'rb') as file:
        weights = pickle.load(file)

    # Update the network model with the loaded weights
    net.load_state_dict(weights)

    # Define the transformations for the input image
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        transforms.Resize((128, 128))
    ])

    # Function to predict if an image is good or not good
    def predict_image(image_path):
        # Load and transform the image
        image = Image.open(image_path)
        image = transform(image).unsqueeze(0).to(device)
        
        # Make a prediction
        with torch.no_grad():
            outputs = net(image)
            _, predicted = torch.max(outputs.data, 1)
        
        # Convert the prediction to a human-readable label
        label = "not good" if predicted.item() == 0 else "good"
        
        return label

    # Function to determine if the folder is good or not good
    def determine_folder_status(folder_path):
        image_files = os.listdir(folder_path)
        num_images = len(image_files)
        predictions = []

        # Make predictions for each image in the folder
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            prediction = predict_image(image_path)
            predictions.append(prediction)

        # Print the predictions for each image
        print("Predictions for each image:")
        for image_file, prediction in zip(image_files, predictions):
            print(f"{image_file}: {prediction}")

        # Determine the majority prediction
        good_count = predictions.count("good")
        not_good_count = predictions.count("not good")
        
        # Determine the folder status based on the majority prediction
        if good_count / num_images > 0.5:
            folder_status = "good"
        elif not_good_count / num_images > 0.5:
            folder_status = "not good"
        else:
            folder_status = "undetermined"

        print(predictions)
        return folder_status

    # Example usage
    folder_path = r'C:\Users\mosac\Git Repositories\FitnessAI\fitnessai_app\models\data\Flexing OR Stretching'
    #folder_path = '/Users/rotemcohen/FitnessAI/models/data/for_test'
    folder_status = determine_folder_status(folder_path)
    print(f"The Squat performed {folder_status}.")


    if folder_status == 'not good':
        return 0
    else:
        return 1
     