import json

from ai_parser import parse_with_ai
from unit_normalizer import normalize_units
from classifier import classify_sample
from excel_writer import save_to_excel


# ==========================================
# 1. 비정형 RAW DATA 읽기
# ==========================================

with open(
    "input/format_changed_raw.txt",
    "r",
    encoding="utf-8"
) as file:
    raw_text = file.read()


print()
print("====================================")
print(" AI 토양분석 자동화 파이프라인")
print("====================================")
print()


# ==========================================
# 2. 로컬 AI 데이터 추출
# ==========================================

print("[1] 로컬 AI RAW DATA 추출")

samples = parse_with_ai(raw_text)

print(
    f"    추출 완료: {len(samples)}건"
)


# ==========================================
# 3. 단위 정규화
# ==========================================

print("[2] Python 단위 검증 및 정규화")

normalized_samples = []

for sample in samples:

    normalized = normalize_units(sample)

    normalized_samples.append(
        normalized
    )

print(
    f"    정규화 완료: "
    f"{len(normalized_samples)}건"
)


# ==========================================
# 4. 테스트 기준값 읽기
# ==========================================

print("[3] 테스트 기준값 불러오기")

with open(
    "standards.json",
    "r",
    encoding="utf-8"
) as file:
    standards = json.load(file)


# ==========================================
# 5. Python 기준 판정
# ==========================================

print("[4] Python 자동 판정")

results = []

for sample in normalized_samples:

    result = classify_sample(
        sample,
        standards
    )

    results.append(
        result
    )


# ==========================================
# 6. 결과 출력
# ==========================================

print()

for result in results:

    print(
        result["sample_id"],
        "| Pb:",
        result["Pb"],
        "mg/kg",
        "| Cd:",
        result["Cd"],
        "mg/kg",
        "| 초과:",
        result["exceeded_items"],
        "| 판정:",
        result["result"]
    )


# ==========================================
# 7. Excel 저장
# ==========================================

output_path = (
    "output/"
    "ai_soil_analysis_result.xlsx"
)

save_to_excel(
    results,
    output_path
)


print()
print("[5] Excel 저장 완료")
print("    저장 위치:", output_path)

print()
print("====================================")
print(" 파이프라인 정상 완료")
print("====================================")