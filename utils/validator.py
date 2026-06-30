import re

ALLOWED_EXTENSIONS = {"fa", "fasta", "txt"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def valid_dna(sequence):

    sequence = sequence.strip().upper()

    return re.fullmatch(r"[ATGC]+", sequence) is not None