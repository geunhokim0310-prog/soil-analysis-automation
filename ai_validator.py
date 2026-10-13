import csv
import math

from ai_parser import parse_with_ai


# ==========================================
# 설정
# ==========================================

RAW_PATH = "input/ai_test_100_raw.txt"
EXPECTED_PATH = "input/ai_expected_100.csv"

BATCH_SIZE = 10


# ==========================================
# 단위 표준화 함수
# ==========================================

def canonical_unit(unit):

    if unit is None:
        return None

    unit = str(unit).lower().strip()

    if unit in {
        "",
        "null",
        "none",
        "n/a"
    }:
        return None

    aliases = {
        "g": "g",
        "gram": "g",
        "grams": "g",

        "mg/kg": "mg/kg",
        "ppm": "ppm"
    }

    return aliases.get(
        unit,
        unit
    )


# ==========================================
# 1. 정답 데이터 읽기
# ==========================================

expected_results = {}

with open(
    EXPECTED_PATH,
    "r",
    encoding="utf-8-sig"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        sample_id = row["sample_id"]

        expected_results[sample_id] = {
            "sample_id": sample_id,

            "Pb": float(
                row["Pb"]
            ),

            "Pb_unit": canonical_unit(
                row["Pb_unit"]
            ),

            "Cd": float(
                row["Cd"]
            ),

            "Cd_unit": canonical_unit(
                row["Cd_unit"]
            ),

            "weight_g": float(
                row["weight_g"]
            ),

            "weight_unit": canonical_unit(
                row["weight_unit"]
            )
        }


# ==========================================
# 2. RAW DATA 읽기
# ==========================================

with open(
    RAW_PATH,
    "r",
    encoding="utf-8"
) as file:

    raw_text = file.read()


# ==========================================
# 3. 시료 블록 분리
# ==========================================

raw_blocks = [
    block.strip()
    for block in raw_text.strip().split("\n\n")
    if block.strip()
]


print()
print("========================================")
print(" AI Parser 100건 정확도 검증")
print("========================================")
print()

print(
    "RAW 시료 블록 수:",
    len(raw_blocks)
)

print(
    "정답 시료 수:",
    len(expected_results)
)

print()


# ==========================================
# 4. 10건씩 AI Parser 실행
# ==========================================

actual_results = {}


for start in range(
    0,
    len(raw_blocks),
    BATCH_SIZE
):

    end = min(
        start + BATCH_SIZE,
        len(raw_blocks)
    )

    batch_blocks = raw_blocks[
        start:end
    ]

    batch_text = "\n\n".join(
        batch_blocks
    )

    batch_number = (
        start // BATCH_SIZE
    ) + 1

    print(
        f"[Batch {batch_number}] "
        f"{start + 1}~{end}번 AI 추출 중..."
    )

    try:

        batch_results = parse_with_ai(
            batch_text
        )

    except Exception as error:

        print(
            f"    Batch {batch_number} 실패:"
        )

        print(
            "   ",
            error
        )

        print(
            "    → 해당 Batch를 "
            "1건씩 다시 검사합니다."
        )

        # ----------------------------------
        # Batch 실패 시 1건씩 재시도
        # ----------------------------------

        for block in batch_blocks:

            try:

                retry_results = parse_with_ai(
                    block
                )

                for result in retry_results:

                    sample_id = result[
                        "sample_id"
                    ]

                    actual_results[
                        sample_id
                    ] = result

            except Exception as retry_error:

                print(
                    "      개별 시료 실패:",
                    retry_error
                )

        continue


    print(
        f"    AI 추출 건수: "
        f"{len(batch_results)}"
    )


    for result in batch_results:

        sample_id = result[
            "sample_id"
        ]

        actual_results[
            sample_id
        ] = result


# ==========================================
# 5. ID 누락 / 추가 검사
# ==========================================

expected_ids = set(
    expected_results.keys()
)

actual_ids = set(
    actual_results.keys()
)


missing_ids = sorted(
    expected_ids - actual_ids
)

extra_ids = sorted(
    actual_ids - expected_ids
)


# ==========================================
# 6. 항목별 정확도 카운터
# ==========================================

checks = {
    "sample_id": 0,
    "Pb": 0,
    "Pb_unit": 0,
    "Cd": 0,
    "Cd_unit": 0,
    "weight_g": 0,
    "weight_unit": 0
}


matched_samples = 0

mismatches = []


# ==========================================
# 7. 100건 1:1 비교
# ==========================================

for sample_id, expected in expected_results.items():

    if sample_id not in actual_results:

        mismatches.append({
            "sample_id": sample_id,
            "error": "AI 추출 결과에서 시료 누락"
        })

        continue


    actual = actual_results[
        sample_id
    ]


    # --------------------------------------
    # Sample ID 비교
    # --------------------------------------

    id_ok = (
        actual["sample_id"]
        == expected["sample_id"]
    )


    # --------------------------------------
    # 숫자 비교
    # --------------------------------------

    pb_ok = math.isclose(
        float(actual["Pb"]),
        expected["Pb"],
        rel_tol=0.0,
        abs_tol=1e-9
    )

    cd_ok = math.isclose(
        float(actual["Cd"]),
        expected["Cd"],
        rel_tol=0.0,
        abs_tol=1e-9
    )

    weight_ok = math.isclose(
        float(actual["weight_g"]),
        expected["weight_g"],
        rel_tol=0.0,
        abs_tol=1e-9
    )


    # --------------------------------------
    # 단위 비교
    # --------------------------------------

    pb_unit_ok = (
        canonical_unit(
            actual["Pb_unit"]
        )
        == expected["Pb_unit"]
    )

    cd_unit_ok = (
        canonical_unit(
            actual["Cd_unit"]
        )
        == expected["Cd_unit"]
    )

    weight_unit_ok = (
        canonical_unit(
            actual["weight_unit"]
        )
        == expected["weight_unit"]
    )


    # --------------------------------------
    # 항목별 카운트
    # --------------------------------------

    if id_ok:
        checks["sample_id"] += 1

    if pb_ok:
        checks["Pb"] += 1

    if pb_unit_ok:
        checks["Pb_unit"] += 1

    if cd_ok:
        checks["Cd"] += 1

    if cd_unit_ok:
        checks["Cd_unit"] += 1

    if weight_ok:
        checks["weight_g"] += 1

    if weight_unit_ok:
        checks["weight_unit"] += 1


    # --------------------------------------
    # 시료 전체 일치 여부
    # --------------------------------------

    all_ok = (
        id_ok
        and pb_ok
        and pb_unit_ok
        and cd_ok
        and cd_unit_ok
        and weight_ok
        and weight_unit_ok
    )


    if all_ok:

        matched_samples += 1

    else:

        mismatches.append({
            "sample_id": sample_id,

            "Pb": {
                "expected": expected["Pb"],
                "actual": actual["Pb"]
            },

            "Pb_unit": {
                "expected": expected["Pb_unit"],
                "actual": canonical_unit(
                    actual["Pb_unit"]
                )
            },

            "Cd": {
                "expected": expected["Cd"],
                "actual": actual["Cd"]
            },

            "Cd_unit": {
                "expected": expected["Cd_unit"],
                "actual": canonical_unit(
                    actual["Cd_unit"]
                )
            },

            "weight_g": {
                "expected": expected["weight_g"],
                "actual": actual["weight_g"]
            },

            "weight_unit": {
                "expected": expected["weight_unit"],
                "actual": canonical_unit(
                    actual["weight_unit"]
                )
            }
        })


# ==========================================
# 8. 정확도 계산
# ==========================================

total_samples = len(
    expected_results
)

fields_per_sample = 7

total_data_points = (
    total_samples
    * fields_per_sample
)

matched_data_points = sum(
    checks.values()
)

data_point_accuracy = (
    matched_data_points
    / total_data_points
) * 100

sample_accuracy = (
    matched_samples
    / total_samples
) * 100


# ==========================================
# 9. 결과 출력
# ==========================================

print()
print("========================================")
print(" AI Parser 100건 검증 결과")
print("========================================")
print()

print(
    "검증 시료 수       :",
    total_samples
)

print(
    "AI 추출 시료 수    :",
    len(actual_results)
)

print(
    "검증 데이터 포인트 :",
    total_data_points
)

print()


print(
    f"Sample ID 일치      : "
    f"{checks['sample_id']}/{total_samples}"
)

print(
    f"Pb 수치 일치        : "
    f"{checks['Pb']}/{total_samples}"
)

print(
    f"Pb 단위 일치        : "
    f"{checks['Pb_unit']}/{total_samples}"
)

print(
    f"Cd 수치 일치        : "
    f"{checks['Cd']}/{total_samples}"
)

print(
    f"Cd 단위 일치        : "
    f"{checks['Cd_unit']}/{total_samples}"
)

print(
    f"Weight 수치 일치    : "
    f"{checks['weight_g']}/{total_samples}"
)

print(
    f"Weight 단위 일치    : "
    f"{checks['weight_unit']}/{total_samples}"
)

print()


print(
    "누락된 Sample ID   :",
    len(missing_ids)
)

print(
    "추가된 Sample ID   :",
    len(extra_ids)
)

print(
    "불일치 시료        :",
    len(mismatches)
)

print()


print(
    f"데이터 포인트 정확도: "
    f"{data_point_accuracy:.2f}%"
)

print(
    f"시료 단위 정확도   : "
    f"{sample_accuracy:.2f}%"
)


# ==========================================
# 10. 누락 / 추가 ID 출력
# ==========================================

if missing_ids:

    print()
    print("=== 누락 Sample ID ===")

    for sample_id in missing_ids:
        print(sample_id)


if extra_ids:

    print()
    print("=== AI가 추가한 Sample ID ===")

    for sample_id in extra_ids:
        print(sample_id)


# ==========================================
# 11. 불일치 상세 출력
# ==========================================

if mismatches:

    print()
    print("=== 불일치 상세 ===")

    for mismatch in mismatches:
        print(mismatch)

else:

    print()
    print(
        "모든 시료의 AI 추출 결과가 "
        "정답 데이터와 일치했습니다."
    )