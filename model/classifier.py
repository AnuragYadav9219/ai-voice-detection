import random

def classify(features):
    confidence = random.uniform(0.65, 0.95)
    label = "AI_GENERATED" if confidence > 0.75 else "HUMAN"
    return label, round(confidence, 2)