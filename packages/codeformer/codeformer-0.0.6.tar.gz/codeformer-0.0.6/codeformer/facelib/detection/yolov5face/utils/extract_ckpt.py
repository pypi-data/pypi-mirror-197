import torch
import sys
from pathlib import Path

weights_dir = Path(__file__).parent.parent.parent.parent / "weights/facelib"
print("extract_ckpt", weights_dir)

sys.path.insert(0, "./facelib/detection/yolov5face")
model = torch.load("facelib/detection/yolov5face/yolov5n-face.pt", map_location="cpu")[
    "model"
]
torch.save(model.state_dict(), f"{weights_dir}/facelib/yolov5n-face.pth")
