# AI·Python 기반 토양분석 데이터 자동화 프로토타입

## 1. 프로젝트 개요

토양분석 업무에서 발생하는 RAW DATA의 수기 입력 및 기준치 판정 과정을 자동화하기 위한 개인 프로토타입입니다.

고정된 형식의 RAW DATA는 Python 정규식 Parser로 처리하고, 서식이 변경되거나 비정형 형태로 입력되는 경우에는 로컬 LLM을 이용해 데이터를 구조화하도록 구현했습니다.

AI는 RAW DATA의 추출 및 구조화만 담당하며, 데이터 검증, 단위 정규화, 기준치 비교 및 최종 판정은 Python의 결정론적 로직으로 수행합니다.

> 본 프로젝트는 개인 학습 및 프로토타입 검증을 위해 합성(Mock) 데이터만 사용했습니다.
>
> `standards.json`에 사용된 Pb, Cd 기준값 역시 실제 법적 기준이 아닌 테스트용 모의값입니다.

---

## 2. 개발 배경

초기에는 다음과 같은 고정 형식의 RAW DATA를 정규식 기반 Parser로 자동 처리했습니다.

```text
Sample ID: SOIL-001
Pb: 82.4 mg/kg
Cd: 2.1 mg/kg
Weight: 3.000 g
```

그러나 RAW DATA의 서식이 다음처럼 변경되자 기존 정규식 Parser가 데이터를 추출하지 못했습니다.

```text
[SAMPLE RESULT]
SAMPLE_NO = FORMAT-001
Lead(Pb) : 82.40 ppm
Cadmium(Cd) : 2.10 ppm
Sample Weight = 3.000 gram
```

실험 결과:

```text
기존 정규식 Parser
→ 변경된 RAW 형식 3건 중 0건 추출
```

이를 개선하기 위해 비정형 RAW DATA를 해석하는 로컬 LLM 기반 AI Parser를 추가했습니다.

---

## 3. 시스템 구조

```text
토양분석 RAW DATA
        |
        v
+-------------------+
|   Local LLM       |
| Qwen2.5 3B        |
| RAW 구조화        |
+-------------------+
        |
        v
JSON Schema 기반 표준 데이터
        |
        v
+-------------------+
| Python Validation |
| - 필수 필드 검사  |
| - 숫자형 검사     |
| - 단위 검사       |
+-------------------+
        |
        v
단위 정규화
        |
        v
Python 기준치 비교
        |
        v
최종 판정
        |
        v
Excel 자동 저장
```

---

## 4. 기술 스택

- Python
- Ollama
- Qwen2.5 3B
- JSON Schema
- Regular Expression
- openpyxl
- CSV 기반 정답 데이터
- Hold-out Validation

---

## 5. AI와 Python의 역할 분리

### Local LLM

AI는 다음 기능만 담당합니다.

- 다양한 RAW DATA 서식 해석
- Sample ID 추출
- Pb / Cd 수치 추출
- Weight 추출
- 원본 단위 추출
- JSON Schema 기반 구조화

AI는 기준치 판정이나 법적 판단을 수행하지 않습니다.

### Python

Python은 다음 기능을 담당합니다.

- 필수 필드 검증
- 데이터형 검증
- 단위 존재 여부 확인
- 허용 단위 확인
- 단위 표준화
- 기준값 비교
- 최종 판정
- Excel 저장
- 정답 데이터와 정확도 검증

이를 통해 AI의 비결정성을 데이터 추출 영역으로 제한하고, 판정 로직의 재현성을 확보하도록 설계했습니다.

---

## 6. 데이터 안전장치

AI가 반환한 값을 그대로 판정에 사용하지 않습니다.

예를 들어 RAW DATA에 단위가 존재하지 않는 경우:

```text
Element Pb = 120.50
Element Cd = 1.80
```

AI가 숫자를 추출하더라도 Python 검증 단계에서 자동 판정을 중단하도록 구현했습니다.

