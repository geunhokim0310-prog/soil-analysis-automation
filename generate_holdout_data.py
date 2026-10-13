import csv
import random


# ==========================================
# 재현 가능한 Hold-out 데이터
# ==========================================

random.seed(777)


raw_blocks = []
answer_rows = []


# ==========================================
# 100건 생성
# ==========================================

for i in range(1, 101):

    sample_id = f"HOLD-{i:03d}"

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
    # 5종의 새로운 RAW 형식
    # 기존 프롬프트에 직접 예시하지 않은 형태
    # ======================================

    format_type = (
        (i - 1) % 5
    ) + 1


    # --------------------------------------
    # 형식 1
    # --------------------------------------

    if format_type == 1:

        block = (
            f"REPORT NO. {sample_id}\n"
            f"Lead result........{pb} mg/kg\n"
            f"Cadmium result.....{cd} mg/kg\n"
            f"Mass used..........{weight} g\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    # --------------------------------------
    # 형식 2
    # --------------------------------------

    elif format_type == 2:

        block = (
            f"Specimen = {sample_id}\n"
            f"Metal Pb [mg/kg] {pb}\n"
            f"Metal Cd [mg/kg] {cd}\n"
            f"Initial mass [g] {weight}\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    # --------------------------------------
    # 형식 3
    # --------------------------------------

    elif format_type == 3:

        block = (
            f"LAB CODE :: {sample_id}\n"
            f"LEAD ASSAY :: {pb} ppm\n"
            f"CADMIUM ASSAY :: {cd} ppm\n"
            f"TEST MASS :: {weight} gram\n"
        )

        pb_unit = "ppm"
        cd_unit = "ppm"
        weight_unit = "gram"


    # --------------------------------------
    # 형식 4
    # --------------------------------------

    elif format_type == 4:

        block = (
            f"Record#{sample_id}\n"
            f"Pb-value={pb}; unit=mg/kg\n"
            f"Cd-value={cd}; unit=mg/kg\n"
            f"Mass-value={weight}; unit=g\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    # --------------------------------------
    # 형식 5
    # --------------------------------------

    else:

        block = (
            f"<SoilRecord>\n"
            f"Code {sample_id}\n"
            f"Lead {pb} ppm\n"
            f"Cadmium {cd} ppm\n"
            f"Mass {weight} grams\n"
            f"</SoilRecord>\n"
        )

        pb_unit = "ppm"
        cd_unit = "ppm"
        weight_unit = "grams"


    raw_blocks.append(
        block
    )


    answer_rows.append([
        sample_id,
        pb,
        pb_unit,
        cd,
        cd_unit,
        weight,
        weight_unit,
        format_type
    ])


# ==========================================
# Hold-out RAW DATA 저장
# ==========================================

with open(
    "input/holdout_100_raw.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(raw_blocks)
    )


# ==========================================
# Hold-out 정답 데이터 저장
# ==========================================

with open(
    "input/holdout_expected_100.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(
        file
    )

    writer.writerow([
        "sample_id",
        "Pb",
        "Pb_unit",
        "Cd",
        "Cd_unit",
        "weight_g",
        "weight_unit",
        "format_type"
    ])

    writer.writerows(
        answer_rows
    )


print()
print(
    "Hold-out 검증용 100건 생성 완료!"
)

print(
    "RAW DATA:"
)

print(
    "input/holdout_100_raw.txt"
)

print(
    "정답 데이터:"
)

print(
    "input/holdout_expected_100.csv"
)

print()

print(
    "형식 수: 5종"
)

print(
    "형식당 시료 수: 20건"
)

print(
    "총 시료 수: 100건"
)