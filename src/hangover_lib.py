import torch
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModel


class hangover_detector:
    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
        self.preprocess = AutoProcessor.from_pretrained(
            "google/siglip-base-patch16-224"
        )
        self.classes = [
            "A person with a hangover",
            "A person feeling ok",
            "Still-life",
        ]


    def detect(self, url):
        img = Image.open(requests.get(url, stream=True).raw)
        inputs = self.preprocess(text=self.classes, images=img, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits_per_image
        probs = torch.sigmoid(logits)
        print(probs)
        class_ = self.get_class(probs[0])
        description = self.get_description(probs[0])
        return class_, probs, description

    # def get_probabilities(self, image_input):
    #     with torch.no_grad():
    #         image_features = self.model.encode_image(image_input)
    #         text_features = self.model.encode_text(self.tokens)
    #     image_features /= image_features.norm(dim=-1, keepdim=True)
    #     text_features /= text_features.norm(dim=-1, keepdim=True)
    #     similarities = (100.0 * image_features @ text_features.T).softmax(
    #         dim=-1
    #     )
    #     return similarities[0]

    def get_class(self, similarities):
        _, indices = similarities.topk(1)
        return self.classes[indices]

    def get_description(self, probs):
        print("Probs inside description: ", probs)
        if probs[-1] >= 0.5:
            return "Where do I look?"
        if probs[0] > 0.7:
            return "Oh dear, you should not be working today."
        if probs[0] >= 0.3:
            return "Drink some water and take a nap."
        if probs[0] >= 0.2:
            return "Off to work you go."
        return "Healthy as a horse. Grab a beer."
