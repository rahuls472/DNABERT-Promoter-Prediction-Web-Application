from flask import Flask, render_template, request
from modeling.classifier_model import DNABERTPredictor
from utils.fasta_parser import parse_fasta
from utils.validator import allowed_file, valid_dna
from utils.sequence_stats import sequence_statistics

app = Flask(__name__)

predictor = DNABERTPredictor()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # =====================================
    # Text Area Prediction
    # =====================================

    sequence = request.form.get("sequence", "").strip()

    if sequence:

        sequence = sequence.upper()

        if not valid_dna(sequence):

            return render_template(
                "result.html",
                error="Invalid DNA sequence. Only A, T, G and C are allowed."
            )

        prediction = predictor.predict(sequence)

        stats = sequence_statistics(sequence)

        result = {
            **prediction,
            **stats
        }

        return render_template(
            "result.html",
            single_result=result
        )
    
    # =====================================
    # FASTA Upload Prediction
    # =====================================

    file = request.files.get("file")

    if file:

        if file.filename == "":

            return render_template(
                "result.html",
                error="Please choose a FASTA file."
            )

        if not allowed_file(file.filename):

            return render_template(
                "result.html",
                error="Only .fa, .fasta and .txt files are supported."
            )

        fasta_sequences = parse_fasta(file)

        if len(fasta_sequences) == 0:

            return render_template(
                "result.html",
                error="No sequences found inside the uploaded FASTA file."
            )

        results = []

        for record in fasta_sequences:

            sequence = record["sequence"].upper()

            if not valid_dna(sequence):

                results.append({

                    "id": record["id"],

                    "prediction": "Invalid Sequence",

                    "confidence": "-",

                    "length": len(sequence),

                    "A": "-",
                    "T": "-",
                    "G": "-",
                    "C": "-",

                    "AT_percent": "-",
                    "GC_percent": "-"

                })

                continue

            prediction = predictor.predict(sequence)

            stats = sequence_statistics(sequence)

            results.append({

                "id": record["id"],

                **prediction,

                **stats

            })

        return render_template(
            "result.html",
            results=results
        )

    return render_template(
        "result.html",
        error="Please provide a DNA sequence or upload a FASTA file."
    )


if __name__ == "__main__":
    app.run(debug=True)