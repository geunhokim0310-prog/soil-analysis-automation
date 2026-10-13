import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


# ==========================================
# 1. AI 출력 JSON Schema
# ==========================================

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "samples": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sample_id": {
                        "type": "string"
                    },
                    "Pb": {
                        "type": "number"
                    },
                    "Pb_unit": {
                        "type": ["string", "null"]
                    },
                    "Cd": {
                        "type": "number"
                    },
                    "Cd_unit": {
                        "type": ["string", "null"]
                    },
                    "weight_g": {
                        "type": "number"
                    },
                    "weight_unit": {
                        "type": ["string", "null"]
                    }
                },
                "required": [
                    "sample_id",
                    "Pb",
                    "Pb_unit",
                    "Cd",
                    "Cd_unit",
                    "weight_g",
                    "weight_unit"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": [
        "samples"
    ],
    "additionalProperties": False
}


# ==========================================
# 2. AI 추출 결과 Python 검증
# ==========================================

def validate_samples(samples):

    validated = []

    for index, sample in enumerate(samples, start=1):

        # ------------------------------
        # Sample ID 검사
        # ------------------------------

        if not isinstance(sample["sample_id"], str):
            raise ValueError(
                f"{index}번째 sample_id가 문자열이 아닙니다."
            )

        # ------------------------------
        # 숫자형 검사
        # ------------------------------

        for field in [
            "Pb",
            "Cd",
            "weight_g"
        ]:

            value = sample[field]

            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
            ):
                raise ValueError(
                    f"{index}번째 {field}가 숫자가 아닙니다."
                )

        # ------------------------------
        # 단위 존재 여부 검사
        # ------------------------------

        if sample["Pb_unit"] is None:
            raise ValueError(
                f"{sample['sample_id']}: "
                "Pb 단위가 없어 자동 판정을 중단합니다."
            )

        if sample["Cd_unit"] is None:
            raise ValueError(
                f"{sample['sample_id']}: "
                "Cd 단위가 없어 자동 판정을 중단합니다."
            )

        if sample["weight_unit"] is None:
            raise ValueError(
                f"{sample['sample_id']}: "
                "Weight 단위가 없어 자동 판정을 중단합니다."
            )

        # ------------------------------
        # 단위 표준화
        # ------------------------------

        pb_unit = (
            sample["Pb_unit"]
            .lower()
            .strip()
        )

        cd_unit = (
            sample["Cd_unit"]
            .lower()
            .strip()
        )

        weight_unit = (
            sample["weight_unit"]
            .lower()
            .strip()
        )

        # ------------------------------
        # 허용 단위
        # ------------------------------

        allowed_concentration_units = {
            "mg/kg",
            "ppm"
        }

        allowed_weight_units = {
            "g",
            "gram",
            "grams"
        }

        # ------------------------------
        # 허용 단위 검사
        # ------------------------------

        if pb_unit not in allowed_concentration_units:
            raise ValueError(
                f"{sample['sample_id']}: "
                f"허용되지 않은 Pb 단위: {pb_unit}"
            )

        if cd_unit not in allowed_concentration_units:
            raise ValueError(
                f"{sample['sample_id']}: "
                f"허용되지 않은 Cd 단위: {cd_unit}"
            )

        if weight_unit not in allowed_weight_units:
            raise ValueError(
                f"{sample['sample_id']}: "
                f"허용되지 않은 Weight 단위: {weight_unit}"
            )

        # ------------------------------
        # 검증 통과 데이터
        # ------------------------------

        validated.append({
            "sample_id": sample["sample_id"].strip(),
            "Pb": float(sample["Pb"]),
            "Cd": float(sample["Cd"]),
            "weight_g": float(sample["weight_g"]),
            "Pb_unit": pb_unit,
            "Cd_unit": cd_unit,
            "weight_unit": weight_unit
        })

    return validated


# ==========================================
# 3. Ollama 로컬 AI Parser
# ==========================================

def parse_with_ai(raw_text):

    prompt = f"""
당신은 토양분석 RAW DATA에서 정보를 추출하는
데이터 추출 엔진입니다.

아래 RAW DATA에 존재하는 모든 시료를 추출하세요.

필드 대응 규칙:

sample_id:
- Sample ID
- SAMPLE_NO
- ID
- Sample

Pb:
- Pb
- Lead(Pb)
- Pb concentration
- Element Pb

Cd:
- Cd
- Cadmium(Cd)
- Cd concentration
- Element Cd

weight_g:
- Weight
- Sample Weight
- Weight(g)
- Weighed Mass


단위 추출 규칙:

Pb_unit:
- Pb 값 뒤에 표시된 단위를 추출하세요.
- 단위가 필드명에 명확히 표시되어 있으면 그것도 사용할 수 있습니다.
- Pb 또는 Lead라는 글자는 분석항목 이름이며 단위가 아닙니다.
- 실제 단위 표시가 없으면 null로 출력하세요.

Cd_unit:
- Cd 값 뒤에 표시된 단위를 추출하세요.
- 단위가 필드명에 명확히 표시되어 있으면 그것도 사용할 수 있습니다.
- Cd 또는 Cadmium이라는 글자는 분석항목 이름이며 단위가 아닙니다.
- 실제 단위 표시가 없으면 null로 출력하세요.

weight_unit:
- Weight 값 뒤에 표시된 단위를 추출하세요.
- Weight(g)처럼 필드명 괄호 안에 단위가 있으면 그 단위를 추출하세요.
- Sample Weight = 3.000 gram이면 gram을 추출하세요.
- 단위가 어디에도 표시되지 않으면 null로 출력하세요.


중요 규칙:

1. RAW DATA에 명시된 숫자만 추출하세요.
2. 존재하지 않는 숫자를 추측하지 마세요.
3. 오염 기준 판정은 하지 마세요.
4. 설명문을 작성하지 마세요.
5. 모든 시료를 빠짐없이 추출하세요.
6. 단위가 보이지 않으면 절대로 추측하지 말고 null로 출력하세요.


RAW DATA:

{raw_text}
"""

    # ======================================
    # Ollama 요청 내용
    # ======================================

    request_body = {
        "model": MODEL_NAME,

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "stream": False,

        "format": OUTPUT_SCHEMA,

        "options": {
            "temperature": 0
        }
    }

    encoded_body = json.dumps(
        request_body
    ).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=encoded_body,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    # ======================================
    # Ollama 호출
    # ======================================

    try:

        with urllib.request.urlopen(
            request,
            timeout=300
        ) as response:

            response_data = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.URLError as error:

        raise ConnectionError(
            "Ollama 서버에 연결할 수 없습니다. "
            "Ollama가 실행 중인지 확인하세요."
        ) from error

    # ======================================
    # AI JSON 응답 읽기
    # ======================================

    ai_content = response_data[
        "message"
    ]["content"]

    parsed = json.loads(
        ai_content
    )

    samples = parsed[
        "samples"
    ]

    # ======================================
    # AI 결과를 Python으로 재검증
    # ======================================

    return validate_samples(
        samples
    )