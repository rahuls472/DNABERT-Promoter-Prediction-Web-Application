def parse_fasta(file):

    sequences = []

    header = None
    sequence = []

    for line in file:

        line = line.decode("utf-8").strip()

        if not line:
            continue

        if line.startswith(">"):

            if header is not None:

                sequences.append({
                    "id": header,
                    "sequence": "".join(sequence)
                })

            header = line[1:]
            sequence = []

        else:

            sequence.append(line)

    if header is not None:

        sequences.append({
            "id": header,
            "sequence": "".join(sequence)
        })

    return sequences