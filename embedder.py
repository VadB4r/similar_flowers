import torch
from PIL import Image
from torchvision.transforms import Compose, Resize, ToTensor


class Embedder:

    def __init__(self, path_to_weights="./models/vgg_flower_trained.pt"):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load(path_to_weights, weights_only=False, map_location=torch.device('cpu')).to(self.device)
        self.model.classifier = self.model.classifier[:-3]
        self.transform = Compose(
            [
                Resize((224, 224)),
                ToTensor()
            ]
        )

    def get_embedding(self, path_to_image):
        img = Image.open(path_to_image)
        img = self.transform(img).to(self.device).unsqueeze(0)
        vec = self.model(img).cpu().detach().numpy()[0]
        return vec

