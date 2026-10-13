from parser import parse_raw_data


with open(
    "input/format_changed_raw.txt",
    "r",
    encoding="utf-8"
) as file:
    raw_text = file.read()


results = parse_raw_data(raw_text)


print("=== 기존 Parser 테스트 ===")
print("추출된 시료 수:", len(results))
print()

for result in results:
    print(result)