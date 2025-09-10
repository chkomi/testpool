import json
import re

# Read the JSON file
with open('2025-gongsa.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the JavaScript object
# First, remove the export statement if present
content = re.sub(r'^.*export default ', '', content, flags=re.MULTILINE)

# Load the JSON data
quiz_data = json.loads(content)

# Modify question 9
for i, question in enumerate(quiz_data):
    if question["questionNumber"] == 9:
        quiz_data[i]["explanation"] = """문제 9 — 【정답】 c — 【해설】

- 관련 법령: 「한국농어촌공사 및 농지관리기금법」 제34조
- 정답 이유: 농지관리기금은 농지시장 안정과 농업구조 개선을 위한 용도로 사용되며, 일반인에게 농지를 매도하는 것은 적절하지 않습니다.

- 선택지 분석:
  ① a) 직업전환 농업인 농지 임차 자금 융자 → 제34조 제1항 제6호에 해당 (O)
  ② b) 경영위기 농업인 지원을 위한 농지매입 자금 융자 → 제34조 제1항 제4호에 해당 (O)
  ③ c) 은퇴 농업인 농지 매입 후 일반인에게 매도 → 농지관리기금 용도에 부합하지 않음 (X)
  ④ d) 농지 재개발사업 자금 투자 → 제34조 제1항 제10호에 해당 (O)"""

# Modify question 11
for i, question in enumerate(quiz_data):
    if question["questionNumber"] == 11:
        quiz_data[i]["explanation"] = """문제 11 — 【정답】 d — 【해설】

- 관련 법령: 「한국농어촌공사 및 농지관리기금법 시행령」 제17조
- 정답 이유: 농지관리기금에서 융자를 받아 사업을 시행한 결과 발생하는 손익 중 기금에 귀속되는 것은 임차료와 임대료의 차액 및 임대료입니다.

- 선택지 분석:
  ① ㉠ 농지연금 위험부담금 → 기금에 귀속되는 손익에 포함되지 않음 (X)
  ② ㉡ 농지의 임차료와 임대료의 차액 → 제17조에 명시된 기금 귀속 손익 (O)
  ③ ㉢ 농지연금채권에 대한 이자 → 기금에 귀속되는 손익에 포함되지 않음 (X)
  ④ ㉣ 농지의 임대료 → 제17조에 명시된 기금 귀속 손익 (O)"""

# Modify question 12
for i, question in enumerate(quiz_data):
    if question["questionNumber"] == 12:
        quiz_data[i]["explanation"] = """문제 12 — 【정답】 a — 【해설】

- 관련 법령: 「한국농어촌공사 및 농지관리기금법」 제12조
- 정답 이유: 사채의 발행액은 공사의 자본금과 적립금을 합친 금액의 2배를 초과하지 못하며, '차감한 금액'이 아닙니다.

- 선택지 분석:
  ① a) 자본금에서 적립금을 차감한 금액의 2배 초과 불가 → 제12조 제2항에 '자본금과 적립금을 합친 금액의 2배를 초과하지 못한다'로 명시 (X)
  ② b) 발행목적과 발행방법에 관하여 이사회 의결 → 제12조 제1항에 명시 (O)
  ③ c) 정부는 원리금 상환 보증하지 않음 → 제12조 제5항에 명시 (O)
  ④ d) 농림축산식품부장관의 승인 거쳐 발행 결정 → 제12조에 명시 (O)"""

# Modify question 13
for i, question in enumerate(quiz_data):
    if question["questionNumber"] == 13:
        quiz_data[i]["explanation"] = """문제 13 — 【정답】 b — 【해설】

- 관련 법령: 「한국농어촌공사 및 농지관리기금법」 제11조 제2항
- 정답 이유: 매 회계연도 결산 결과 손실이 생겼을 때의 처리 순서는 제11조 제2항에 명시되어 있습니다.

- 선택지 분석:
  ① a) 부채, 자산, 10/100, 적립금, 자본금, 자본금 → 제11조 제2항 제1호에 명시된 순서 (X)
  ② b) 이월손실금, 자본금, 20/100, 적립금, 적립금, 자본금 → 제11조 제2항 제2호에 명시된 순서 (O)
  ③ c) 이월손실금, 자본금, 20/100, 이익준비금, 자본금, 사업확장적립금 → 제11조 제2항 제2호에 명시된 순서와 다름 (X)
  ④ d) 이월손실금, 자산, 10/100, 이익준비금, 자본금, 사업확장적립금 → 제11조 제2항 제2호에 명시된 순서와 다름 (X)"""

# Convert back to JSON string
json_str = json.dumps(quiz_data, ensure_ascii=False, indent=4)

# Write back to file with export statement
with open('2025-gongsa.js', 'w', encoding='utf-8') as f:
    f.write("export default ")
    f.write(json_str)
    f.write(";")

print("Questions 9, 11, 12, and 13 have been updated.")