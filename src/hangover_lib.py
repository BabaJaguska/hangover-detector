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
        self.classes = ["A person with a hangover", "A person feeling ok"]
        self.tokis = torch.cat(
            [clip.tokenize(f"a photo of a {d}") for d in self.classes]
        ).to(self.device)

    def detect(self, url):
        img = Image.open(requests.get(url, stream=True).raw)
        image_input = self.preprocess(img).unsqueeze(0).to(self.device)
        prob = self.get_probability(image_input)
        description = self.get_description(prob)
        return prob, description

    def get_probability(self, image_input):
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            text_features = self.model.encode_text(self.tokis)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, _ = similarity[0].topk(2)
        return values[0].item()

    def get_description(self, hangover_prob):
        if hangover_prob > 0.7:
            return "Oh dear, you should not be working today."
        elif hangover_prob >= 0.5:
            return "Drink some water and take a nap."
        elif hangover_prob >= 0.3:
            return "Off to work you go."
        else:
            return "Healthy as a horse. Grab a beer."
