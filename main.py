import json

from parser import parse_raw_data
from classifier import classify_sample
from excel_writer import save_to_excel

# 1. RAW DATA 파일 읽기
with open("input/sample_raw.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()


# 2. RAW DATA에서 시료 정보 추출
samples = parse_raw_data(raw_text)


# 3. 기준값 파일 읽기
with open("standards.json", "r", encoding="utf-8") as file:
    standards = json.load(file)


# 4. 각 시료 자동 판정
results = []

for sample in samples:
    result = classify_sample(sample, standards)
    results.append(result)


# 5. 결과 출력
print("=== 토양 분석 자동 판정 결과 ===")

for result in results:
    print(
        result["sample_id"],
        "| Pb:", result["Pb"],
        "| Cd:", result["Cd"],
        "| 초과 항목:", result["exceeded_items"],
        "| 판정:", result["result"]
    )
    # 6. Excel 파일 자동 저장
output_path = "output/soil_analysis_result.xlsx"

save_to_excel(results, output_path)

print()
print("Excel 파일 생성 완료!")
print("저장 위치:", output_path)