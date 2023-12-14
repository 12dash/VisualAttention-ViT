import pickle
import struct
import numpy as np

import torch
from torch.utils.data import Dataset

class Cifar(Dataset):
    def __init__(self, img_gzip, label_name_zip, base_dir):
        self.gzip_path = [base_dir + _ for _ in img_gzip] 
        self.label_name_gzip = base_dir + label_name_zip
        self.imgs, self.labels = [], []
        self.label_name = []
        self.load_label()
        self.load()
    
    def load_label(self):
        with open(self.label_name_gzip,'rb') as f:
            data = pickle.load(f, encoding='bytes')
            self.label_name = data['label_names']
        
    def load(self):
        for file_path in self.gzip_path:
            with open(file_path,'rb') as f:
                data = pickle.load(f, encoding='bytes')
                self.imgs.append(data['data'])
                self.labels.append(data['labels'])
        self.imgs, self.labels = np.concatenate(self.imgs), np.concatenate(self.labels)
       
    def __len__(self):
        return self.imgs.shape[0]

    def __getitem__(self, idx):
        img = torch.tensor(self.imgs[idx], dtype=torch.float32)/255.0
        label = torch.tensor(self.labels[idx])
        return img, label