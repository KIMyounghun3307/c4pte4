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
        'description': '철은 구조물의 뼈대가 되는 가장 신뢰할 수 있는 원소입니다. 당신은 철처럼 책임감이 강하고 현실적이며, 조직의 중심을 든든하게 지탱하는 사람입니다.',
        'properties': ['견고함', '신뢰성', '실용주의', '체계적'],
        'atomicNumber': 26, 'atomicMass': '55.845 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://picsum.photos/seed/iron-steel/800/800', 'usage': '건축 구조물 및 강철 생산'
    },
    'ISFJ': {
        'symbol': 'Au', 'name': '금 (Gold)', 'mbti': 'ISFJ',
        'description': '금은 변하지 않는 가치와 따뜻한 빛을 지닌 원소입니다. 당신은 금처럼 주변 사람들을 소중히 여기고, 헌신적이며 안정적인 환경을 만드는 수호자입니다.',
        'properties': ['불변성', '헌신', '온화함', '세심함'],
        'atomicNumber': 79, 'atomicMass': '196.966 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://picsum.photos/seed/gold-jewelry/800/800', 'usage': '장신구 및 화폐 가치 저장'
    },
    'INFJ': {
        'symbol': 'Pt', 'name': '백금 (Platinum)', 'mbti': 'INFJ',
        'description': '백금은 희귀하며 강력한 촉매 역할을 하는 고귀한 원소입니다. 당신은 백금처럼 통찰력이 뛰어나고 이상적이며, 조용히 세상을 변화시키는 힘을 가지고 있습니다.',
        'properties': ['희귀성', '통찰력', '고결함', '신비로움'],
        'atomicNumber': 78, 'atomicMass': '195.084 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '1735년',
        'imageUrl': 'https://picsum.photos/seed/platinum-watch/800/800', 'usage': '자동차 촉매 장치 및 고급 정밀 기기'
    },
    'INTJ': {
        'symbol': 'C', 'name': '탄소 (Carbon)', 'mbti': 'INTJ',
        'description': '탄소는 생명의 근원이자 다이아몬드처럼 단단한 결합력을 가졌습니다. 당신은 탄소처럼 독립적이고 전략적이며, 자신만의 확고한 논리 체계를 구축하는 지략가입니다.',
        'properties': ['다재다능', '전략적', '독립성', '강인함'],
        'atomicNumber': 6, 'atomicMass': '12.011 u', 'category': '비금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://picsum.photos/seed/diamond-carbon/800/800', 'usage': '다이아몬드, 연필심, 탄소 섬유'
    },
    'ISTP': {
        'symbol': 'Ti', 'name': '티타늄 (Titanium)', 'mbti': 'ISTP',
        'description': '티타늄은 가볍지만 강철보다 강하며 실용적인 원소입니다. 당신은 티타늄처럼 상황 적응력이 뛰어나고 도구를 잘 다루며, 효율적인 해결책을 찾아내는 기술자입니다.',
        'properties': ['효율성', '적응력', '냉철함', '실무능력'],
        'atomicNumber': 22, 'atomicMass': '47.867 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '1791년',
        'imageUrl': 'https://picsum.photos/seed/titanium-jet/800/800', 'usage': '항공우주 부품 및 인공 관절'
    },
    'ISFP': {
        'symbol': 'Ag', 'name': '은 (Silver)', 'mbti': 'ISFP',
        'description': '은은 가장 높은 반사율을 가진 아름답고 유연한 원소입니다. 당신은 은처럼 감수성이 풍부하고 예술적이며, 현재의 순간을 아름답게 즐길 줄 아는 예술가입니다.',
        'properties': ['예술성', '유연함', '겸손함', '감수성'],
        'atomicNumber': 47, 'atomicMass': '107.868 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://picsum.photos/seed/silver-mirror/800/800', 'usage': '거울 코팅, 은식기, 전자 회로'
    },
    'INFP': {
        'symbol': 'Ne', 'name': '네온 (Neon)', 'mbti': 'INFP',
        'description': '네온은 어둠 속에서 독특하고 아름다운 빛을 내는 비활성 기체입니다. 당신은 네온처럼 자신만의 세계가 뚜렷하고 낭만적이며, 따뜻한 이상을 꿈꾸는 중재자입니다.',
        'properties': ['이상주의', '독창성', '낭만적', '순수함'],
        'atomicNumber': 10, 'atomicMass': '20.180 u', 'category': '비활성 기체', 'phase': '기체', 'discovery': '1898년',
        'imageUrl': 'https://picsum.photos/seed/neon-sign/800/800', 'usage': '네온 사인 및 고전압 표시기'
    },
    'INTP': {
        'symbol': 'He', 'name': '헬륨 (Helium)', 'mbti': 'INTP',
        'description': '헬륨은 우주에서 두 번째로 흔하지만 매우 독립적이고 가벼운 원소입니다. 당신은 헬륨처럼 지적 호기심이 많고 자유로우며, 사물의 본질을 탐구하는 분석가입니다.',
        'properties': ['분석적', '객관성', '자유로움', '탐구심'],
        'atomicNumber': 2, 'atomicMass': '4.0026 u', 'category': '비활성 기체', 'phase': '기체', 'discovery': '1868년',
        'imageUrl': 'https://picsum.photos/seed/helium-balloon/800/800', 'usage': '풍선 충전재 및 MRI 냉각제'
    },
    'ESTP': {
        'symbol': 'Na', 'name': '나트륨 (Sodium)', 'mbti': 'ESTP',
        'description': '나트륨은 반응성이 매우 강하고 에너지가 넘치는 원소입니다. 당신은 나트륨처럼 활동적이고 모험을 즐기며, 즉각적인 행동으로 문제를 해결하는 활동가입니다.',
        'properties': ['활동성', '순발력', '자신감', '실행력'],
        'atomicNumber': 11, 'atomicMass': '22.990 u', 'category': '알칼리 금속', 'phase': '고체', 'discovery': '1807년',
        'imageUrl': 'https://picsum.photos/seed/salt-sodium/800/800', 'usage': '식탁용 소금 및 가로등'
    },
    'ESFP': {
        'symbol': 'Cu', 'name': '구리 (Copper)', 'mbti': 'ESFP',
        'description': '구리는 열과 전기를 가장 잘 전달하는 밝고 친근한 원소입니다. 당신은 구리처럼 사교적이고 에너지를 잘 전달하며, 주변 사람들을 즐겁게 만드는 연예인입니다.',
        'properties': ['사교성', '낙천적', '친화력', '열정'],
        'atomicNumber': 29, 'atomicMass': '63.546 u', 'category': '전이 금속', 'phase': '고체', 'discovery': '고대',
        'imageUrl': 'https://picsum.photos/seed/copper-wire/800/800', 'usage': '전선, 배관, 동전 생산'
    },
    'ENFP': {
        'symbol': 'O', 'name': '산소 (Oxygen)', 'mbti': 'ENFP',
        'description': '산소는 생명 유지에 필수적이며 어디에나 존재하는 활기찬 원소입니다. 당신은 산소처럼 열정적이고 창의적이며, 사람들에게 긍정적인 에너지를 불어넣는 활동가입니다.',
        'properties': ['창의성', '열정', '긍정적', '자유분방'],
        'atomicNumber': 8, 'atomicMass': '15.999 u', 'category': '비금속', 'phase': '기체', 'discovery': '1774년',
        'imageUrl': 'https://picsum.photos/seed/oxygen-mask/800/800', 'usage': '의료용 산소 및 로켓 연료'
    },
    'ENTP': {
        'symbol': 'P', 'name': '인 (Phosphorus)', 'mbti': 'ENTP',
        'description': '인은 빛을 내며 다양한 형태로 변신하는 변화무쌍한 원소입니다. 당신은 인처럼 두뇌 회전이 빠르고 도전적이며, 끊임없이 새로운 아이디어를 제시하는 발명가입니다.',
        'properties': ['독창성', '도전정신', '다재다능', '변론가'],
        'atomicNumber': 15, 'atomicMass': '30.974 u', 'category': '비금속', 'phase': '고체', 'discovery': '1669년',
        'imageUrl': 'https://picsum.photos/seed/matchstick-fire/800/800', 'usage': '성냥, 비료, 세제 성분'
    },
    'ESTJ': {
        'symbol': 'Ca', 'name': '칼슘 (Calcium)', 'mbti': 'ESTJ',
        'description': '칼슘은 뼈를 구성하는 단단하고 필수적인 원소입니다. 당신은 칼슘처럼 질서를 중시하고 추진력이 강하며, 공동체의 규칙을 세우고 이끄는 관리자입니다.',
        'properties': ['추진력', '질서', '정직함', '지도력'],
        'atomicNumber': 20, 'atomicMass': '40.078 u', 'category': '알칼리 토금속', 'phase': '고체', 'discovery': '1808년',
        'imageUrl': 'https://picsum.photos/seed/milk-calcium/800/800', 'usage': '뼈와 치아 형성, 시멘트 제조'
    },
    'ESFJ': {
        'symbol': 'Al', 'name': '알루미늄 (Aluminum)', 'mbti': 'ESFJ',
        'description': '알루미늄은 가볍고 유연하며 실생활에서 널리 쓰이는 친숙한 원소입니다. 당신은 알루미늄처럼 협조적이고 다정하며, 타인을 돕는 일에 기쁨을 느끼는 외교관입니다.',
        'properties': ['협동심', '다정함', '사교성', '봉사정신'],
        'atomicNumber': 13, 'atomicMass': '26.982 u', 'category': '후전이 금속', 'phase': '고체', 'discovery': '1825년',
        'imageUrl': 'https://picsum.photos/seed/aluminum-can/800/800', 'usage': '음료 캔, 호일, 운송 수단'
    },
    'ENFJ': {
        'symbol': 'H', 'name': '수소 (Hydrogen)', 'mbti': 'ENFJ',
        'description': '수소는 우주에서 가장 많으며 다른 원소들과 결합하여 별을 만드는 원소입니다. 당신은 수소처럼 타인의 성장을 돕고 이타적이며, 강한 영향력을 미치는 지도자입니다.',
        'properties': ['이타주의', '영향력', '공감능력', '카리스마'],
        'atomicNumber': 1, 'atomicMass': '1.008 u', 'category': '비금속', 'phase': '기체', 'discovery': '1766년',
        'imageUrl': 'https://picsum.photos/seed/hydrogen-rocket/800/800', 'usage': '청정 연료 및 로켓 추진제'
    },
    'ENTJ': {
        'symbol': 'U', 'name': '우라늄 (Uranium)', 'mbti': 'ENTJ',
        'description': '우라늄은 엄청난 에너지를 내포하고 있는 강력한 원소입니다. 당신은 우라늄처럼 야망이 크고 결단력이 있으며, 목표를 향해 거침없이 나아가는 통치자입니다.',
        'properties': ['결단력', '야망', '카리스마', '효율성'],
        'atomicNumber': 92, 'atomicMass': '238.029 u', 'category': '악티늄족', 'phase': '고체', 'discovery': '1789년',
        'imageUrl': 'https://picsum.photos/seed/nuclear-power/800/800', 'usage': '원자력 발전 및 연대 측정'
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
    st.write("12개의 질문을 통해 당신만의 원소를 찾아보세요.")
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
        st.image(result['imageUrl'], caption=f"활용 사례: {result['usage']}", use_container_width=True)
        st.markdown(f"**원소 기호:** `{result['symbol']}`")
    
    with col2:
        st.write(result['description'])
        st.markdown("#### 주요 성질")
        for prop in result['properties']:
            st.info(prop)

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
