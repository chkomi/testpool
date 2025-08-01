const quizData = [
    {
        question: "다음 농어촌민박사업자 중 시장·군수·구청장이 사업장의 폐쇄를 명하거나 6개월 이내의 기간을 정하여 그 사업의 전부 또는 일부의 정지를 명할 수 있는 경우에 해당하는 사업자만을 바르게 고른 것은?<br><br>- A사업자 : 6개월 이상 사업을 하지 않고 있다.<br>- B사업자 : 구청장이 필요하다고 인정하여 운영의 개선을 명하였으나 이행을 하지 않고 있다.<br>- C사업자 : 승인을 받지 않고 관광농원을 개발하였다.<br>- D사업자 : 한국농어촌공사로부터 관광농원을 양수 받은 양수인 D는 「농업·농촌 및 식품산업 기본법」 제3조제2호에 따른 농업인이다.<br>- E사업자 : 관광농원과 주말농원에 재배작물을 6개월 이상 경작하지 않고 있다.",
        a: "A, B 사업자",
        b: "B, C 사업자",
        c: "A, E 사업자",
        d: "B, D 사업자",
        correct: "b"
    },
    {
        question: "다음 중 농어촌정비법 제130조(벌칙) 조항에 따라 처벌이 위중한 순서로 바르게 나열한 것은?<br><br>㉠ 조성용지를 전매한 자<br>㉡ 농업생산기반시설관리자의 허락 없이 수문을 조작하거나 용수를 인수함으로써 농어촌용수의 이용ㆍ관리에 지장을 준 자<br>㉢ 사업정지명령을 받고도 그 기간 중에 사업을 하거나 사업장 폐쇄명령을 받고도 계속하여 사업을 한 자<br>㉣ 농업생산기반시설을 불법으로 점용하거나 사용한 자",
        a: "㉠ – ㉣ – ㉢ - ㉡",
        b: "㉡ – ㉠ – ㉣ - ㉢",
        c: "㉡ – ㉠ – ㉢ - ㉣",
        d: "㉢ – ㉣ – ㉡ - ㉠",
        correct: "b"
    },
    {
        question: "농어촌정비사업의 시행자는 농어촌정비사업을 시행하기 위하여 필요하면 측량ㆍ설계 및 공사감리를 한국농어촌공사 등 농어촌 정비업무와 관련 있는 자 중에서 대통령령으로 정하는 자에게 위탁할 수 있다. 다음 보기 중 대통령령으로 정하는 자에 항상 해당하는 것은 모두 몇 개인가?<br><br>㉠ 「엔지니어링산업 진흥법」 제21조에 따라 신고한 엔지니어링사업자<br>㉡ 「건설기술 진흥법」 제26조에 따라 등록을 한 건설엔지니어링사업자<br>㉢ 「기술사법」 제6조에 따라 등록을 한 기술사사무소<br>㉣ 농어촌지역개발 관련 연구를 목적으로 설립된 연구기관",
        a: "1개",
        b: "2개",
        c: "3개",
        d: "4개",
        correct: "c"
    },
    {
        question: "[농어촌정비법] 제9조 (농업생산기반 정비사업 시행계획의 수립 등)에 대한 내용에서 밑줄 친 부분 중에서 옳지 않은 내용은 모두 몇 개인가?",
        a: "4개",
        b: "3개",
        c: "2개",
        d: "1개",
        correct: "a"
    },
    {
        question: "[농어촌정비법] 제65조의5 (특정빈집에 대한 조치 등)에 대한 조문에서 각 [보기]에 포함된 두 개의 잘못 작성된 내용을 모두 올바르게 수정한 [보기]를 고르시오.",
        a: "농림축산식품부장관이 설치(X) → 시장ㆍ군수ㆍ구청장이 설치(O), 한 차례만 30일의 범위(X) → 한 차례만 60일의 범위(O)",
        b: "소유자가 정당한 사유라도(X) → 소유자가 정당한 사유 없이(O), 지방자치단체장령으로(X) → 국무총리령으로(O)",
        c: "홈페이지에 3회 이상 공고(X) → 홈페이지에 2회 이상 공고(O), 공고일 익일부터 60일 이내(X) → 공고한 날부터 90일 이내(O)",
        d: "소요된 비용을 빼고 지급해야만 하며(X) → 소요된 비용을 빼고 지급할 수 있으며(O), 보상액에 절반에 해당하는 금액을 공탁(X) → 보상액 두 배에 해당하는 금액을 공탁(O)",
        correct: "a"
    },
    {
        question: "[농어촌정비법시행령] 제24조 (농어촌용수구역)에서 제24조 3항에서 밑줄 친 시ㆍ군ㆍ구가 조례로 정하여야 할 각 호의 사항이 아닌 것을 고르시오.",
        a: "농어촌용수의 이용ㆍ배분 및 보전ㆍ관리에 관한 사항",
        b: "농어촌용수의 보전ㆍ관리를 위한 시설의 유지ㆍ관리 및 설치 비용의 상환에 관한 사항",
        c: "농어촌용수구역의 설정 목적 및 농어촌용수의 개발 및 이용계획",
        d: "농어촌용수의 보전ㆍ관리를 위한 시설의 운영ㆍ조작에 관한 사항",
        correct: "c"
    },
    {
        question: "[농어촌정비법] 제86조 (농어촌민박사업자의 신고)에 대한 조문에서 밑줄 친 제86조의 하위 항목 중에서 올바른 내용을 고르시오.",
        a: "제86조 ①항",
        b: "제86조 ④항",
        c: "제86조 ⑥항",
        d: "제86조 ⑨항",
        correct: "a"
    },
    {
        question: "[농어촌정비법 시행령] 제32조 (농업생산기반시설이나 용수의 사용허가에 따른 사용료의 징수)에서 세 개의 숫자(㉮ : 100분의 10, ㉯ : 100분의 5, ㉰ : 600분의 1)가 각각 몇 번씩 들어가는가?",
        a: "㉮ (3개), ㉯ (3개), ㉰ (0개)",
        b: "㉮ (2개), ㉯ (2개), ㉰ (2개)",
        c: "㉮ (2개), ㉯ (3개), ㉰ (1개)",
        d: "㉮ (3개), ㉯ (2개), ㉰ (1개)",
        correct: "c"
    },
    {
        question: "[농어촌정비법 시행령] 제44조 (수혜자총회 또는 대의원회의 운영)에서 ㉮~㉱에 해당하는 틀린 내용을 바르게 수정하려고 한다. 다음 중 수정사항이 올바른 것을 고르시오.",
        a: "㉮ => [농업인 삶의 질 향상 및 농촌지역 개발촉진사업]로 수정",
        b: "㉯ => [대의원 과반수의 출석과 출석자 과반수]로 수정",
        c: "㉰ => [3명 이상의 수혜자 또는 대의원이 서명 날인]로 수정",
        d: "㉱ => [인근 지역 토지의 개별공시지가]로 수정",
        correct: "b"
    },
    {
        question: "농업생산기반 정비사업 시행자 A에 대한 설명에서 농어촌정비법을 기준으로 판단했을 때 옳지 않은 것은?<br><br>농업생산기반 정비사업 시행자 A는 농업생산기반 정비사업 시행으로 조성된 재산 중 농업생산기반시설에 제공되지 아니한 간척지를 가지고 있다.",
        a: "A는 간척지를 매각하여 처분하였다.",
        b: "A는 간척지를 매각하기 위해 농림축산식품부장관의 승인을 받았다.",
        c: "A의 간척지가 국가가 시행한 농업생산기반 정비사업으로 조성된 간척지라면 그 매각 대금을 「한국농어촌공사 및 농지관리기금법」 제31조에 따른 농지관리기금에 내야 한다.",
        d: "간척지를 매각한 대금은 사용에 제한이 없기 때문에 A는 농어촌산업을 활성화하기 위한 기부금으로 사용하였다.",
        correct: "d"
    },
    {
        question: "농어촌정비법 제59조(생활환경정비사업 시행계획의 수립)의 내용 중 3항의 밑줄 친 대통령령으로 정하는 요건이란 무엇인가?",
        a: "사업 대상 면적이 10만㎡ 이상",
        b: "사업 대상 면적이 20만㎡ 이상",
        c: "사업 대상 면적이 30만㎡ 이상",
        d: "사업 대상 면적이 40만㎡ 이상",
        correct: "b"
    },
    {
        question: "농업생산기반 정비사업의 시행시 업무 절차를 바르게 나열한 것은?<br><br>㉠ 지역별ㆍ유형별 농업생산기반 정비계획 수립<br>㉡ 자원 조사<br>㉢ 농어촌 정비 종합계획 수립<br>㉣ 예정지 조사<br>㉤ 농업생산기반 정비사업 시행계획 수립<br>㉥ 농업생산기반 정비사업 기본계획 수립",
        a: "㉡ - ㉢ - ㉠ - ㉣ - ㉥ - ㉤",
        b: "㉡ - ㉢ - ㉣ - ㉠ - ㉥ - ㉤",
        c: "㉡ - ㉣ - ㉠ - ㉢ - ㉥ - ㉤",
        d: "㉣ - ㉡ - ㉢ - ㉠ - ㉥ - ㉤",
        correct: "a"
    },
    {
        question: "분사무소의 설치등기에 대한 설명에서 ㉠,㉡,㉢에 알맞은 각 숫자의 합은?<br><br>- 공사가 분사무소를 설치한 경우, 주된 사무소 소재지의 경우 ( ㉠ )주일이내에 그 설치된 분사무소의 명칭과 소재지 및 설치 연월일을 등기한다.<br>- 공사가 분사무소를 설치한 경우, 새로 설치된 분사무소 소재지의 경우 ( ㉡ )주일 이내에 법령에 명시된 사항을 등기한다.<br>- 공사가 분사무소를 설치한 경우, 이미 설치된 다른 분사무소 소재지의 경우 ( ㉢ )주일 이내에 새로 설치된 분사무소의 명칭과 소재지 및 설치 연월일을 등기한다.",
        a: "6",
        b: "7",
        c: "8",
        d: "9",
        correct: "c"
    },
    {
        question: "농지관리기금에서 융자를 받아 적합한 용도에 따른 사업을 시행한 경우 그 결과 발생하는 손익은 기금에 귀속된다. 이 때 기금에 귀속되는 손익(損益)으로 알맞은 것을 모두 고른 것은?<br><br>㉠ 농지연금 위험부담금<br>㉡ 농지의 임차료와 임대료의 차액<br>㉢ 농지연금채권에 대한 이자<br>㉣ 농지의 임대료",
        a: "㉠, ㉡",
        b: "㉡, ㉢",
        c: "㉢, ㉣",
        d: "㉡, ㉣",
        correct: "d"
    },
    {
        question: "다음 중 매 회계연도 결산 결과 이익이 생겼을 때 업무를 처리하는 순서 바르게 나열한 것은?<br><br>㉠ 이월손실금의 보전(補塡)<br>㉡ 사업확장적립금 적립<br>㉢ 이익준비금 적립<br>㉣ 국고 납입",
        a: "㉠ - ㉡ - ㉢ - ㉣",
        b: "㉠ - ㉢ - ㉡ - ㉣",
        c: "㉡ - ㉢ - ㉠ - ㉣",
        d: "㉢ - ㉡ - ㉠ - ㉣",
        correct: "b"
    },
    {
        question: "[한국농어촌공사 및 농지관리기금법 시행령] 제19조의13(농지연금의 지급정지 및 회수 등)에서 3항의 끝 부분(공란)에 들어갈 내용으로 가장 부합되는 것을 고르시오.",
        a: "그 담보농지 부분에 대한 농지연금채권을 회수하고, 나머지 담보농지부분에 대한 농지연금은 지원하지 않는다.",
        b: "그 담보농지 부분에 대한 농지연금채권을 회수하고, 나머지 담보농지부분에 대하여 농지연금을 지원할 수 있다",
        c: "그 담보농지 부분에 대한 농지연금채무의 상환을 대납하고, 나머지 담보농지 부분에 대하여 농지연금을 지원할 수 있다",
        d: "그 담보농지 부분에 대한 농지연금채권을 회수하고, 담보농지 부분에 대한 농지연금 수혜자격을 해제할 수 있다.",
        correct: "b"
    },
    {
        question: "[한국농어촌공사 및 농지관리기금법 시행령] 제16조 (농지의 교환 또는 분리ㆍ합병 등)에서 [가] [나] 에 들어갈 적합한 단어를 고르시오. (단 [보기]의 순서는 [가], [나] 순서이다.)",
        a: "[농어촌정비법시행령] - [대통령령]",
        b: "[농어촌정비법시행령] - [농림축산식품부령]",
        c: "[농어촌정비법] - [농림축산식품부령]",
        d: "[농어촌정비법] - [대통령령]",
        correct: "c"
    },
    {
        question: "[한국농어촌공사 및 농지관리기금법 시행령] 제43조의2 (자료 및 정보의 제공 기관과 범위 등) 에서 밑줄 친 \"「OOOO법(률)」\"에 한 번도 들어가지 않는 법(률)은 무엇인가?",
        a: "공간정보의 구축 및 관리 등에 관한 법률",
        b: "국·공유 부동산의 등기·촉탁에 관한 법률",
        c: "농지법",
        d: "농업ㆍ농촌 공익기능 증진 직접지불제도 운영에 관한 법률",
        correct: "b"
    },
    {
        question: "[한국농어촌공사 및 농지관리기금법] 제10조 (사업)에서 밑줄 친 항목에 각각의 항목에 포함되는 사업명칭이 잘못 연결된 것을 고르시오.",
        a: "[7호] → 가축분뇨 처리시설 설치 및 지원",
        b: "[7호] → 토양오염에 관한 조사ㆍ평가 및 오염토양 개선사업",
        c: "[11호] → 농어촌 정주 지원 및 농어촌지역 투자 활성화",
        d: "[13호] → 내수면 수산자원 조성 및 유어기반 정비사업",
        correct: "b"
    },
    {
        question: "[한국농어촌공사 및 농지관리기금법]의 제23조 (농지매매사업금의 융자 등)의 내용에서 밑줄 친 '다음 각호의 사업'에 해당하지 않는 사업내용을 고르시오.",
        a: "제19조에 따른 '농지의 장기임대차사업'",
        b: "제21조에 따른 '직업을 전환한 농업인의 영농복귀 지원사업'",
        c: "제22조에 따른 '농지의 교환 또는 분리ㆍ합병사업'",
        d: "제24조의5에 따른 '농지를 담보로 한 농업인의 노후생활안정 지원사업'",
        correct: "b"
    },
    {
        question: "농지관리기금법 제12조(공사관리지역의 변경)에 관한 설명에서 각각의 옳고 그름을 순서대로 나열한 것은?<br><br>㉠ 공사는 새로운 농업기반시설을 관리ㆍ운영하는 등 농림축산식품부령으로 정하는 사유가 있는 경우에는 공사관리지역 외의 지역을 공사관리지역으로 편입할 수 있다.<br>㉡ 공사관리지역에 있는 토지가 대통령령으로 정하는 사유로 농업기반시설로부터 농업용수의 공급을 받을 수 없게 되었을 경우에는 그 토지의 이해관계인의 신청이나 농림축산식품부장관의 승인을 받아 직권으로 공사관리지역에서 제외할 수 있다.<br>㉢ 공사관리지역에서 제외하는 경우에는 농림축산식품부령으로 정하는 바에 따라 공사관리지역에서 제외하는 토지를 공고하여야 한다.",
        a: "X – O – O",
        b: "O – X – O",
        c: "X – X – O",
        d: "O – O – O",
        correct: "a"
    },
    {
        question: "「한국농어촌공사 및 농지관리기금법 시행령」제2조 (조성토지 등의 출자)와 관련한 내용에서 각 보기에 대한 O,X를 순서대로 나열한 것은?<br><br>㉠ 국가는 국가가 조성한 간척지, 매립지, 그 밖에 농림축산식품부장관이 지정한 토지를 공사에 출자할 수 있다.<br>㉡ 국가는 국가가 조성한 농업기반시설 중 농림축산식품부장관이 지정하는 부속시설의 관리권에 한하여 공사에 출자할 수 있다.<br>㉢ 국가가 공사에 출자하는 농업기반시설 부속시설의 관리권의 출자가액은 공사의 정관에서 정하는 방법으로 평가된 가액(價額)으로 한다.<br>㉣ 공사의 자본금은 5조원으로 하고, 전액을 국가가 출자(出資)하며 국가는 공사의 사업에 필요한 동산 또는 부동산을 공사에 현물로 출자할 수 있다.",
        a: "O – X – O - O",
        b: "O – O – O - X",
        c: "X – X – X - O",
        d: "X – X – O – O",
        correct: "c"
    },
    {
        question: "「공공기관의 운영에 관한 법률」제26조(준정부기관 임원의 임면)에서 임명권자가 같은 준정부기관 임원끼리 묶은 것은?<br><br>㉠ 총수입액이 1천억원 미만이고, 직원 정원이 500명 미만인 위탁집행형 준정부기관 장<br>㉡ 총수입액이 1천억원 미만이고, 직원 정원이 500명 미만인 위탁집행형 준정부기관 상임이사<br>㉢ 자산규모가 1조원 미만이고, 직원 정원이 500명 미만인 기금관리형 준정부기관 상임감사위원<br>㉣ 한국주택금융공사 비상임이사",
        a: "㉠ - ㉡",
        b: "㉠ - ㉣",
        c: "㉡ - ㉢",
        d: "㉡ - ㉣",
        correct: "c"
    },
    {
        question: "「공공기관의 운영에 관한 법률 시행령」의 내용에서 괄호 안에 들어갈 숫자가 큰 순서로 나열한 것은?<br><br>㉠ 제16조(통합공시) ② 기획재정부장관은 제1항에 따라 결정된 통합공시기준등에 관한 사항을 변경하는 경우에는 운영위원회의 심의ㆍ의결을 거쳐 확정한 후 변경된 통합공시기준등을 적용하기 ( )일 전까지 공공기관의 장에게 통보하여야 한다.<br>㉡ 제26조(결산서 제출) ② 준정부기관은 법 제43조제2항에 따라 확정한 결산서를 확정한 날로부터 ( )일 이내에 기획재정부장관에게 제출하여야 한다.<br>㉢ 제24조(임원후보자의 모집) ① 임원후보자를 공개모집하는 경우에는 해당 공기업ㆍ준정부기관의 인터넷 홈페이지 및 1개 이상의 일간지에 공고하되, 그 모집기간을 ( )주 이상으로 하여야 한다.",
        a: "㉠ > ㉡ > ㉢",
        b: "㉠ > ㉢ > ㉡",
        c: "㉡ > ㉠ > ㉢",
        d: "㉡ > ㉢ > ㉠",
        correct: "a"
    },
    {
        question: "[공공기관의 운영에 관한 법률 시행령] 제23조 [임원추천위원회의 구성 및 운영]에서 틀린 부분을 올바르게 수정하려고 한다. 다음 중에서 올바른 수정이 아닌 것을 고르시오.",
        a: "㉠ [임명권자와 제청권자가 합의해] -> [임명권자 또는 재청권자와 협의해]",
        b: "㉡ [위원 정수를 3명] -> [위원 정수를 2명]",
        c: "㉢ [구성원의 의견을 대변할 수 있는 사람 2명] -> [구성원의 의견을 대변할 수 있는 사람 1명]",
        d: "㉣ [재적위원 3분의 2이상의 찬성] -> [재적위원 과반수의 찬성]",
        correct: "b"
    },
    {
        question: "[공공기관의 운영에 관한 법률 시행령] 제25조의 3 [예비타당성조사]에서 13개의 [공란]에 들어갈 주체(단어) 중에 [기관장]과 [기획재정부장관]은 각각 몇 번씩 들어가는가?",
        a: "[기관장] = (6번) , [기획재정부장관] = (6번)",
        b: "[기관장] = (5번) , [기획재정부장관] = (7번)",
        c: "[기관장] = (6번) , [기획재정부장관] = (5번)",
        d: "[기관장] = (5번) , [기획재정부장관] = (6번)",
        correct: "d"
    },
    {
        question: "[공공기관의 운영에 관한 법률 시행령]의 제6조[총수입액 등의 산정방법]에서 세 개의 [공란]에는 특정한 숫자가 기입되어야 한다. [㉠], [㉡], [㉢]에 들어갈 숫자를 각각 구하시오. (단 각 [보기]의 기재 순서는 [㉠], [㉡], [㉢] 순서이다.)",
        a: "[3] - [2] - [3]",
        b: "[2] - [3] - [2]",
        c: "[3] - [3] - [3]",
        d: "[2] - [2] - [2]",
        correct: "c"
    },
    {
        question: "[공공기관의 운영에 관한 법률]의 제48조[경영실적 평가]에 관한 내용에서 올바른 내용을 고르시오.",
        a: "기획재정부장관은 경영실적 평가 결과 경영실적이 부진한 공기업ㆍ준정부기관에 대하여 운영위원회의 심의ㆍ의결을 거쳐 제25조(공기업임원의 임면) 및 제26조(준정부기관 임원의 임면)의 규정에 따른 기관장ㆍ상임이사에게 해임을 명할 수 있다.",
        b: "기획재정부장관은 경영실적 평가의 효율적인 수행과 경영실적 평가에 관한 전문적ㆍ기술적인 연구 또는 자문을 위하여 공기업ㆍ준정부기관운영심의회(이하 운영심의회)를 구성ㆍ운영할 수 있다.",
        c: "제1항에 따른 경영실적 평가의 절차, 경영실적 평가 결과에 따른 조치 및 경영평가단의 구성ㆍ운영 등에 관하여 필요한 사항은 대통령령으로 정한다.",
        d: "기획재정부장관은 제1항에 따른 경영실적 평가 결과 인건비 과다편성 및 제50조제1항에 따른 경영지침 위반으로 경영부실을 초래한 공기업·준정부기관에 대하여는 경영평가단의 심의·의결을 거쳐 향후 경영책임성 확보 및 경영개선을 위하여 필요한 인사상 또는 예산상의 조치 등을 취하도록 요청할 수 있다.",
        correct: "c"
    },
    {
        question: "경영목표의 수립에 대한 설명에서 ㉠,㉡,㉢,㉣에 각 들어갈 내용으로 알맞은 것은?<br><br>- 기관장은 사업내용과 경영환경, 제31조제3항 및 제4항의 규정에 따라 체결한 계약의 내용 등을 고려하여 다음 연도를 포함한 ( ㉠ )회계연도 이상의 중장기 경영목표를 설정하고, 이사회의 의결을 거쳐 확정한 후 매년 10월 31일까지 ( ㉣ )에게 제출하여야 한다.<br>- 기관장은 제1항의 규정에 불구하고 제6조의 규정에 따라 공기업ㆍ준정부기관으로 지정(변경지정을 제외한다)된 해에는 지정 후 ( ㉡ )월 이내에 당해 연도를 포함한 ( ㉢ )회계연도 이상의 중장기 경영목표를 설정하고, 이사회의 의결을 거쳐 확정한 후 이를 ( ㉣ )에게 제출하여야 한다.",
        a: "㉠ 3 ㉡ 3 ㉢ 3 ㉣ 기획재정부장관과 주무기관의 장",
        b: "㉠ 3 ㉡ 5 ㉢ 5 ㉣ 기획재정부장관",
        c: "㉠ 5 ㉡ 3 ㉢ 3 ㉣ 기획재정부장관과 주무기관의 장",
        d: "㉠ 5 ㉡ 3 ㉢ 5 ㉣ 기획재정부장관",
        correct: "c"
    },
    {
        question: "다음 밑줄 친 비위행위에 해당하지 않는 것은?",
        a: "해당 공공기관의 공금, 재산 또는 물품의 횡령, 배임, 절도, 사기 또는 유용(流用)",
        b: "법령이나 정관ㆍ내규 등을 위반하여 채용ㆍ승진 등 인사에 개입하거나 영향을 주는 행위로서 인사의 공정성을 현저하게 해치는 행위",
        c: "「성폭력범죄의 처벌 등에 관한 특례법」 제2조에 따른 성폭력범죄",
        d: "직무와 관련하여 권한 이상을 개입함으로써 업무상 계약의 효율성을 저하하는 행위",
        correct: "d"
    },
    {
        question: "다음 직위들을 직급별로 바르게 구분한 것은?<br><br>㉠ 연구위원<br>㉡ 전임교수<br>㉢ 연구원<br>㉣ 선임연구원<br>㉤ 책임연구원<br>㉥ 사원<br>㉦ 전임강사<br>㉧ 수석연구원",
        a: "5급 - ㉢, ㉤, ㉥",
        b: "4급 - ㉠, ㉣",
        c: "3급 - ㉡, ㉧",
        d: "1·2급 - ㉠, ㉦, ㉧",
        correct: "c"
    },
    {
        question: "[직제규정] '제2장 (구성원)'에 대한 내용에서 올바른 내용을 모두 고르시오.",
        a: "직원은 특정직 및 사원으로 구분한다.",
        b: "일반직은 행정직과 기술직, 전문직으로 하고 직급은 1급에서 5급으로 구분한다.",
        c: "공사는 필요에 따라 예산의 범위에서 계약직사원 및 보조적 업무 수행에 필요한 임시직원을 둘 수 있다.",
        d: "별정직은 비상계획관, 예비군지휘관 등 특수 업무 수행 직원으로 하며, 직급 구분은 전문직에 준한다.",
        correct: "a"
    },
    {
        question: "다음 중 본사에 있는 부서 중 소속을 바르게 짝지은 것은?",
        a: "기획관리이사 – 기획관리실, 기반사업처, 대단위간척처",
        b: "기반조성이사 – 기반사업처, 환경지질처, 보상사업처",
        c: "수자원관리이사 – 농촌개발처, 어촌수산처, 지역개발지원단",
        d: "농지관리이사 – 총무인사처, 농지은행처, 기금관리처",
        correct: "d"
    },
    {
        question: "다음 중 공사 취업규칙에 따른 공가 대상에 해당하지 않는 것은?",
        a: "국회의원 총선으로 인한 투표참여",
        b: "공사 재해보상규정에 따른 공상으로 근무하지 못하는 6개월 이내의 기간 (병가기간 포함)",
        c: "전염병에 걸린 해당 직원의 출근이 다른 직원에 영향을 미칠 우려가 있을 때",
        d: "공사의 업무와 관련된 자격을 보유한 직원이 관련법에 따라 교육을 받을 때",
        correct: "c"
    },
    {
        question: "한국농어촌공사의 취업규칙 중 [전보]에 관련한 조문에서 수정이 필요한 부분은 모두 몇 개인가?",
        a: "6개",
        b: "5개",
        c: "4개",
        d: "3개",
        correct: "b"
    },
    {
        question: "한국농어촌공사의 취업규칙에 대한 몇 가지 내용 중에서 올바른 발언을 고르시오.",
        a: "모성보호시간과 관련하여 생후 10개월 미만의 유아를 가진 여직원에게는 1일 2회 각각 30분 이상의 유급 수유시간을 주어야 합니다.",
        b: "가족돌봄휴가 기간은 가족돌봄휴직 기간에 포함된다.",
        c: "직원이 유연근무를 신청한 경우, 사장은 직무수행에 특별한 지장이 없으면 이에 대한 허락을 고려해야 한다. 단 유연근무를 이유로 부당한 불이익을 주어서는 아니 된다.",
        d: "18세 이상의 여직원은 오후 10시부터 오전 6시까지의 시간 및 휴일에 근로를 시키려면 반드시 근로개시시점 1일 전까지 당사자의 서면동의가 필요하다.",
        correct: "b"
    },
    {
        question: "공사 취업규칙 상 근로시간에 대한 설명에서 빈 칸에 알맞은 숫자를 차례대로 묶은 것으로 옳은 것은?<br><br>㉠ 사장은 2주 이내의 일정한 단위기간을 평균하여 1주 간의 근로시간이 ( )시간을 초과하지 아니하는 범위에서 근로시간을 초과하여 근로하게 할 수 있다. 다만, 특정한 주의 근로시간은 ( )시간을 초과할 수 없다.<br>㉡ 사장은 3개월 이내의 단위기간을 평균하여 1주 간의 근로시간이 ( )시간을 초과하지 아니하는 범위에서 근로시간을 초과하여 근로하게 할 수 있다. 다만, 특정한 주의 근로시간은 ( )시간을, 특정한 날의 근로시간은 ( )시간을 초과할 수 없다.",
        a: "40 – 52 – 40 – 48 - 8",
        b: "40 – 48 – 40 – 52 - 8",
        c: "40 – 48 – 40 – 52 - 12",
        d: "40 – 52 – 40 – 48 – 12",
        correct: "c"
    },
    {
        question: "다음 중 빈칸에 들어갈 용어를 순서대로 짝지은 것은?<br><br>( )란 1명의 직원에게 부여할 수 있는 직무와 책임을 말한다.<br>( )란 직무의 종류, 곤란성과 책임도가 상당히 유사한 직위의 군을 말한다.<br>( )란 동일한 직급 내에서 보직을 변경시킴을 말한다.",
        a: "직급 – 직책 - 전배",
        b: "직급 – 직위 - 전보",
        c: "직위 – 직급 - 전보",
        d: "직위 – 직위 – 전배",
        correct: "c"
    },
    {
        question: "[인사규정] 제22조 (승진에 걸리는 최저 근속기간)에서 제22조 제1항에서 규정하는 최저근속기간에 넣어 계산되는 경우로 옳은 것을 보기에서 모두 고른 것은?<br><br>[보기]<br>㉠ 업무상 사유에 의한 신체상의 장애로 장기요양을 위해 신청한 휴직기간<br>㉡ ｢병역법｣에 따른 병역의무를 마치기 위하여 징집 또는 소집된 때 경우 신청한 휴직기간<br>㉢ 선거 입후보 등 공민권 행사를 위해 신청한 휴직기간<br>㉣ 연구기관이나 교육기관에서 연수하기 위해 신청한 휴직기간<br>㉤ 국제기구에 임시로 고용되어 신청한 휴직기간<br>㉥ 질병으로 인하여 부모를 돌보기 위해 신청한 휴직기간",
        a: "㉠, ㉡, ㉤",
        b: "㉠, ㉢, ㉤",
        c: "㉠, ㉢, ㉥",
        d: "㉡, ㉣, ㉤",
        correct: "a"
    },
    {
        question: "한국농어촌공사 인사규정 중 상급인사위원회와 보통인사위원회의 구성에 대한 내용에서 옳지 않은 것을 고르시오.",
        a: "㉠: 상급인사위원회와 보통인사위원회 위원장의 임명권자는 사장으로 동일하다.",
        b: "㉡: 상급인사위원회와 보통인사위원회의 구성 위원 수는 6명 이상 8명 이하로 동일하다.",
        c: "㉢: 상급인사위원회와 보통인사위원회 모두 중징계 처분에 대한 심의를 위한 외부위원 1인의 추천 권한은 노동조합 위원장이 갖는다.",
        d: "㉣: 상급인사위원회와 보통인사위원회의 간사로는 인사담당 부서장이 선임된다.",
        correct: "d"
    },
    {
        question: "다음 중 특별승진을 시킬 수 있는 경우를 모두 고른 것은?<br><br>㉠ 승진한 후 2년이 경과하고 재직 중 공적이 특히 현저한 2급 부장이 공무로 인하여 사망한 때<br>㉡ 승진한 후 5년이 경과하고 재직 중 공적이 특히 현저한 3급 차장이 명예퇴직 할 때<br>㉢ 승진한 후 3년이 경과하고 지식제안규정에 따라 1~2등급으로 채택된 3급 차장<br>㉣ 승진한 후 4년이 경과하고 직무수행이 탁월하여 공사의 경영개선에 지대한 공적이 객관적으로 입증되는 4급 과장",
        a: "㉡",
        b: "㉡, ㉣",
        c: "㉠, ㉡, ㉣",
        d: "㉠, ㉢, ㉣",
        correct: "c"
    },
    {
        question: "본사에서 재직 중인 K 부장이 직무와 관련하여 요청받은 외부강의를 다녀 온 상황에서 임직원 행동강령의 규정의 내용과 맞지 않은 것은?<br><br>K 부장은 직무와 관련하여 영리 단체로부터 외부강의 요청을 받았다. ㉠ K 부장은 행동강령책임관에게 관련 사항을 미리 신고를 하였으며, 신고 할 때 사례금 총액을 미리 알 수 없어 그 사항은 제외하고 신고를 하였다. 신고 내용을 확인 행동강령책임관은 신고한 외부강의가 공정한 직무수행을 저해할 수 있는지를 검토하였고 이상 없음을 확인하였다. 외부강의에 다녀온 K 부장은 ㉡ 강의 당일 사례금을 지급받았고, 그로부터 3일 후 사전 신고 사항에 빠져 있던 사례금 정보를 보완하였다. 그리고 ㉢ 사례금이 공사 규정을 초과하여 이를 행동강령책임관에게 신고하고 초과금액을 강의를 요청한 영리 단체에 반환하였다. 이 때, ㉣ 반환 비용이 발생하여 증명자료를 첨부한 후 행동강령책임관에게 청구하였고 해당 반환 비용을 돌려받았다.",
        a: "㉠",
        b: "㉡",
        c: "㉢",
        d: "㉣",
        correct: "d"
    },
    {
        question: "[한국농어촌공사 임직원행동강령]의 제21조(알선ㆍ청탁 등의 금지)에 관한 내용에서 옳지 않은 항목은 모두 몇 개인가?",
        a: "없음",
        b: "1개",
        c: "2개",
        d: "3개",
        correct: "b"
    },
    {
        question: "[한국농어촌공사 임직원행동강령]의 제13조에서 [퇴직자와의 사전접촉 신고]에 해당하지 않는 예시를 고르시오.",
        a: "직무관련 퇴직자가 함께 가자고 소개한 경마장을 사전에 먼저 방문을 하는 행위",
        b: "직무관련 퇴직자 본인 명의의 법인이 비용을 부담하는 약간의 반주를 동반한 식사",
        c: "직무관련 퇴직자와 각자 부담으로 여행 및 골프를 함께 하는 행위",
        d: "직무관련 퇴직자 본인이 아닌, 퇴직자 본인을 후원하는 사람이 비용을 부담하는 식사(단 음주는 제외)",
        correct: "a"
    },
    {
        question: "[임직원 행동강령] 제29조 (직무관련자 등과의 거래 신고)에서 각 항(또는 각호)에 해당하는 단서조항에 대한 설명으로 잘못된 내용은 무엇인가?",
        a: "㉠ 다만,「금융실명거래 및 비밀보장에 관한 법률」제2조제1호에 따른 금융회사등으로부터 통상적인 조건으로 금전을 빌리는 행위 및 유가증권을 거래하는 행위는 제외한다.",
        b: "㉡ 다만, 공매·경매·입찰 및 공개추첨(이하 \"공매 등\"이라 한다)을 통한 거래 행위는 제외한다.",
        c: "㉢ 다만, 공매 등을 통한 계약 체결 행위 또는 거래관행상 특정한 집단을 대상으로 비정기적으로 반복적으로 행해지는 계약 체결 행위는 제외한다.",
        d: "㉣ 다만, 그 직무관련자 또는 직무관련임직원과 관련된 직무 수행이 종료된 날부터 2년이 지난 경우에는 그러하지 아니하다.",
        correct: "c"
    },
    {
        question: "회계관계직원의 재정보증에 관련된 내용에서 옳지 않은 것은?",
        a: "재정보증설정액은 1억원으로 하며, 보증보험가입에 따른 보험료는 공사가 부담한다.",
        b: "회계관계직원은 재정보증 없이는 그 직무를 담당 할 수 없다.",
        c: "회계관계직원이란 재무담당 상임이사와 공기업준정부기관 회계기준시행세칙 제6조 제1항에 따른 회계담당 및 그 보조자를 말한다.",
        d: "재정보증은 특별한 사유가 없으면 직위포괄계약방식을 원칙으로 한 보증보험의 가입으로 한다.",
        correct: "b"
    },
    {
        question: "[공기업․준정부기관 회계기준 시행세칙]에서 [제55조]에서 [제59조]까지의 조문에서 ㉮~㉵ 중에서 잘못된 내용을 모두 고르시오.",
        a: "㉮, ㉯, ㉱, ㉲",
        b: "㉯, ㉰, ㉲, ㉳",
        c: "㉮, ㉰, ㉲, ㉴",
        d: "㉯, ㉱, ㉴, ㉵",
        correct: "c"
    },
    {
        question: "[공기업ㆍ준정부기관회계기준 시행세칙]의 제3절 '장부'에 대한 내용에서 밑줄 친 부분에 대한 수정사항이 올바르지 못한 것은?",
        a: "(가) : [출납장을 3권 이상~] → [출납장을 2권 이상]",
        b: "(나) : [대륙식] → [영미식]",
        c: "(다) : [계정의 모든 총액] → [계정의 모든 잔액]",
        d: "(라) : [~기입은 매일 검열하여야~] → [~기업은 매주 검열하여야~]",
        correct: "d"
    },
    {
        question: "공기업․준정부기관 회계기준 시행세칙에서 규정된 추정가격 2천만원 이상의 수의계약 진행 절차를 순서대로 나열한 것은?<br><br>㉠ 수의계약 적정성에 대한 위원회 심의<br>㉡ 공사 홈페이지에 5일간 수의계약안을 사전공개<br>㉢ 의견수렴<br>㉣ 업체로부터 퇴직자 영입현황 확인서(임원 및 계약관련 업무담당직원 명단) 징구<br>㉤ 수의계약 체결<br>㉥ 수의계약 여부 결정",
        a: "㉠ - ㉡ - ㉢ - ㉥ - ㉣ - ㉤",
        b: "㉡ - ㉢ - ㉠ - ㉥ - ㉣ - ㉤",
        c: "㉡ - ㉢ - ㉠ - ㉥ - ㉤ - ㉣",
        d: "㉢ - ㉡ - ㉠ - ㉥ - ㉣ - ㉤",
        correct: "b"
    },
    {
        question: "공기업․준정부기관 회계기준 시행세칙에서 규정된 계약목적물에 하자가 발생했을 시 하자조치 업무의 처리 순서로 알맞은 것은? (단, 지정기일까지 하자보수를 이행하지 않았다고 가정한다.)<br><br>㉠ 직영보수<br>㉡ 계약담당부서장에게 통보<br>㉢ 하자보수보증금 전액 공사 귀속<br>㉣ 하자보수 요청",
        a: "㉣ - ㉠ - ㉢ - ㉡",
        b: "㉣ - ㉠ - ㉡ - ㉢",
        c: "㉣ - ㉢ - ㉡ - ㉠",
        d: "㉣ - ㉡ - ㉢ - ㉠",
        correct: "d"
    }
];