```text
ValueError:
Pb 단위가 없어 자동 판정을 중단합니다.
```

또한 다음 단위 표현을 내부 표준 단위로 정규화합니다.

```text
g
gram
grams
```

→

```text
g
```

---

## 7. 정규식 Parser 검증

고정 형식 합성 데이터 100건을 대상으로 다음 6개 항목을 1:1 교차검증했습니다.

- Sample ID
- Pb
- Cd
- Weight
- 초과 항목
- 최종 판정

검증 결과:

```text
시료 수            : 100
데이터 포인트      : 600

Sample ID          : 100/100
Pb                 : 100/100
Cd                 : 100/100
Weight             : 100/100
초과 항목          : 100/100
최종 판정          : 100/100

시료 정확도        : 100.00%
```

고의로 Pb 값을 변경한 오류 주입 테스트에서는 정확도가 99%로 감소하며 해당 시료를 정상적으로 검출했습니다.

---

## 8. AI Parser 기본 검증

정의된 4종 RAW 형식으로 구성한 합성 데이터 100건을 이용해 AI Parser의 다음 7개 항목을 검증했습니다.

- Sample ID
- Pb
- Pb 단위
- Cd
- Cd 단위
- Weight
- Weight 단위

총 검증 데이터 포인트:

```text
100개 시료 × 7개 항목
= 700개
```

Batch 처리 중 일부 단위 추출 오류가 발생했으며, 해당 Batch를 개별 시료 단위로 재처리하는 Fallback 로직을 적용했습니다.

최종 결과:

```text
시료 수             : 100
데이터 포인트       : 700

누락 ID             : 0
추가 ID             : 0
불일치 시료         : 0

데이터포인트 정확도 : 100.00%
시료 단위 정확도    : 100.00%
```

---

## 9. 미정의 형식 Baseline 테스트

AI Parser의 일반화 성능을 확인하기 위해 기존 Prompt에서 직접 사용하지 않은 새로운 RAW 형식 5종을 생성했습니다.

총 100개의 합성 시료를 이용해 최초 Hold-out 테스트를 수행했습니다.

### Batch Size 10

```text
데이터포인트 정확도 : 93.14%
시료 단위 정확도    : 86.00%
```

발견된 주요 오류:

- 일부 Sample ID 누락
- Weight 소수점 정밀도 손실
- 서로 다른 시료의 값 교차 매핑

### Batch Size 1

```text
데이터포인트 정확도 : 80.00%
시료 단위 정확도    : 80.00%
```

형식별 시료 정확도:

```text
형식 1 : 80%
형식 2 : 25%
형식 3 : 100%
형식 4 : 95%
형식 5 : 100%
```

오류 분석 결과 특정 필드명, 단위 위치 및 Sample ID 표현에 대한 일반화 문제가 확인되었습니다.

---

## 10. Prompt v2 개선

Baseline 오류를 분석하여 단순 필드명 매칭 방식에서 의미 기반 추출 규칙으로 Prompt를 개선했습니다.

개선 내용:

- Sample / Specimen / Code / Record 등 식별자 의미 기반 인식
- Pb / Lead 의미 기반 인식
- Cd / Cadmium 의미 기반 인식
- Weight / Mass 의미 기반 인식
- 필드명 내부 단위 인식
- 대괄호 단위 인식
- 별도 unit 필드 인식
- Sample ID 원문 대소문자 보존
- 숫자 반올림 및 자릿수 축소 금지
- 시료 간 값 교차 매핑 금지

개발 데이터 재검증 결과:

```text
시료 수             : 100
데이터 포인트       : 700

데이터포인트 정확도 : 100.00%
시료 단위 정확도    : 100.00%
```

---

## 11. Final Hold-out 검증

Prompt v2 개선 완료 후 AI Parser를 수정하지 않는 동결 상태로 설정했습니다.

