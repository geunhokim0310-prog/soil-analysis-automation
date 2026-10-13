import csv
import random


random.seed(2026)


raw_blocks = []
answer_rows = []


for i in range(1, 101):

    sample_id = f"AI-{i:03d}"

    pb = round(
        random.uniform(20, 350),
        2
    )

    cd = round(
        random.uniform(0.5, 8.0),
        2
    )

    weight = round(
        random.uniform(2.990, 3.010),
        3
    )

    # ======================================
    # 서로 다른 RAW 형식 4종
    # ======================================

    format_type = i % 4


    # 형식 1
    if format_type == 1:

        block = (
            f"Sample ID: {sample_id}\n"
            f"Pb: {pb} mg/kg\n"
            f"Cd: {cd} mg/kg\n"
            f"Weight: {weight} g\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    # 형식 2
    elif format_type == 2:

        block = (
            f"[SAMPLE RESULT]\n"
            f"SAMPLE_NO = {sample_id}\n"
            f"Lead(Pb) : {pb} ppm\n"
            f"Cadmium(Cd) : {cd} ppm\n"
            f"Sample Weight = {weight} gram\n"
        )

        pb_unit = "ppm"
        cd_unit = "ppm"
        weight_unit = "gram"


    # 형식 3
    elif format_type == 3:

        block = (
            f"--- Analysis Report ---\n"
            f"ID => {sample_id}\n"
            f"Pb concentration = {pb} mg/kg\n"
            f"Cd concentration = {cd} mg/kg\n"
            f"Weight(g) = {weight}\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    # 형식 4
    else:

        block = (
            f"Sample: {sample_id}\n"
            f"Element Pb = {pb} mg/kg\n"
            f"Element Cd = {cd} mg/kg\n"
            f"Weighed Mass = {weight} g\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    raw_blocks.append(block)


    answer_rows.append([
        sample_id,
        pb,
        pb_unit,
        cd,
        cd_unit,
        weight,
        weight_unit
    ])


# ==========================================
# RAW DATA 저장
# ==========================================

with open(
    "input/ai_test_100_raw.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(raw_blocks)
    )


# ==========================================
# 정답 데이터 저장
# ==========================================

with open(
    "input/ai_expected_100.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "sample_id",
        "Pb",
        "Pb_unit",
        "Cd",
        "Cd_unit",
        "weight_g",
        "weight_unit"
    ])

    writer.writerows(
        answer_rows
    )


print("AI 검증용 100건 데이터 생성 완료!")
print(
    "RAW DATA: "
    "input/ai_test_100_raw.txt"
)
print(
    "정답 데이터: "
    "input/ai_expected_100.csv"
)