// 문제 순서를 랜덤으로 섞기
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// 문제 순서를 랜덤으로 섞어서 저장
const shuffledQuizData = shuffleArray(quizData.map((q, index) => ({...q, originalIndex: index + 1})));

let currentQuiz = 0;
let score = 0;
let userAnswers = [];
let questionAnswered = false;

const quiz = document.getElementById('quiz');
const question = document.getElementById('question');
const aText = document.getElementById('a_text');
const bText = document.getElementById('b_text');
const cText = document.getElementById('c_text');
const dText = document.getElementById('d_text');
const submitBtn = document.getElementById('submit');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const questionCounter = document.getElementById('question-counter');
const result = document.getElementById('result');

loadQuiz();

function loadQuiz() {
    deselectAnswers();
    questionAnswered = false;
    
    const currentQuizData = shuffledQuizData[currentQuiz];
    
    question.innerHTML = `${currentQuiz + 1}. ${currentQuizData.question}`;
    aText.innerText = currentQuizData.a;
    bText.innerText = currentQuizData.b;
    cText.innerText = currentQuizData.c;
    dText.innerText = currentQuizData.d;
    
    questionCounter.innerText = `${currentQuiz + 1} / ${shuffledQuizData.length}`;
    
    // 피드백 메시지 숨기기
    hideFeedback();
    
    // 모든 선택지의 스타일 초기화
    resetOptionStyles();
    
    // 이전에 선택한 답안이 있으면 복원하고 피드백 표시
    if (userAnswers[currentQuiz]) {
        const selectedAnswer = document.getElementById(userAnswers[currentQuiz]);
        if (selectedAnswer) {
            selectedAnswer.checked = true;
            showFeedback(userAnswers[currentQuiz]);
            questionAnswered = true;
        }
    }
    
    // 버튼 상태 업데이트
    prevBtn.disabled = currentQuiz === 0;
    nextBtn.style.display = 'inline-block';
    submitBtn.style.display = currentQuiz === shuffledQuizData.length - 1 ? 'inline-block' : 'none';
    
    // 답변이 완료된 경우 다음 버튼 활성화
    updateNextButtonState();
}

