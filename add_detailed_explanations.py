import json
import re

def create_detailed_explanations():
    """2025년 과목들의 상세한 해설을 생성합니다."""
    
    # 해설 데이터 구조
    detailed_explanations = {
        "농어촌정비법": {
            1: {
                "explanation": "농어촌정비법 제58조(생활환경정비사업 기본계획의 수립)",
                "detailed_explanation": "시장·군수·구청장은 생활환경정비계획에 포함된 사항을 추진하기 위하여 필요한 경우 세부 사업별로 생활환경정비사업 기본계획을 수립할 수 있습니다. 이 계획을 수립하거나 변경할 때는 해당 사업지역 주민의 의견을 듣고 시·도지사 및 관계 기관과 협의해야 하며, 이를 고시해야 합니다. 단, 대통령령으로 정하는 경미한 사항을 변경하는 경우에는 주민의견 청취와 협의가 면제됩니다.",
                "url": "https://www.law.go.kr/법령/농어촌정비법/(20250621,20581,20241220)/제58조"
            },
            2: {
                "explanation": "농어촌정비법 제23조(농업생산기반시설의 사용허가)",
                "detailed_explanation": "농업생산기반시설을 본래의 목적 범위를 벗어나거나 사용에 방해가 되는 범위로 사용하려는 자는 시장·군수·구청장의 사용허가를 받아야 합니다. 사용허가를 받은 자에게는 시설을 유지하거나 보수하는 데에 필요한 경비의 전부를 사용료로 징수할 수 있으며, 사용료를 납부하지 않으면 지방세 체납 처분의 예에 따라 징수할 수 있습니다.",
                "url": "https://www.law.go.kr/법령/농어촌정비법/(20250621,20581,20241220)/제23조"
            },
            3: {
                "explanation": "농어촌정비법 제21조(농어촌용수 오염 방지와 수질 개선 등)",
                "detailed_explanation": "오염물질이 흘러들어 농어촌용수가 오염되어 영농과 농어촌 생활환경에 지장을 줄 우려가 있다고 인정될 때, 농림축산식품부장관은 물환경보전법, 하수도법, 가축분뇨의 관리 및 이용에 관한 법률, 지하수법에 따른 명령과 조치 등을 하도록 관계 중앙행정기관의 장에게 요구할 수 있습니다. 이는 농어촌용수의 수질을 보호하고 농업생산과 농어촌 생활환경을 보전하기 위한 조치입니다.",
                "url": "https://www.law.go.kr/법령/농어촌정비법/(20250621,20581,20241220)/제21조"
            }
        },
        "공운법": {
            1: {
                "explanation": "시행령 제6조(총수입액 등의 산정방법 등)",
                "detailed_explanation": "공공기관의 총수입액은 해당 기관이 영위하는 모든 사업에서 발생하는 수입의 합계를 의미합니다. 이는 공공기관의 규모와 성격을 판단하는 중요한 지표로 사용되며, 공기업과 준정부기관을 구분하는 기준이 됩니다. 총수입액의 산정에는 정부로부터 받는 보조금, 융자금 등도 포함됩니다.",
                "url": "https://www.law.go.kr/법령/공공기관의 운영에 관한 법률 시행령/(20230101,33078,20221220)/제6조"
            },
            2: {
                "explanation": "법 제4조(공공기관) / 시행령 제4조(사실상 지배력 확보의 기준)",
                "detailed_explanation": "공공기관은 정부가 자본금의 50% 이상을 출자하거나 정부가 임원의 과반수를 임면할 수 있는 권한을 가진 기관입니다. 또한 정부가 사실상 지배력을 확보하고 있는 기관도 포함됩니다. 사실상 지배력은 정부의 출자비율, 임원 임면권, 정관 변경권, 예산 승인권 등을 종합적으로 고려하여 판단합니다.",
                "url1": "https://www.law.go.kr/법령/공공기관의 운영에 관한 법률/(20240927,20400,20240326)/제4조",
                "url2": "https://www.law.go.kr/법령/공공기관의 운영에 관한 법률 시행령/(20230101,33078,20221220)/제4조"
            }
        },
        "공사법": {
            1: {
                "explanation": "법 제10조(사업)",
                "detailed_explanation": "한국농어촌공사는 농어촌정비법에 따른 농업생산기반 정비사업, 농지의 매수·매도·임대차, 농지의 재개발, 농업용수의 공급, 농어촌 주택개량자금의 조성 및 융자, 농지은행사업 등을 수행합니다. 이는 농업생산기반을 확충하고 농어촌의 발전을 도모하기 위한 공공기관의 핵심 사업입니다.",
                "url": "https://www.law.go.kr/법령/한국농어촌공사 및 농지관리기금법/(20220218,18403,20210817)/제10조"
            }
        },
        "직제규정": {
            1: {
                "explanation": "제2장 구성원",
                "detailed_explanation": "한국농어촌공사의 구성원은 이사장, 상임이사, 비상임이사, 사원으로 구성됩니다. 이사장은 공사를 대표하고 업무를 총괄하며, 상임이사는 이사장을 보좌하고 정관이 정하는 업무를 담당합니다. 비상임이사는 이사회에 참여하여 의사결정에 참여하고, 사원은 공사의 주주를 의미합니다.",
                "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 직제규정/(9999,20250101)/제2장"
            }
        },
        "취업규칙": {
            1: {
                "explanation": "제19조(연차휴가)",
                "detailed_explanation": "연차휴가는 1년간 80% 이상 출근한 직원에게 15일을 부여합니다. 3년 이상 계속 근로한 직원에 대해서는 기본 휴가일수에 최초 1년을 초과하는 계속 근로 연수 2년에 대하여 1일을 가산합니다. 가산휴가를 포함한 총 휴가일수는 30일을 한도로 하며, 1년간 80% 미만 출근한 직원에게는 1개월 개근 시 1일의 연차휴가를 부여합니다.",
                "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 취업규칙/(9999,20250101)/제19조"
            }
        },
        "인사규정": {
            1: {
                "explanation": "제5조(정의)",
                "detailed_explanation": "인사규정에서 '직원'이란 공사의 정규직원을 말하며, '임용'이란 신규채용, 승진, 전보, 파견, 겸임, 겸직, 휴직, 복직, 면직, 해임, 징계, 정직, 감봉, 견책을 말합니다. '승진'이란 직급이 상위 직급으로 올라가는 것을 의미하고, '전보'는 같은 직급 내에서 다른 직무로 이동하는 것을 말합니다.",
                "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 인사규정/(9999,20250101)/제5조"
            }
        },
        "행동강령": {
            1: {
                "explanation": "제28조(초과사례금의 신고방법 등)",
                "detailed_explanation": "임직원이 외부강의, 강연, 집필, 자문, 심사, 평가, 연구 등의 업무를 수행하고 받은 사례금이 월 10만원을 초과하는 경우, 해당 월 말일까지 행동강령책임관에게 신고해야 합니다. 이는 공정한 직무수행을 해치는 지시에 대한 처리와 관련된 규정으로, 임직원의 투명성과 청렴성을 확보하기 위한 제도입니다.",
                "url": "https://www.law.go.kr/학칙공단/한국농어촌공사 임직원 행동강령/(9999,20241231)/제28조"
            }
        },
        "회계기준": {
            1: {
                "explanation": "제109조(검사원의 임면)",
                "detailed_explanation": "검사원은 공사의 업무와 재산상황을 검사하는 역할을 담당합니다. 검사원은 이사회에서 선임하며, 공사의 임원이나 직원을 겸할 수 없습니다. 검사원은 공사의 업무집행상황과 재산상황을 검사하여 이사회에 보고하고, 필요시 이사회 소집을 요구할 수 있습니다.",
                "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 공기업·준정부기관회계기준 시행세칙/(9999,20250301)/제109조"
            }
        }
    }
    
    return detailed_explanations

