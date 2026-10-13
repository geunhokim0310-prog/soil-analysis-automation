import random
import csv


random.seed(42)

PB_STANDARD = 200.0
CD_STANDARD = 4.0

raw_lines = []
answer_rows = []


for i in range(1, 101):
    sample_id = f"TEST-{i:03d}"

    pb = round(random.uniform(20, 350), 2)
    cd = round(random.uniform(0.5, 8.0), 2)
    weight = round(random.uniform(2.990, 3.010), 3)

    # 모의 RAW DATA 생성
    raw_lines.append(
        f"Sample ID: {sample_id}\n"
        f"Pb: {pb} mg/kg\n"
        f"Cd: {cd} mg/kg\n"
        f"Weight: {weight} g\n"
    )

    # 독립적인 정답 생성
    exceeded = []

    if pb > PB_STANDARD:
        exceeded.append("Pb")

    if cd > CD_STANDARD:
        exceeded.append("Cd")

    if exceeded:
        expected_result = "정밀조사 대상"
    else:
        expected_result = "기준 이내"

    answer_rows.append([
        sample_id,
        pb,
        cd,
        weight,
        ", ".join(exceeded),
        expected_result
    ])


# RAW DATA 저장
with open(
    "input/test_100_raw.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("\n".join(raw_lines))


# 정답 데이터 저장
with open(
    "input/expected_100.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "sample_id",
        "Pb",
        "Cd",
        "weight_g",
        "expected_exceeded",
        "expected_result"
    ])

    writer.writerows(answer_rows)


print("100건 모의 데이터 생성 완료!")
print("RAW DATA: input/test_100_raw.txt")
print("정답 데이터: input/expected_100.csv")