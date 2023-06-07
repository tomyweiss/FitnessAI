import torch
import torch.nn as nn
import torchvision.transforms as transforms
import pickle
from PIL import Image
import torch.nn.functional as F

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
weights_path = '/Users/rotemcohen/FitnessAI/CNN - Accuracy/Bench/model_weights.pickle'


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

# Example usage
image_path = '/Users/rotemcohen/FitnessAI/models/data/for_test/frame4.jpg'
prediction = predict_image(image_path)
print(f"The image is {prediction}.")
