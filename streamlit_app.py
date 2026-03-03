import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="Element MBTI Matcher",
    page_icon="🧪",
    layout="centered"
)

# 데이터 정의
QUESTIONS = [
    {
        "id": 1,
        "text": "주말에 당신은 주로 무엇을 하며 시간을 보내나요?",
        "dimension": "EI",
        "options": [
            {"text": "친구들을 만나거나 밖으로 나가 에너지를 얻는다.", "value": "E"},
            {"text": "집에서 혼자만의 시간을 가지며 재충전한다.", "value": "I"}
        ]
    },
    {
        "id": 2,
        "text": "새로운 사람을 만났을 때 당신은?",
        "dimension": "EI",
        "options": [
            {"text": "먼저 말을 걸고 대화를 주도하는 편이다.", "value": "E"},
            {"text": "상대방이 먼저 말을 걸어줄 때까지 기다리는 편이다.", "value": "I"}
        ]
    },
    {
        "id": 3,
        "text": "다수의 사람들과 함께 있을 때 당신은?",
        "dimension": "EI",
        "options": [
            {"text": "분위기를 띄우고 대화의 중심에 있는 것을 즐긴다.", "value": "E"},
            {"text": "조용히 경청하며 필요한 말만 하는 편이다.", "value": "I"}
        ]
    },
    {
        "id": 4,
        "text": "사물을 바라볼 때 당신은?",
        "dimension": "SN",
        "options": [
            {"text": "현재의 사실과 구체적인 세부 사항에 집중한다.", "value": "S"},
            {"text": "미래의 가능성과 전체적인 흐름, 의미를 생각한다.", "value": "N"}
        ]
    },
    {
        "id": 5,
        "text": "새로운 일을 배울 때 선호하는 방식은?",
        "dimension": "SN",
        "options": [
            {"text": "직접 경험해보고 실질적인 예시를 통해 배운다.", "value": "S"},
            {"text": "원리와 개념을 먼저 이해하고 상상력을 발휘한다.", "value": "N"}
        ]
    },
    {
        "id": 6,
        "text": "이야기를 할 때 당신의 스타일은?",
        "dimension": "SN",
        "options": [
            {"text": "정확하고 묘사가 풍부하며 현실적인 이야기를 한다.", "value": "S"},
            {"text": "비유와 상징을 많이 사용하며 아이디어 중심의 이야기를 한다.", "value": "N"}
        ]
    },
    {
        "id": 7,
        "text": "결정을 내려야 할 때 당신은?",
        "dimension": "TF",
        "options": [
            {"text": "객관적인 논리와 원칙에 따라 판단한다.", "value": "T"},
            {"text": "사람들의 감정과 상황, 조화를 고려하여 판단한다.", "value": "F"}
        ]
    },
    {
        "id": 8,
        "text": "친구가 고민을 털어놓을 때 당신의 반응은?",
        "dimension": "TF",
        "options": [
            {"text": "상황을 분석하고 실질적인 해결책을 제시해준다.", "value": "T"},
            {"text": "친구의 감정에 공감해주고 위로의 말을 건넨다.", "value": "F"}
        ]
    },
    {
        "id": 9,
        "text": "비판을 받았을 때 당신은?",
        "dimension": "TF",
        "options": [
            {"text": "내용이 논리적으로 맞는지 따져보고 수용한다.", "value": "T"},
            {"text": "상대방의 말투나 감정적인 의도에 더 신경이 쓰인다.", "value": "F"}
        ]
    },
    {
        "id": 10,
        "text": "여행 계획을 세울 때 당신은?",
        "dimension": "JP",
        "options": [
            {"text": "시간별로 상세한 일정을 짜고 그대로 따르려 한다.", "value": "J"},
            {"text": "가고 싶은 곳 몇 군데만 정하고 상황에 따라 움직인다.", "value": "P"}
        ]
    },
    {
        "id": 11,
        "text": "과제를 하거나 일을 할 때 당신은?",
        "dimension": "JP",
        "options": [
            {"text": "미리 계획을 세워 마감 기한보다 일찍 끝내는 편이다.", "value": "J"},
            {"text": "마지막 순간에 집중력을 발휘하여 몰아서 하는 편이다.", "value": "P"}
        ]
    },
    {
        "id": 12,
        "text": "주변 환경이 정리되어 있지 않을 때 당신은?",
        "dimension": "JP",
        "options": [
            {"text": "불안함을 느끼며 바로 정리 정돈을 하고 싶어 한다.", "value": "J"},
            {"text": "크게 신경 쓰지 않으며 나중에 한꺼번에 정리한다.", "value": "P"}
        ]
    },
    {
        "id": 13,
        "text": "파티나 모임에서 당신은 주로 어떻게 행동하나요?",
        "dimension": "EI",
        "options": [
            {"text": "모르는 사람들과도 적극적으로 대화하며 새로운 인맥을 쌓는다.", "value": "E"},
            {"text": "주로 아는 사람들과 대화하며 조용히 시간을 보낸다.", "value": "I"}
        ]
    },
    {
        "id": 14,
        "text": "생각을 정리할 때 당신은 어떤 방식을 선호하나요?",
        "dimension": "EI",
        "options": [
            {"text": "말로 내뱉으면서 생각을 구체화하고 정리한다.", "value": "E"},
            {"text": "머릿속으로 충분히 생각한 뒤에 결론을 내린다.", "value": "I"}
        ]
    },
    {
        "id": 15,
        "text": "새로운 가전제품을 샀을 때 당신은?",
        "dimension": "SN",
        "options": [
            {"text": "설명서를 처음부터 끝까지 꼼꼼하게 읽어본다.", "value": "S"},
            {"text": "일단 이것저것 눌러보며 감으로 사용법을 익힌다.", "value": "N"}
        ]
    },
    {
        "id": 16,
        "text": "영화나 소설을 볼 때 당신이 더 흥미를 느끼는 부분은?",
        "dimension": "SN",
        "options": [
            {"text": "현실감 넘치는 묘사와 구체적인 사건 전개", "value": "S"},
            {"text": "작가가 숨겨놓은 상징적 의미와 복선, 철학적 메시지", "value": "N"}
        ]
    },
    {
        "id": 17,
        "text": "동료가 업무상 실수를 했을 때 당신의 첫 반응은?",
        "dimension": "TF",
        "options": [
            {"text": "무엇이 잘못되었는지 분석하고 해결책을 먼저 제시한다.", "value": "T"},
            {"text": "동료가 당황했을 마음을 먼저 다독이고 위로한다.", "value": "F"}
        ]
    },
    {
        "id": 18,
        "text": "당신이 생각하는 '공정함'의 기준은 무엇인가요?",
        "dimension": "TF",
        "options": [
            {"text": "예외 없이 누구에게나 동일한 규칙을 적용하는 것", "value": "T"},
            {"text": "개개인의 특별한 사정과 상황을 고려하여 대우하는 것", "value": "F"}
        ]
    },
    {
        "id": 19,
        "text": "일을 시작하기 전 당신의 책상 상태는 어떤가요?",
        "dimension": "JP",
        "options": [
            {"text": "깔끔하게 정리되어 있어야 집중이 잘 된다.", "value": "J"},
            {"text": "조금 어질러져 있어도 필요한 물건만 찾을 수 있으면 상관없다.", "value": "P"}
        ]
    },
    {
        "id": 20,
        "text": "약속 장소에 나갈 때 당신은 보통?",
        "dimension": "JP",
        "options": [
            {"text": "변수를 고려해 약속 시간보다 5~10분 일찍 도착한다.", "value": "J"},
            {"text": "시간에 딱 맞춰 도착하거나 가끔 조금 늦기도 한다.", "value": "P"}
        ]
    }
]

