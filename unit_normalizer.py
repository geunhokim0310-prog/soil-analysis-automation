def normalize_units(sample):
    """
    모의 프로토타입용 단위 정규화.

    농도:
    - mg/kg -> mg/kg
    - ppm -> mg/kg
      ※ 질량 기준 농도라는 테스트 전제에서 1 ppm = 1 mg/kg

    무게:
    - g / gram / grams -> g
    """

    normalized = sample.copy()

    # ======================================
    # Pb 단위 정규화
    # ======================================

    if sample["Pb_unit"] == "mg/kg":
        normalized["Pb"] = sample["Pb"]

    elif sample["Pb_unit"] == "ppm":
        normalized["Pb"] = sample["Pb"]

    else:
        raise ValueError(
            f"{sample['sample_id']}: "
            f"Pb 단위 변환 불가: {sample['Pb_unit']}"
        )

    # ======================================
    # Cd 단위 정규화
    # ======================================

    if sample["Cd_unit"] == "mg/kg":
        normalized["Cd"] = sample["Cd"]

    elif sample["Cd_unit"] == "ppm":
        normalized["Cd"] = sample["Cd"]

    else:
        raise ValueError(
            f"{sample['sample_id']}: "
            f"Cd 단위 변환 불가: {sample['Cd_unit']}"
        )

    # ======================================
    # Weight 단위 정규화
    # ======================================

    if sample["weight_unit"] in {
        "g",
        "gram",
        "grams"
    }:
        normalized["weight_g"] = sample["weight_g"]

    else:
        raise ValueError(
            f"{sample['sample_id']}: "
            f"Weight 단위 변환 불가: "
            f"{sample['weight_unit']}"
        )

    # 내부 표준 단위 기록
    normalized["Pb_unit"] = "mg/kg"
    normalized["Cd_unit"] = "mg/kg"
    normalized["weight_unit"] = "g"

    return normalized