import torch
import torchvision.models as models
import torchvision.transforms as transforms

def load_resnet50():
    base = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    model = torch.nn.Sequential(*list(base.children())[:-1])
    model.eval()
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    return model, transform

def extract_deep_features(img_pil, model, transform):
    """ResNet50 → 2048D"""
    x = transform(img_pil).unsqueeze(0)
    with torch.no_grad():
        feat = model(x).squeeze().numpy()
    return feat  # (2048,)