ELEMENT_RESULTS = {
    'ISTJ': {
        'symbol': 'Fe', 'name': '철 (Iron)', 'mbti': 'ISTJ',
        'description': '철은 구조물의 뼈대가 되는 가장 신뢰할 수 있는 원소입니다. ISTJ의 책임감 있고 현실적인 면모는 철이 지닌 견고함과 닮아 있습니다. 철이 문명을 지탱하듯, 당신은 조직의 중심을 든든하게 지탱하며 체계적인 질서를 유지하는 사람입니다.',
        'properties': ['견고함', '신뢰성', '실용주의', '체계적'],
        'atomicNumber': 26, 'atomicMass': '55.845 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=800&auto=format&fit=crop', 'usage': '건축 구조물 및 강철 생산',
        'bestMatch': {'mbti': 'ESFP', 'element': '구리', 'reason': '철의 견고한 구조와 구리의 뛰어난 전도성이 만나 안정적이면서도 활기찬 시너지를 냅니다.'}, 
        'worstMatch': {'mbti': 'ENFP', 'element': '산소', 'reason': '철이 산소를 만나면 부식되듯, 엄격한 질서가 자유분방함에 의해 약해질 수 있습니다.'}
    },
    'ISFJ': {
        'symbol': 'Au', 'name': '금 (Gold)', 'mbti': 'ISFJ',
        'description': '금은 변하지 않는 가치와 따뜻한 빛을 지닌 원소입니다. ISFJ의 헌신적이고 온화한 성품은 금의 불변성과 광택에 비견됩니다. 금이 소중한 가치를 보존하듯, 당신은 주변 사람들을 소중히 여기고 안정적인 환경을 만드는 수호자입니다.',
        'properties': ['불변성', '헌신', '온화함', '세심함'],
        'atomicNumber': 79, 'atomicMass': '196.966 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://images.unsplash.com/photo-1610375461246-83df859d849d?q=80&w=800&auto=format&fit=crop', 'usage': '장신구 및 화폐 가치 저장',
        'bestMatch': {'mbti': 'ESTP', 'element': '나트륨', 'reason': '금의 변치 않는 온화함이 나트륨의 폭발적인 에너지를 차분하게 감싸주며 완벽한 균형을 이룹니다.'}, 
        'worstMatch': {'mbti': 'ENTP', 'element': '인', 'reason': '안정을 추구하는 금의 성질이 끊임없이 변화하고 연소하는 인의 성질과 충돌할 수 있습니다.'}
    },
    'INFJ': {
        'symbol': 'Pt', 'name': '백금 (Platinum)', 'mbti': 'INFJ',
        'description': '백금은 희귀하며 강력한 촉매 역할을 하는 고귀한 원소입니다. INFJ의 깊은 통찰력과 이상적인 면모는 백금의 희귀성과 강력한 반응 유도 능력과 닮았습니다. 백금이 화학 반응을 이끌어내듯, 당신은 조용히 세상을 긍정적으로 변화시키는 힘을 가지고 있습니다.',
        'properties': ['희귀성', '통찰력', '고결함', '신비로움'],
        'atomicNumber': 78, 'atomicMass': '195.084 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '1735년',
        'imageUrl': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop', 'usage': '자동차 촉매 장치 및 고급 정밀 기기',
        'bestMatch': {'mbti': 'ENFP', 'element': '산소', 'reason': '백금 촉매가 산소와 결합하여 깨끗한 에너지를 만들듯, 두 유형은 서로의 이상을 실현하도록 돕습니다.'}, 
        'worstMatch': {'mbti': 'ESTP', 'element': '나트륨', 'reason': '고귀하고 신중한 백금의 성질이 나트륨의 즉흥적이고 강한 반응성과는 속도를 맞추기 어렵습니다.'}
    },
    'INTJ': {
        'symbol': 'C', 'name': '탄소 (Carbon)', 'mbti': 'INTJ',
        'description': '탄소는 생명의 근원이자 다이아몬드처럼 단단한 결합력을 가졌습니다. INTJ의 독립적이고 전략적인 지성은 탄소의 다재다능함과 강인한 결합 구조를 연상시킵니다. 탄소가 무한한 화합물을 만들듯, 당신은 자신만의 확고한 논리 체계를 구축하는 지략가입니다.',
        'properties': ['다재다능', '전략적', '독립성', '강인함'],
        'atomicNumber': 6, 'atomicMass': '12.011 u', 'category': '비금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://images.unsplash.com/photo-1512161775974-407f68c55b72?q=80&w=800&auto=format&fit=crop', 'usage': '다이아몬드, 연필심, 탄소 섬유',
        'bestMatch': {'mbti': 'ENTP', 'element': '인', 'reason': '탄소의 견고한 논리와 인의 창의적인 발광력이 만나 혁신적인 아이디어를 현실로 구현해냅니다.'}, 
        'worstMatch': {'mbti': 'ESFP', 'element': '구리', 'reason': '독립적이고 깊은 탄소의 성질이 사교적이고 에너지를 발산하는 구리의 성질과 평행선을 달릴 수 있습니다.'}
    },
    'ISTP': {
        'symbol': 'Ti', 'name': '티타늄 (Titanium)', 'mbti': 'ISTP',
        'description': '티타늄은 가볍지만 강철보다 강하며 실용적인 원소입니다. ISTP의 상황 적응력과 냉철한 판단력은 티타늄의 효율성과 내구성에 비견됩니다. 티타늄이 극한 환경에서도 견디듯, 당신은 도구를 잘 다루며 실질적인 해결책을 찾아내는 기술자입니다.',
        'properties': ['효율성', '적응력', '냉철함', '실무능력'],
        'atomicNumber': 22, 'atomicMass': '47.867 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '1791년',
        'imageUrl': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800&auto=format&fit=crop', 'usage': '항공우주 부품 및 인공 관절',
        'bestMatch': {'mbti': 'ESFJ', 'element': '알루미늄', 'reason': '티타늄의 강인함과 알루미늄의 유연한 협동심이 만나 가장 효율적인 기술적 조화를 이룹니다.'}, 
        'worstMatch': {'mbti': 'ENFJ', 'element': '수소', 'reason': '냉철하고 실무적인 티타늄의 성질이 감성적이고 이상적인 수소의 에너지와는 공감대를 찾기 어렵습니다.'}
    },
    'ISFP': {
        'symbol': 'Ag', 'name': '은 (Silver)', 'mbti': 'ISFP',
        'description': '은은 가장 높은 반사율을 가진 아름답고 유연한 원소입니다. ISFP의 풍부한 감수성과 예술적 기질은 은의 빛나는 광택과 유연한 성질과 닮았습니다. 은이 빛을 반사하여 아름다움을 전달하듯, 당신은 현재의 순간을 예술적으로 즐길 줄 아는 사람입니다.',
        'properties': ['예술성', '유연함', '겸손함', '감수성'],
        'atomicNumber': 47, 'atomicMass': '107.868 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://images.unsplash.com/photo-1517400473880-9946298f3366?q=80&w=800&auto=format&fit=crop', 'usage': '거울 코팅, 은식기, 전자 회로',
        'bestMatch': {'mbti': 'ESTJ', 'element': '칼슘', 'reason': '은의 섬세한 예술성과 칼슘의 든든한 지도력이 만나 아름다우면서도 체계적인 결과물을 만듭니다.'}, 
        'worstMatch': {'mbti': 'ENTJ', 'element': '우라늄', 'reason': '유연하고 현재를 즐기는 은의 성질이 목표 지향적이고 강력한 우라늄의 압박감을 견디기 힘듭니다.'}
    },
    'INFP': {
        'symbol': 'Ne', 'name': '네온 (Neon)', 'mbti': 'INFP',
        'description': '네온은 어둠 속에서 독특하고 아름다운 빛을 내는 비활성 기체입니다. INFP의 낭만적이고 이상적인 내면 세계는 네온이 뿜어내는 신비로운 빛과 닮았습니다. 네온이 독자적인 빛을 발하듯, 당신은 자신만의 가치관이 뚜렷하며 따뜻한 이상을 꿈꾸는 중재자입니다.',
        'properties': ['이상주의', '독창성', '낭만적', '순수함'],
        'atomicNumber': 10, 'atomicMass': '20.180 u', 'category': "비활성 기체", 'phase': '기체', 'discovery': '1898년',
        'imageUrl': 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=800&auto=format&fit=crop', 'usage': '네온 사인 및 고전압 표시기',
        'bestMatch': {'mbti': 'ENTJ', 'element': '우라늄', 'reason': '네온의 신비로운 빛이 우라늄의 거대한 에너지를 시각화하듯, 서로의 꿈을 현실로 이끄는 동반자가 됩니다.'}, 
        'worstMatch': {'mbti': 'ESTJ', 'element': '칼슘', 'reason': '자유로운 기체인 네온의 성질이 단단하고 규칙적인 칼슘의 틀 안에서 답답함을 느낄 수 있습니다.'}
    },
    'INTP': {
        'symbol': 'He', 'name': '헬륨 (Helium)', 'mbti': 'INTP',
        'description': '헬륨은 우주에서 두 번째로 흔하지만 매우 독립적이고 가벼운 원소입니다. INTP의 지적 호기심과 자유로운 사고방식은 헬륨의 가벼움과 비활성(독립성)에 비견됩니다. 헬륨이 높이 날아오르듯, 당신은 사물의 본질을 탐구하며 객관적인 분석을 즐기는 분석가입니다.',
        'properties': ['분석적', '객관성', '자유로움', '탐구심'],
        'atomicNumber': 2, 'atomicMass': '4.0026 u', 'category': '비활성 기체', 'phase': '기체', 'discovery': '1868년',
        'imageUrl': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?q=80&w=800&auto=format&fit=crop', 'usage': '풍선 충전재 및 MRI 냉각제',
        'bestMatch': {'mbti': 'ENFJ', 'element': '수소', 'reason': '헬륨과 수소가 별의 핵융합을 일으키듯, 두 유형의 지성과 열정이 만나 거대한 우주적 통찰을 만듭니다.'}, 
        'worstMatch': {'mbti': 'ESFJ', 'element': '알루미늄', 'reason': '독립적이고 가벼운 헬륨의 사고방식이 협동과 실용을 중시하는 알루미늄의 현실 세계와는 거리가 멉니다.'}
    },
    'ESTP': {
        'symbol': 'Na', 'name': '나트륨 (Sodium)', 'mbti': 'ESTP',
        'description': '나트륨은 반응성이 매우 강하고 에너지가 넘치는 원소입니다. ESTP의 활동적이고 모험적인 성향은 나트륨의 폭발적인 반응성과 닮았습니다. 나트륨이 즉각적으로 반응하듯, 당신은 순발력이 뛰어나며 행동으로 문제를 해결하는 활동가입니다.',
        'properties': ['활동성', '순발력', '자신감', '실행력'],
        'atomicNumber': 11, 'atomicMass': '22.990 u', 'category': '알칼리 금속', 'phase': '고체', 'discovery': '1807년',
        'imageUrl': 'https://images.unsplash.com/photo-1518110168401-f28bf39c4a44?q=80&w=800&auto=format&fit=crop', 'usage': '식탁용 소금 및 가로등',
        'bestMatch': {'mbti': 'ISFJ', 'element': '금', 'reason': '나트륨의 폭발적인 에너지를 금의 온화함이 안정적으로 잡아주어 가장 조화로운 관계를 형성합니다.'}, 
        'worstMatch': {'mbti': 'INFJ', 'element': '백금', 'reason': '나트륨의 즉각적인 반응성이 신중하고 깊은 백금의 템포를 당황하게 만들 수 있습니다.'}
    },
    'ESFP': {
        'symbol': 'Cu', 'name': '구리 (Copper)', 'mbti': 'ESFP',
        'description': '구리는 열과 전기를 가장 잘 전달하는 밝고 친근한 원소입니다. ESFP의 사교적이고 낙천적인 에너지는 구리의 높은 전도성과 닮았습니다. 구리가 에너지를 전달하듯, 당신은 주변 사람들을 즐겁게 만들고 열정을 공유하는 연예인입니다.',
        'properties': ['사교성', '낙천적', '친화력', '열정'],
        'atomicNumber': 29, 'atomicMass': '63.546 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://images.unsplash.com/photo-1558332854-f7e35ed41859?q=80&w=800&auto=format&fit=crop', 'usage': '전선, 배관, 동전 생산',
        'bestMatch': {'mbti': 'ISTJ', 'element': '철', 'reason': '구리의 밝은 에너지 전달력과 철의 견고한 지지력이 만나 실용적이면서도 즐거운 파트너십을 이룹니다.'}, 
        'worstMatch': {'mbti': 'INTJ', 'element': '탄소', 'reason': '사교적이고 외향적인 구리의 성질이 독립적이고 내향적인 탄소의 공간을 침해하는 것처럼 느껴질 수 있습니다.'}
    },
    'ENFP': {
        'symbol': 'O', 'name': '산소 (Oxygen)', 'mbti': 'ENFP',
        'description': '산소는 생명 유지에 필수적이며 어디에나 존재하는 활기찬 원소입니다. ENFP의 열정적이고 창의적인 성격은 산소가 생명을 지탱하는 활력과 닮았습니다. 산소가 모든 곳에 스며들듯, 당신은 사람들에게 긍정적인 에너지를 불어넣는 활동가입니다.',
        'properties': ['창의성', '열정', '긍정적', '자유분방'],
        'atomicNumber': 8, 'atomicMass': '15.999 u', 'category': '비금속', 'phase': '기체', 'discovery': '1774년',
        'imageUrl': 'https://images.unsplash.com/photo-1530026405186-ed1f139313f8?q=80&w=800&auto=format&fit=crop', 'usage': '의료용 산소 및 로켓 연료',
        'bestMatch': {'mbti': 'INFJ', 'element': '백금', 'reason': '산소가 백금 촉매를 통해 에너지를 발산하듯, 두 유형은 서로의 잠재력을 폭발시키는 최고의 조합입니다.'}, 
        'worstMatch': {'mbti': 'ISTJ', 'element': '철', 'reason': '산소가 철을 녹슬게 하듯, ENFP의 자유로움이 ISTJ의 엄격한 규칙을 무너뜨리는 갈등이 생길 수 있습니다.'}
    },
    'ENTP': {
        'symbol': 'P', 'name': '인 (Phosphorus)', 'mbti': 'ENTP',
        'description': '인은 빛을 내며 다양한 형태로 변신하는 변화무쌍한 원소입니다. ENTP의 두뇌 회전과 도전 정신은 인의 발광성과 동소체(변화)와 닮았습니다. 인이 어둠 속에서 빛나듯, 당신은 끊임없이 새로운 아이디어를 제시하며 논쟁을 즐기는 발명가입니다.',
        'properties': ['독창성', '도전정신', '다재다능', '변론가'],
        'atomicNumber': 15, 'atomicMass': '30.974 u', 'category': '비금속', 'phase': '고체', 'discovery': '1669년',
        'imageUrl': 'https://images.unsplash.com/photo-1536939459926-301728717817?q=80&w=800&auto=format&fit=crop', 'usage': '성냥, 비료, 세제 성분',
        'bestMatch': {'mbti': 'INTJ', 'element': '탄소', 'reason': '인의 번뜩이는 아이디어와 탄소의 전략적 논리가 만나 세상을 바꿀 혁신적인 설계를 완성합니다.'}, 
        'worstMatch': {'mbti': 'ISFJ', 'element': '금', 'reason': '끊임없이 연소하고 변화하는 인의 에너지가 변하지 않는 가치를 중시하는 금의 안정을 위협할 수 있습니다.'}
    },
    'ESTJ': {
        'symbol': 'Ca', 'name': '칼슘 (Calcium)', 'mbti': 'ESTJ',
        'description': '칼슘은 뼈를 구성하는 단단하고 필수적인 원소입니다. ESTJ의 질서 정연함과 추진력은 칼슘이 신체의 골격을 세우는 역할과 닮았습니다. 칼슘이 구조를 지탱하듯, 당신은 공동체의 규칙을 세우고 정직하게 이끄는 관리자입니다.',
        'properties': ['추진력', '질서', '정직함', '지도력'],
        'atomicNumber': 20, 'atomicMass': '40.078 u', 'category': '알칼리 토금속', 'phase': '고체', 'discovery': '1808년',
        'imageUrl': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?q=80&w=800&auto=format&fit=crop', 'usage': '뼈와 치아 형성, 시멘트 제조',
        'bestMatch': {'mbti': 'ISFP', 'element': '은', 'reason': '칼슘의 단단한 골조 위에 은의 아름다운 장식이 더해져 완벽하고 견고한 예술적 구조를 만듭니다.'}, 
        'worstMatch': {'mbti': 'INFP', 'element': '네온', 'reason': '현실적이고 단단한 칼슘의 규칙이 몽환적이고 자유로운 네온의 빛과는 서로를 이해하기 어렵게 만듭니다.'}
    },
    'ESFJ': {
        'symbol': 'Al', 'name': '알루미늄 (Aluminum)', 'mbti': 'ESFJ',
        'description': '알루미늄은 가볍고 유연하며 실생활에서 널리 쓰이는 친숙한 원소입니다. ESFJ의 협조적이고 다정한 성품은 알루미늄의 친숙함과 가공 용이성에 비견됩니다. 알루미늄이 일상 곳곳에서 도움을 주듯, 당신은 타인을 돕는 일에 기쁨을 느끼는 외교관입니다.',
        'properties': ['협동심', '다정함', '사교성', '봉사정신'],
        'atomicNumber': 13, 'atomicMass': '26.982 u', 'category': '후전이 금속', 'phase': '고체', 'discovery': '1825년',
        'imageUrl': 'https://images.unsplash.com/photo-1584013321683-f824c6ed195f?q=80&w=800&auto=format&fit=crop', 'usage': '음료 캔, 호일, 운송 수단',
        'bestMatch': {'mbti': 'ISTP', 'element': '티타늄', 'reason': '알루미늄의 친화력과 티타늄의 기술력이 만나 실생활에 가장 유용하고 강력한 합금을 만들어냅니다.'}, 
        'worstMatch': {'mbti': 'INTP', 'element': '헬륨', 'reason': '사람들과의 연결을 중시하는 알루미늄의 성질이 홀로 떠다니는 독립적인 헬륨의 성질을 이해하기 힘듭니다.'}
    },
    'ENFJ': {
        'symbol': 'H', 'name': '수소 (Hydrogen)', 'mbti': 'ENFJ',
        'description': '수소는 우주에서 가장 많으며 다른 원소들과 결합하여 별을 만드는 원소입니다. ENFJ의 이타주의와 영향력은 수소가 우주의 근간을 이루며 결합하는 성질과 닮았습니다. 수소가 별의 에너지가 되듯, 당신은 타인의 성장을 돕고 공감을 이끄는 카리스마 있는 지도자입니다.',
        'properties': ['이타주의', '영향력', '공감능력', '카리스마'],
        'atomicNumber': 1, 'atomicMass': '1.008 u', 'category': '비금속', 'phase': '기체', 'discovery': '1766년',
        'imageUrl': 'https://images.unsplash.com/photo-1614728263952-84ea256f9679?q=80&w=800&auto=format&fit=crop', 'usage': '청정 연료 및 로켓 추진제',
        'bestMatch': {'mbti': 'INTP', 'element': '헬륨', 'reason': '수소와 헬륨이 만나 태양의 빛을 내듯, 두 유형은 세상을 밝히는 거대한 지적, 감성적 에너지를 창출합니다.'}, 
        'worstMatch': {'mbti': 'ISTP', 'element': '티타늄', 'reason': '모두와 결합하려는 수소의 열정이 혼자만의 효율을 중시하는 티타늄의 냉철함에 상처받을 수 있습니다.'}
    },
    'ENTJ': {
        'symbol': 'U', 'name': '우라늄 (Uranium)', 'mbti': 'ENTJ',
        'description': '우라늄은 엄청난 에너지를 내포하고 있는 강력한 원소입니다. ENTJ의 야망과 결단력은 우라늄이 지닌 막대한 에너지 잠재력과 닮았습니다. 우라늄이 거대한 동력을 제공하듯, 당신은 목표를 향해 거침없이 나아가며 효율적으로 조직을 이끄는 통치자입니다.',
        'properties': ['결단력', '야망', '카리스마', '효율성'],
        'atomicNumber': 92, 'atomicMass': '238.029 u', 'category': '악티늄족', 'phase': '고체', 'discovery': '1789년',
        'imageUrl': 'https://images.unsplash.com/photo-1585913652332-602907607244?q=80&w=800&auto=format&fit=crop', 'usage': '원자력 발전 및 연대 측정',
        'bestMatch': {'mbti': 'INFP', 'element': '네온', 'reason': '우라늄의 강력한 추진력이 네온의 이상적인 빛을 현실로 구현하며 서로의 부족한 점을 완벽히 채웁니다.'}, 
        'worstMatch': {'mbti': 'ISFP', 'element': '은', 'reason': '우라늄의 거대한 에너지와 압박감이 유연하고 평화로운 은의 감수성을 위축시킬 우려가 있습니다.'}
    }
}

