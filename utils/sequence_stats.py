def sequence_statistics(sequence: str):

    sequence = sequence.upper()

    length = len(sequence)

    a = sequence.count("A")
    t = sequence.count("T")
    g = sequence.count("G")
    c = sequence.count("C")

    at = a + t
    gc = g + c

    at_percent = round((at / length) * 100, 2)
    gc_percent = round((gc / length) * 100, 2)

    return {

        "length": length,

        "A": a,
        "T": t,
        "G": g,
        "C": c,

        "AT_percent": at_percent,
        "GC_percent": gc_percent
    }