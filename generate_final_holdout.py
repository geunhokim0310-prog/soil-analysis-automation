import csv
import random


# ==========================================
# Final Hold-out
# 기존 개발 데이터와 다른 seed 사용
# ==========================================

random.seed(9137)


raw_blocks = []
answer_rows = []


# ==========================================
# 100건 생성
# ==========================================

for i in range(1, 101):

    sample_id = f"FINAL-{i:03d}"

    pb = round(
        random.uniform(15, 380),
        2
    )

    cd = round(
        random.uniform(0.3, 9.0),
        2
    )

    weight = round(
        random.uniform(2.985, 3.015),
        3
    )

    format_type = (
        (i - 1) % 5
    ) + 1


    # ======================================
    # 형식 1
    # ======================================

    if format_type == 1:

        block = (
            f"CASE IDENTIFIER : {sample_id}\n"
            f"Pb reading -> {pb} | mg/kg\n"
            f"Cd reading -> {cd} | mg/kg\n"
            f"Portion weighed -> {weight} | g\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    # ======================================
    # 형식 2
    # ======================================

    elif format_type == 2:

        block = (
            f"material_ref={sample_id}\n"
            f"LEAD_RESULT({pb}) [ppm]\n"
            f"CADMIUM_RESULT({cd}) [ppm]\n"
            f"ALIQUOT_MASS({weight}) [gram]\n"
        )

        pb_unit = "ppm"
        cd_unit = "ppm"
        weight_unit = "gram"


    # ======================================
    # 형식 3
    # ======================================

    elif format_type == 3:

        block = (
            f"=== METAL ANALYSIS ===\n"
            f"BOTTLE REF .... {sample_id}\n"
            f"Lead measured .... {pb} mg/kg\n"
            f"Cadmium measured . {cd} mg/kg\n"
            f"Sample portion .... {weight} g\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
        weight_unit = "g"


    # ======================================
    # 형식 4
    # ======================================

    elif format_type == 4:

        block = (
            f"<entry id='{sample_id}'>\n"
            f"lead_value={pb}; lead_unit=ppm\n"
            f"cadmium_value={cd}; cadmium_unit=ppm\n"
            f"sample_mass={weight}; mass_unit=g\n"
            f"</entry>\n"
        )

        pb_unit = "ppm"
        cd_unit = "ppm"
        weight_unit = "g"


    # ======================================
    # 형식 5
    # ======================================

    else:

        block = (
            f"Container Tag :: {sample_id}\n"
            f"Measured Lead [{pb}] mg/kg\n"
            f"Measured Cadmium [{cd}] mg/kg\n"
            f"Prepared Portion [{weight}] grams\n"
        )

        pb_unit = "mg/kg"
        cd_unit = "mg/kg"
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
# RAW DATA 저장
# ==========================================

with open(
    "input/final_holdout_100_raw.txt",
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
    "input/final_holdout_expected_100.csv",
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
print("========================================")
print(" Final Hold-out 데이터 생성 완료")
print("========================================")
print()

print(
    "RAW DATA:"
)

print(
    "input/final_holdout_100_raw.txt"
)

print()

print(
    "정답 데이터:"
)

print(
    "input/final_holdout_expected_100.csv"
)

print()

print(
    "새로운 RAW 형식: 5종"
)

print(
    "형식당 시료 수: 20건"
)

print(
    "총 시료 수: 100건"
)

print(
    "검증 데이터 포인트: 700개"
)