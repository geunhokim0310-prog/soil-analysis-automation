import csv
import json

from parser import parse_raw_data
from classifier import classify_sample


# ==========================================
# 1. 100건 RAW DATA 읽기
# ==========================================

with open(
    "input/test_100_raw.txt",
    "r",
    encoding="utf-8"
) as file:
    raw_text = file.read()


# ==========================================
# 2. RAW DATA 자동 추출
# ==========================================

samples = parse_raw_data(raw_text)


# ==========================================
# 3. 기준값 읽기
# ==========================================

with open(
    "standards.json",
    "r",
    encoding="utf-8"
) as file:
    standards = json.load(file)


# ==========================================
# 4. Python 자동 판정
# ==========================================

actual_results = []

for sample in samples:
    result = classify_sample(sample, standards)
    actual_results.append(result)


# ==========================================
# 5. 정답 데이터 읽기
# ==========================================

expected_results = {}

with open(
    "input/expected_100.csv",
    "r",
    encoding="utf-8-sig"
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        expected_results[row["sample_id"]] = row


# ==========================================
# 6. 항목별 검증 카운터
# ==========================================

checks = {
    "sample_id": 0,
    "Pb": 0,
    "Cd": 0,
    "weight_g": 0,
    "exceeded_items": 0,
    "result": 0
}

matched_samples = 0
mismatches = []


# ==========================================
# 7. 100건 1:1 정밀 비교
# ==========================================

for actual in actual_results:

    sample_id = actual["sample_id"]

    # 정답 데이터에 Sample ID가 존재하는지 확인
    if sample_id not in expected_results:
        mismatches.append({
            "sample_id": sample_id,
            "error": "정답 데이터에 Sample ID 없음"
        })
        continue

    expected = expected_results[sample_id]

    # 실제값
    actual_pb = float(actual["Pb"])
    actual_cd = float(actual["Cd"])
    actual_weight = float(actual["weight_g"])

    actual_exceeded = ", ".join(
        actual["exceeded_items"]
    )

    actual_result = actual["result"]

    # 정답값
    expected_pb = float(expected["Pb"])
    expected_cd = float(expected["Cd"])
    expected_weight = float(expected["weight_g"])

    expected_exceeded = expected["expected_exceeded"]
    expected_result = expected["expected_result"]


    # --------------------------------------
    # 항목별 비교
    # --------------------------------------

    id_ok = sample_id == expected["sample_id"]
    pb_ok = actual_pb == expected_pb
    cd_ok = actual_cd == expected_cd
    weight_ok = actual_weight == expected_weight

    exceeded_ok = (
        actual_exceeded == expected_exceeded
    )

    result_ok = (
        actual_result == expected_result
    )


    # --------------------------------------
    # 항목별 일치 건수 기록
    # --------------------------------------

    if id_ok:
        checks["sample_id"] += 1

    if pb_ok:
        checks["Pb"] += 1

    if cd_ok:
        checks["Cd"] += 1

    if weight_ok:
        checks["weight_g"] += 1

    if exceeded_ok:
        checks["exceeded_items"] += 1

    if result_ok:
        checks["result"] += 1


    # --------------------------------------
    # 시료 전체가 일치하는지 확인
    # --------------------------------------

    all_ok = (
        id_ok
        and pb_ok
        and cd_ok
        and weight_ok
        and exceeded_ok
        and result_ok
    )

    if all_ok:
        matched_samples += 1

    else:
        mismatches.append({
            "sample_id": sample_id,

            "Pb": {
                "expected": expected_pb,
                "actual": actual_pb
            },

            "Cd": {
                "expected": expected_cd,
                "actual": actual_cd
            },

            "Weight": {
                "expected": expected_weight,
                "actual": actual_weight
            },

            "Exceeded": {
                "expected": expected_exceeded,
                "actual": actual_exceeded
            },

            "Result": {
                "expected": expected_result,
                "actual": actual_result
            }
        })


# ==========================================
# 8. 최종 정확도 계산
# ==========================================

total = len(expected_results)

accuracy = (
    matched_samples / total
) * 100

total_data_points = total * 6


# ==========================================
# 9. 검증 결과 출력
# ==========================================

print()
print("====================================")
print("  100건 정밀 교차 검증 결과")
print("====================================")
print()

print("검증 시료 수       :", total)
print("검증 데이터 포인트 :", total_data_points)

print()

print(
    f"Sample ID 일치     : "
    f"{checks['sample_id']}/{total}"
)

print(
    f"Pb 수치 일치       : "
    f"{checks['Pb']}/{total}"
)

print(
    f"Cd 수치 일치       : "
    f"{checks['Cd']}/{total}"
)

print(
    f"Weight 수치 일치   : "
    f"{checks['weight_g']}/{total}"
)

print(
    f"초과항목 일치      : "
    f"{checks['exceeded_items']}/{total}"
)

print(
    f"최종판정 일치      : "
    f"{checks['result']}/{total}"
)

print()

print(
    f"전체 일치 시료     : "
    f"{matched_samples}/{total}"
)

print(
    "불일치 시료        :",
    len(mismatches)
)

print(
    f"시료 단위 정확도   : "
    f"{accuracy:.2f}%"
)


# ==========================================
# 10. 불일치 상세 출력
# ==========================================

if mismatches:

    print()
    print("=== 불일치 상세 ===")

    for mismatch in mismatches:
        print(mismatch)

else:

    print()
    print(
        "모든 시료의 추출 수치 및 "
        "판정 결과가 일치했습니다."
    )