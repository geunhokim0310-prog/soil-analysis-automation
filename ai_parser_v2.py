import json
import urllib.request
import urllib.error

from ai_parser import (
    OLLAMA_URL,
    MODEL_NAME,
    OUTPUT_SCHEMA,
    validate_samples
)


def parse_with_ai(raw_text):

    prompt = f"""
당신은 다양한 분석기와 보고서에서 생성된
토양분석 RAW DATA를 표준 구조로 변환하는
데이터 추출 엔진입니다.

RAW DATA 안의 각 시료 레코드를 서로 독립적으로 읽고,
존재하는 모든 시료를 빠짐없이 추출하세요.


==========================================
1. sample_id 추출 원칙
==========================================

sample_id는 시료를 고유하게 구분하는 식별자입니다.

식별자 앞의 라벨은 다양한 표현일 수 있습니다.

예:
- Sample ID
- SAMPLE_NO
- ID
- Sample
- Specimen
- Code
- Lab Code
- Record
- Report No.
- Report Number

중요:

- 라벨 자체는 sample_id에 포함하지 마세요.
- 구분 기호도 포함하지 마세요.
- 예를 들어

  Record#HOLD-014

  이라면 sample_id는

  HOLD-014

  입니다.

- REPORT NO. HOLD-001 이라면
  sample_id는 HOLD-001 입니다.

- 원문 식별자의 대소문자를 임의로 변경하지 마세요.
- HOLD-001을 Hold-001로 바꾸면 안 됩니다.


==========================================
2. Pb 추출 원칙
==========================================

Pb는 납(Lead) 분석값입니다.

필드명은 다양한 표현일 수 있습니다.

예:
- Pb
- Lead
- Lead(Pb)
- Element Pb
- Metal Pb
- Pb concentration
- Pb result
- Lead result
- Lead assay

Pb 또는 Lead의 의미를 가진 필드에서
해당 시료의 숫자만 추출하세요.


==========================================
3. Cd 추출 원칙
==========================================

Cd는 카드뮴(Cadmium) 분석값입니다.

필드명은 다양한 표현일 수 있습니다.

예:
- Cd
- Cadmium
- Cadmium(Cd)
- Element Cd
- Metal Cd
- Cd concentration
- Cd result
- Cadmium result
- Cadmium assay

Cd 또는 Cadmium의 의미를 가진 필드에서
해당 시료의 숫자만 추출하세요.


==========================================
4. Weight 추출 원칙
==========================================

weight_g는 시료 질량 값입니다.

필드명은 다양한 표현일 수 있습니다.

예:
- Weight
- Sample Weight
- Weighed Mass
- Mass
- Mass used
- Initial mass
- Test mass

숫자를 절대로 반올림하거나 자릿수를 줄이지 마세요.

예:

3.005 -> 3.005

3.002 -> 3.002

2.991 -> 2.991

3.010 -> 3.010의 수치값


==========================================
5. 단위 추출 원칙
==========================================

단위는 숫자 바로 뒤에만 있는 것이 아닙니다.

다음 위치를 모두 확인하세요.

예:

Pb = 82.4 mg/kg

Pb [mg/kg] 82.4

Metal Pb [mg/kg] 82.4

Pb-value=82.4; unit=mg/kg

Lead 82.4 ppm


이 경우 모두 Pb 단위를 정확히 추출하세요.


Weight도 동일합니다.

예:

Weight = 3.001 g

Weight(g) = 3.001

Initial mass [g] 3.001

Mass-value=3.001; unit=g

Mass 3.001 grams


단위가 실제 RAW DATA 어디에도 없다면
절대로 추측하지 말고 null로 출력하세요.


==========================================
6. 레코드 독립성 원칙
==========================================

각 시료는 독립된 레코드입니다.

절대로 다른 시료의 값을 가져오거나 섞지 마세요.

한 시료의:

- sample_id
- Pb
- Pb_unit
- Cd
- Cd_unit
- weight_g
- weight_unit

은 반드시 모두 같은 레코드에서 가져와야 합니다.


==========================================
7. 숫자 보존 원칙
==========================================

RAW DATA에 적힌 숫자를 그대로 추출하세요.

- 반올림 금지
- 자릿수 축소 금지
- 다른 숫자로 변경 금지
- 계산 금지
- 추측 금지


==========================================
8. 역할 제한
==========================================

당신은 데이터 추출만 수행합니다.

오염 기준 판정을 하지 마세요.
법적 판단을 하지 마세요.
설명문을 작성하지 마세요.

JSON Schema에 맞는 데이터만 반환하세요.


==========================================
RAW DATA
==========================================

{raw_text}
"""

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

    ai_content = response_data[
        "message"
    ]["content"]

    parsed = json.loads(
        ai_content
    )

    samples = parsed[
        "samples"
    ]

    return validate_samples(
        samples
    )