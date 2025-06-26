import torch
weights = torch.load('weights/crnn.pth', map_location='cpu', weights_only=False)
print(list(weights.keys())[:10])  # Should include cnn.conv0.weight, etc.