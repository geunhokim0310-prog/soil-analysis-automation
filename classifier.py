def classify_sample(sample, standards):
    exceeded = []

    for metal in ["Pb", "Cd"]:
        if sample[metal] > standards[metal]:
            exceeded.append(metal)

    if exceeded:
        result = "정밀조사 대상"
    else:
        result = "기준 이내"

    sample["exceeded_items"] = exceeded
    sample["result"] = result

    return sample