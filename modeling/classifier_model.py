import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class DNABERTPredictor:

    def __init__(self):
        self.model_name = "rahuls472/DNABERT-Promoter-Classifier"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

        self.model.eval()

        self.labels = {
            0: "Non-Promoter",
            1: "Promoter"
        }

    def generate_kmers(self, sequence: str, k: int = 6):
        """
        Convert DNA sequence into overlapping k-mers.

        Example:
        ATGCGTA

        becomes

        ATGCGT TGCGTA
        """
        return " ".join(
            sequence[i:i+k]
            for i in range(len(sequence) - k + 1)
        )

    def predict(self, sequence: str):

        # Clean sequence
        sequence = sequence.strip().upper()

        # Convert to 6-mers
        kmer_sequence = self.generate_kmers(sequence)

        # Tokenize
        inputs = self.tokenizer(
            kmer_sequence,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=512
        )

        with torch.no_grad():

            outputs = self.model(**inputs)

            probabilities = torch.softmax(outputs.logits, dim=1)

            predicted_class = torch.argmax(
                probabilities,
                dim=1
            ).item()

            confidence = probabilities[
                0
            ][predicted_class].item()

        return {
            "prediction": self.labels[predicted_class],
            "label": predicted_class,
            "confidence": round(confidence * 100, 2)
        }