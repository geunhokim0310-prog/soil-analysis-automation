from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


def save_to_excel(results, output_path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "토양분석결과"

    # 엑셀 첫 번째 행
    headers = [
        "시료 ID",
        "Pb (mg/kg)",
        "Cd (mg/kg)",
        "칭량 (g)",
        "초과 항목",
        "최종 판정"
    ]

    sheet.append(headers)

    # 분석 결과 입력
    for result in results:
        exceeded = ", ".join(result["exceeded_items"])

        if not exceeded:
            exceeded = "-"

        sheet.append([
            result["sample_id"],
            result["Pb"],
            result["Cd"],
            result["weight_g"],
            exceeded,
            result["result"]
        ])

    # 제목 행 굵게 표시
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # 열 너비 조절
    sheet.column_dimensions["A"].width = 15
    sheet.column_dimensions["B"].width = 15
    sheet.column_dimensions["C"].width = 15
    sheet.column_dimensions["D"].width = 15
    sheet.column_dimensions["E"].width = 18
    sheet.column_dimensions["F"].width = 20

    # 엑셀 파일 저장
    workbook.save(output_path)