이후 기존 개발 데이터와 다른 표현 및 숫자로 구성된 새로운 합성 RAW 형식 5종, 총 100건을 새롭게 생성했습니다.

각 시료는 독립적으로 AI Parser에 입력했습니다.

### Final 결과

```text
검증 시료 수        : 100
검증 데이터 포인트  : 700

Sample ID           : 100/100
Pb 수치             : 100/100
Pb 단위             : 100/100
Cd 수치             : 100/100
Cd 단위             : 100/100
Weight 수치         : 100/100
Weight 단위         : 100/100

AI 호출 실패        : 0
누락 Sample ID      : 0
추가 Sample ID      : 0
중복 Sample ID      : 0
불일치 시료         : 0

데이터포인트 정확도 : 100.00%
시료 단위 정확도    : 100.00%
```

형식별 결과:

```text
형식 1 : 20/20 (100%)
형식 2 : 20/20 (100%)
형식 3 : 20/20 (100%)
형식 4 : 20/20 (100%)
형식 5 : 20/20 (100%)
```

---

## 12. 정확도 해석 시 주의사항

본 프로젝트에서 확인된 100% 정확도는 실제 기관 전체 데이터 또는 모든 가능한 RAW DATA에 대한 성능을 의미하지 않습니다.

정확한 표현은 다음과 같습니다.

> Prompt 동결 상태에서 새롭게 생성한 합성 Final Hold-out 100건, 700개 데이터 포인트의 검증 범위에서 정답 데이터와 100% 일치했습니다.

실제 운영 환경 적용을 위해서는 실제 장비별 RAW DATA, 더 다양한 예외 형식, 대규모 데이터 및 반복 실행에 대한 추가 검증이 필요합니다.

---

## 13. 프로젝트 구조

```text
soil_analysis_automation/
|
|-- input/
|   |-- sample_raw.txt
|   |-- test_100_raw.txt
|   |-- expected_100.csv
|   |-- format_changed_raw.txt
|   |-- ai_test_100_raw.txt
|   |-- ai_expected_100.csv
|   |-- holdout_100_raw.txt
|   |-- holdout_expected_100.csv
|   |-- final_holdout_100_raw.txt
|   `-- final_holdout_expected_100.csv
|
|-- output/
|   |-- soil_analysis_result.xlsx
|   `-- ai_soil_analysis_result.xlsx
|
|-- parser.py
|-- ai_parser.py
|-- ai_parser_v2.py
|-- classifier.py
|-- unit_normalizer.py
|-- excel_writer.py
|
|-- main.py
|-- ai_pipeline.py
|
|-- generate_test_data.py
|-- generate_ai_test_data.py
|-- generate_holdout_data.py
|-- generate_final_holdout.py
|
|-- validator.py
|-- ai_validator.py
|-- holdout_validator.py
|-- holdout_validator_single.py
|-- holdout_validator_single_v2.py
|-- final_validator.py
|
|-- test_parser.py
|-- test_ai_parser.py
|
|-- standards.json
`-- README.md
```

---

## 14. 실행 예시

### 기본 Python 파이프라인

```powershell
python main.py
```

### AI 기반 파이프라인

Ollama 및 Qwen2.5 3B가 실행 가능한 환경에서:

```powershell
python ai_pipeline.py
```

### Final Hold-out 검증

```powershell
python final_validator.py
```

---

## 15. 향후 개선 방향

- 실제 장비별 RAW DATA 형식 추가 검증
- 지원 중금속 항목 확장
- 기준값 및 단위 설정 외부 파일화
- Schema 검증 강화
- 로그 및 Audit Trail 기록
- 입력 파일 Hash 기록
- 기준값 버전 관리
- COC(Chain of Custody) 정보 연계
- 반복 Hold-out 검증
- 대규모 시료 성능 평가
- 실제 운영 환경을 고려한 보안 정책 검토