# 세션 상태 초기화
if 'state' not in st.session_state:
    st.session_state.state = 'START'
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

# 메인 로직
def main():
    if st.session_state.state == 'START':
        show_start()
    elif st.session_state.state == 'QUIZ':
        show_quiz()
    elif st.session_state.state == 'RESULT':
        show_result()

def show_start():
    st.title("🧪 Element MBTI Matcher")
    st.markdown("### 당신의 성격은 어떤 화학 원소와 닮았을까요?")
    st.write("20개의 질문을 통해 당신만의 원소를 찾아보세요.")
    if st.button("실험 시작하기", use_container_width=True):
        st.session_state.state = 'QUIZ'
        st.session_state.current_q = 0
        st.session_state.answers = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
        st.rerun()

def show_quiz():
    q_idx = st.session_state.current_q
    q = QUESTIONS[q_idx]
    
    st.progress((q_idx + 1) / len(QUESTIONS))
    st.write(f"**질문 {q_idx + 1} / {len(QUESTIONS)}**")
    st.markdown(f"### {q['text']}")
    
    for opt in q['options']:
        if st.button(opt['text'], key=f"opt_{q_idx}_{opt['value']}", use_container_width=True):
            st.session_state.answers[opt['value']] += 1
            if q_idx < len(QUESTIONS) - 1:
                st.session_state.current_q += 1
            else:
                st.session_state.state = 'RESULT'
            st.rerun()