function deselectAnswers() {
    const answerElements = document.querySelectorAll('.answer');
    answerElements.forEach(answerEl => answerEl.checked = false);
}

function getSelected() {
    const answerElements = document.querySelectorAll('.answer');
    let answer;
    answerElements.forEach(answerEl => {
        if (answerEl.checked) {
            answer = answerEl.id;
        }
    });
    return answer;
}

// 피드백 표시 함수
function showFeedback(selectedAnswer) {
    const currentQuizData = shuffledQuizData[currentQuiz];
    const correctAnswer = currentQuizData.correct;
    const isCorrect = selectedAnswer === correctAnswer;
    
    // 기존 피드백 제거
    hideFeedback();
    
    // 선택지들에 스타일 적용
    const allLabels = document.querySelectorAll('ul li label');
    allLabels.forEach((label, index) => {
        const optionLetter = ['a', 'b', 'c', 'd'][index];
        const li = label.parentElement;
        
        if (optionLetter === selectedAnswer) {
            // 선택한 답안
            if (isCorrect) {
                li.classList.add('selected-correct');
            } else {
                li.classList.add('selected-incorrect');
            }
        } else if (optionLetter === correctAnswer) {
            // 정답 표시
            li.classList.add('correct-answer');
        }
    });
    
    // 피드백 메시지 생성
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
    feedbackDiv.innerHTML = `
        <div class="feedback-content">
            <span class="feedback-icon">${isCorrect ? '✓' : '✗'}</span>
            <span class="feedback-text">
                ${isCorrect ? '정답입니다!' : `오답입니다. 정답: ${correctAnswer.toUpperCase()}`}
            </span>
        </div>
    `;
    
    // 문제 영역 바로 아래에 피드백 추가
    const questionDiv = document.getElementById('question');
    questionDiv.parentNode.insertBefore(feedbackDiv, questionDiv.nextSibling);
    
    questionAnswered = true;
}

