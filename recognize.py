import torch
from PIL import Image
import torchvision.transforms as transforms
from models.crnn import CRNN
from utils import strLabelConverter

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'  # Adjust if needed
converter = strLabelConverter(alphabet)
nclass = len(alphabet) + 1
model = CRNN(imgH=32, nc=1, nclass=nclass, nh=256).to(device)
model.eval()

model_path = 'weights/crnn.pth'
model.load_state_dict(torch.load(model_path, map_location=device, weights_only=False))

transform = transforms.Compose([
    transforms.Resize((32, 100)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

img_path = 'test13.png'
img = Image.open(img_path).convert('L')
img = transform(img).unsqueeze(0).to(device)
with torch.no_grad():
    preds = model(img)
    _, preds = preds.max(2)
    preds = preds.transpose(1, 0).contiguous().view(-1)
    preds_size = torch.IntTensor([preds.size(0)])
    text = converter.decode(preds.data, preds_size.data, raw=False)
print(f"Predicted text: {text}")