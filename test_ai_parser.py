from ai_parser import parse_with_ai


with open(
    "input/format_changed_raw.txt",
    "r",
    encoding="utf-8"
) as file:
    raw_text = file.read()


print("=== 로컬 AI Parser 테스트 ===")
print()

results = parse_with_ai(raw_text)


print("추출된 시료 수:", len(results))
print()


for result in results:
    print(result)