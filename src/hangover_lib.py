import torch
import requests
from PIL import Image
import clip


class hangover_detector:
    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.classes = [
            "A person with a hangover",
            "A person feeling ok",
            "Still-life",
        ]
        self.tokens = torch.cat(
            [clip.tokenize(f"a photo of a {d}") for d in self.classes]
        ).to(self.device)

    def detect(self, url):
        img = Image.open(requests.get(url, stream=True).raw)
        image_input = self.preprocess(img).unsqueeze(0).to(self.device)
        probs = self.get_probabilities(image_input)
        class_ = self.get_class(probs)
        description = self.get_description(probs)
        return class_, probs, description

    def get_probabilities(self, image_input):
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            text_features = self.model.encode_text(self.tokens)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarities = (100.0 * image_features @ text_features.T).softmax(
            dim=-1
        )
        return similarities[0]

    def get_class(self, similarities):
        _, indices = similarities.topk(1)
        return self.classes[indices]

    def get_description(self, probs):
        if probs[-1] >= 0.5:
            return "Where do I look?"
        if probs[0] > 0.7:
            return "Oh dear, you should not be working today."
        if probs[0] >= 0.5:
            return "Drink some water and take a nap."
        if probs[0] >= 0.3:
            return "Off to work you go."
        return "Healthy as a horse. Grab a beer."