def update_exam_file_with_detailed_explanations():
    """2025-exam.js 파일에 상세한 해설을 추가합니다."""
    
    # 상세한 해설 데이터 생성
    detailed_explanations = create_detailed_explanations()
    
    # 2025-exam.js 파일 읽기
    with open('2025-exam.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 각 과목별로 상세한 해설 추가
    for subject, questions in detailed_explanations.items():
        for question_num, explanation_data in questions.items():
            # 해당 문제 찾기
            pattern = rf'"{subject}":\s*\[(.*?)\]'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                subject_content = match.group(1)
                
                # 해당 문제 번호 찾기 (1부터 시작하는 인덱스)
                question_index = question_num - 1
                
                # 문제 패턴 찾기
                question_pattern = r'\{[^}]*"question"[^}]*\}'
                questions = re.findall(question_pattern, subject_content)
                
                if question_index < len(questions):
                    # 해당 문제의 explanation 필드 업데이트
                    old_explanation = r'"explanation":\s*""'
                    new_explanation = f'"explanation": "{explanation_data["explanation"]}", "detailed_explanation": "{explanation_data["detailed_explanation"]}"'
                    
                    # URL 필드 추가
                    if "url" in explanation_data:
                        new_explanation += f', "url": "{explanation_data["url"]}"'
                    elif "url1" in explanation_data:
                        new_explanation += f', "url1": "{explanation_data["url1"]}", "url2": "{explanation_data["url2"]}"'
                    
                    # 해당 문제만 업데이트
                    updated_question = re.sub(old_explanation, new_explanation, questions[question_index])
                    
                    # 전체 내용에서 해당 문제 업데이트
                    content = content.replace(questions[question_index], updated_question)
    
    # 업데이트된 내용 저장
    with open('2025-exam.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("상세한 해설이 성공적으로 추가되었습니다!")

if __name__ == "__main__":
    update_exam_file_with_detailed_explanations() 