// 피드백 숨기기 함수
function hideFeedback() {
    const existingFeedback = document.querySelector('.feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
}

// 선택지 스타일 초기화 함수
function resetOptionStyles() {
    const allLis = document.querySelectorAll('ul li');
    allLis.forEach(li => {
        li.classList.remove('selected-correct', 'selected-incorrect', 'correct-answer');
    });
}

// 다음 버튼 상태 업데이트
function updateNextButtonState() {
    if (questionAnswered) {
        nextBtn.disabled = false;
        nextBtn.textContent = currentQuiz === shuffledQuizData.length - 1 ? '결과 보기' : '다음';
    } else {
        nextBtn.disabled = true;
        nextBtn.textContent = '다음';
    }
}

// 답안 선택 시 즉시 피드백 표시 (이벤트 위임 사용)
document.addEventListener('change', (e) => {
    if (e.target.classList.contains('answer') && !questionAnswered) {
        const selectedAnswer = getSelected();
        if (selectedAnswer) {
            userAnswers[currentQuiz] = selectedAnswer;
            showFeedback(selectedAnswer);
            updateNextButtonState();
        }
    }
});

prevBtn.addEventListener('click', () => {
    const answer = getSelected();
    if (answer) {
        userAnswers[currentQuiz] = answer;
    }
    
    if (currentQuiz > 0) {
        currentQuiz--;
        loadQuiz();
    }
});

nextBtn.addEventListener('click', () => {
    if (questionAnswered) {
        if (currentQuiz === shuffledQuizData.length - 1) {
            // 마지막 문제인 경우 결과 표시
            calculateScore();
            showResults();
        } else {
            currentQuiz++;
            loadQuiz();
        }
    } else {
        alert('답안을 선택해주세요.');
    }
});

submitBtn.addEventListener('click', () => {
    if (questionAnswered) {
        calculateScore();
        showResults();
    } else {
        alert('답안을 선택해주세요.');
    }
});

// 점수 계산 함수
function calculateScore() {
    score = 0;
    for (let i = 0; i < shuffledQuizData.length; i++) {
        if (userAnswers[i]) {
            const correctAnswer = shuffledQuizData[i].correct;
            if (userAnswers[i] === correctAnswer) {
                score++;
            }
        }
    }
}

function showResults() {
    quiz.innerHTML = `
        <div class="result">
            <h2>시험 결과</h2>
            <p>총 ${shuffledQuizData.length}문제 중 ${score}문제 정답</p>
            <p>정답률: ${(score / shuffledQuizData.length * 100).toFixed(1)}%</p>
            <div class="detailed-results">
                <h3>상세 결과</h3>
                ${getDetailedResults()}
            </div>
            <button onclick="location.reload()">다시 풀기</button>
            <button onclick="location.href='index.html'">메인으로</button>
        </div>
    `;
}

function getDetailedResults() {
    let detailedHTML = '';
    for (let i = 0; i < shuffledQuizData.length; i++) {
        const userAnswer = userAnswers[i];
        const questionData = shuffledQuizData[i];
        const correctAnswer = questionData.correct;
        const isCorrect = userAnswer === correctAnswer;
        
        const options = {
            'a': questionData.a,
            'b': questionData.b,
            'c': questionData.c,
            'd': questionData.d
        };
        
        detailedHTML += `
            <div class="question-result ${isCorrect ? 'correct' : 'incorrect'}">
                <p><strong>문제 ${i + 1} (원래 ${questionData.originalIndex}번):</strong> ${isCorrect ? '정답' : '오답'}</p>
                <p><strong>정답:</strong> ${correctAnswer.toUpperCase()}. ${options[correctAnswer]}</p>
                ${userAnswer ? `<p><strong>선택한 답:</strong> ${userAnswer.toUpperCase()}. ${options[userAnswer]}</p>` : '<p><strong>선택한 답:</strong> 미선택</p>'}
            </div>
        `;
    }
    return detailedHTML;
}