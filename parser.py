import re


def parse_raw_data(text):
    pattern = re.compile(
        r"Sample ID:\s*(?P<sample_id>[^\n]+).*?"
        r"Pb:\s*(?P<pb>[\d.]+)\s*mg/kg.*?"
        r"Cd:\s*(?P<cd>[\d.]+)\s*mg/kg.*?"
        r"Weight:\s*(?P<weight>[\d.]+)\s*g",
        re.DOTALL
    )

    samples = []

    for match in pattern.finditer(text):
        sample = {
            "sample_id": match.group("sample_id").strip(),
            "Pb": float(match.group("pb")),
            "Cd": float(match.group("cd")),
            "weight_g": float(match.group("weight"))
        }

        samples.append(sample)

    return samples