def show_result():
    ans = st.session_state.answers
    mbti = (
        ('E' if ans['E'] >= ans['I'] else 'I') +
        ('S' if ans['S'] >= ans['N'] else 'S') + # Default to S if equal
        ('T' if ans['T'] >= ans['F'] else 'F') +
        ('J' if ans['J'] >= ans['P'] else 'P')
    )
    
    # Correcting the S/N logic if needed
    mbti = ""
    mbti += 'E' if ans['E'] >= ans['I'] else 'I'
    mbti += 'S' if ans['S'] >= ans['N'] else 'N'
    mbti += 'T' if ans['T'] >= ans['F'] else 'F'
    mbti += 'J' if ans['J'] >= ans['P'] else 'P'

    result = ELEMENT_RESULTS.get(mbti, ELEMENT_RESULTS['ISTJ'])
    
    st.balloons()
    st.title(f"결과: {result['name']}")
    st.subheader(f"당신의 MBTI 유형: {result['mbti']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f'<img src="{result["imageUrl"]}" style="width:100%; border-radius:10px; margin-bottom: 10px;" referrerpolicy="no-referrer">', unsafe_allow_html=True)
        st.caption(f"활용 사례: {result['usage']}")
        st.markdown(f"**원소 기호:** `{result['symbol']}`")
    
    with col2:
        st.write(result['description'])
        st.markdown("#### 주요 성질")
        for prop in result['properties']:
            st.info(prop)
            
    st.divider()
    st.markdown("#### 🤝 궁합 분석 (Compatibility)")
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        st.success(f"**최고의 궁합 (Best Match)**\n\n**원소:** {result['bestMatch']['element']}\n\n**MBTI:** {result['bestMatch']['mbti']}\n\n*{result['bestMatch']['reason']}*")
    with comp_col2:
        st.error(f"**최악의 궁합 (Worst Match)**\n\n**원소:** {result['worstMatch']['element']}\n\n**MBTI:** {result['worstMatch']['mbti']}\n\n*{result['worstMatch']['reason']}*")

    st.divider()
    st.markdown("#### 기술 사양 (Technical Specifications)")
    spec_col1, spec_col2 = st.columns(2)
    with spec_col1:
        st.write(f"**원자 번호:** {result['atomicNumber']}")
        st.write(f"**분류:** {result['category']}")
    with spec_col2:
        st.write(f"**원자량:** {result['atomicMass']}")
        st.write(f"**상태:** {result['phase']}")
    st.write(f"**발견:** {result['discovery']}")

    if st.button("다시 테스트하기", use_container_width=True):
        st.session_state.state = 'START'
        st.rerun()

if __name__ == "__main__":
    main()
