import os
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import torchvision.transforms as transforms

class DeepFakeDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        for label in ['AI generated', 'Real images']:
            dir_path = os.path.join(root_dir, label.replace(' ', '_'))
            if not os.path.exists(dir_path):
                continue
            for file in os.listdir(dir_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    self.images.append(os.path.join(dir_path, file))
                    self.labels.append(0 if label == 'Real images' else 1)
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image = Image.open(self.images[idx]).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

# Define transforms once for both datasets
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

# Create dataset instances
midjourney_dataset = DeepFakeDataset(root_dir='MidJourney', transform=transform)
stable_diffusion_dataset = DeepFakeDataset(root_dir='StableDiffusion', transform=transform)
