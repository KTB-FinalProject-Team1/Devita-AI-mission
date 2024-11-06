from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import json
import os

class LLMManager:
    _instance = None
    _model = None
    _tokenizer = None
    _device = None

    # 현재 디렉토리 구조에 맞게 경로 설정
    BASE_PATH = "/Users/do-yoon/work/devita/models/Llama-3-Open-Ko-8B"
    MODEL_PATH = os.path.join(BASE_PATH, "model")
    TOKENIZER_PATH = os.path.join(BASE_PATH, "tokenizer")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if LLMManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LLMManager._instance = self
            self._device = "mps" if torch.backends.mps.is_available() else "cpu"

    def load_model(self):
        """로컬 저장소에서 모델 로드"""
        if self._model is None:
            try:
                # 토크나이저 로드
                print(f"Loading tokenizer from: {self.TOKENIZER_PATH}")
                self._tokenizer = AutoTokenizer.from_pretrained(
                    self.TOKENIZER_PATH,
                    local_files_only=True,
                    trust_remote_code=True
                )
                print("Tokenizer loaded successfully!")

                # 모델 로드
                print(f"Loading model from: {self.MODEL_PATH}")
                self._model = AutoModelForCausalLM.from_pretrained(
                    self.MODEL_PATH,
                    local_files_only=True,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True
                )
                print("Model loaded successfully!")

            except Exception as e:
                print(f"Error loading model: {str(e)}")
                raise

    @property
    def model(self):
        if self._model is None:
            raise Exception("Model not loaded. Call load_model first.")
        return self._model

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            raise Exception("Tokenizer not loaded. Call load_model first.")
        return self._tokenizer

    def mission_generator_daily(self, main_category, sub_category):
        """미션 생성 함수"""
        instruction = self.generate_mission_prompt(main_category, sub_category)

        try:
            # 입력 텍스트 구성
            prompt = f"""
            System: {instruction['system']}

            Instruction: {instruction['instruction']}

            User: {instruction['user']}
            
            Assistant:
            """

            # 토크나이저로 입력 처리
            inputs = self._tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048
            ).to(self._device)

            # 생성 파라미터 설정
            generation_config = {
                "max_new_tokens": 1024,
                "do_sample": True,
                "temperature": 0.8,
                "top_p": 0.9,
                "num_return_sequences": 1,
                "pad_token_id": self._tokenizer.pad_token_id,
                "eos_token_id": self._tokenizer.eos_token_id,
            }

            # 텍스트 생성
            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    **generation_config
                )

            # 생성된 텍스트 디코딩
            generated_text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)

            # JSON 형식 추출 시도
            try:
                # JSON 부분만 추출
                json_start = generated_text.find('{')
                json_end = generated_text.rfind('}') + 1
                if json_start == -1 or json_end == 0:
                    raise json.JSONDecodeError("No JSON found", generated_text, 0)
                json_str = generated_text[json_start:json_end]

                # JSON 파싱
                output_dict = json.loads(json_str)

                return {
                    "mission_1": output_dict.get("mission_1", ""),
                    "mission_2": output_dict.get("mission_2", ""),
                    "mission_3": output_dict.get("mission_3", "")
                }

            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Generated text: {generated_text}")
                return {
                    "mission_1": "Error parsing JSON",
                    "mission_2": "Error parsing JSON",
                    "mission_3": "Error parsing JSON"
                }

        except Exception as e:
            print(f"Error in mission generation: {str(e)}")
            return None

    def generate_mission_prompt(self, main_category, sub_category):
        if main_category == "cs":
            if sub_category == "네트워크":
                example_text = """
                높은 난이도: TCP와 UDP의 차이점을 설명하고, TCP의 혼잡 제어 메커니즘(예: 슬라이딩 윈도우, 혼잡 회피)을 분석하라.
                중간 난이도: 라우팅 테이블의 동작 원리와 OSPF 프로토콜의 작동 방식을 설명하고, 기본적인 OSPF 설정 예시를 작성하라.
                쉬운 난이도: OSI 7계층 모델의 각 계층 역할을 간단히 설명하고, 해당 계층에서 사용하는 프로토콜(예: HTTP, TCP, IP)을 예시로 들어라.
                """
            elif sub_category == "알고리즘":
                example_text = """
                높은 난이도: 다익스트라 알고리즘을 사용한 최단 경로 탐색 원리를 분석하고, 우선순위 큐를 이용한 최적화 방안을 설명하라.
                중간 난이도: 퀵 정렬 알고리즘의 분할 정복 방식을 설명하고, 시간 복잡도를 분석하며, 퀵 정렬의 성능을 개선하는 방법을 제시하라.
                쉬운 난이도: 선택 정렬 알고리즘의 동작 과정을 설명하고, 시간 복잡도와 공간 복잡도를 계산하라.
                """
            else:
                example_text = """
                높은 난이도: 다익스트라 알고리즘을 사용한 최단 경로 탐색 원리를 분석하고, 우선순위 큐를 이용한 최적화 방안을 설명하라.
                중간 난이도: 퀵 정렬 알고리즘의 분할 정복 방식을 설명하고, 시간 복잡도를 분석하며, 퀵 정렬의 성능을 개선하는 방법을 제시하라.
                쉬운 난이도: 선택 정렬 알고리즘의 동작 과정을 설명하고, 시간 복잡도와 공간 복잡도를 계산하라.
                """
            prompt_description = "심화된 대학교 전공 수준의 개념 이해와 분석 능력을 테스트할 수 있는 미션"

        elif main_category == "language":
            if sub_category == "Java":
                example_text = """
                높은 난이도: 멀티스레드 환경에서의 동기화 필요성을 설명하고, synchronized 키워드를 사용해 데이터 레이스 문제를 해결하는 방법을 분석하라.
                중간 난이도: 자바 메모리 구조(스택과 힙)의 차이점을 설명하고, 가비지 컬렉션 방식 중 '마크-스윕'의 작동 원리를 이해할 수 있도록 예시를 제시하라.
                쉬운 난이도: 객체 지향 프로그래밍의 4가지 개념(캡슐화, 상속, 다형성, 추상화)을 각각 설명하라.
                """
            elif sub_category == "Python":
                example_text = """
                높은 난이도: 비동기 프로그래밍의 필요성과 개념을 설명하고, asyncio와 aiohttp를 사용해 비동기 웹 크롤러를 구현하라.
                중간 난이도: 데코레이터와 클로저의 차이점을 설명하고, 함수 실행 시간을 측정하는 로깅 기능을 데코레이터로 구현하라.
                쉬운 난이도: 리스트와 딕셔너리와 같은 기본 자료구조의 특징을 설명하라.
                """
            else:
                example_text = """
                높은 난이도: 비동기 프로그래밍의 필요성과 개념을 설명하고, asyncio와 aiohttp를 사용해 비동기 웹 크롤러를 구현하라.
                중간 난이도: 데코레이터와 클로저의 차이점을 설명하고, 함수 실행 시간을 측정하는 로깅 기능을 데코레이터로 구현하라.
                쉬운 난이도: 리스트와 딕셔너리와 같은 기본 자료구조의 특징을 설명하라.
                """
            prompt_description = "언어적 특성을 이해하고 사용하는 데 중점을 둔 미션"

        else:  # main_category == "tool"
            if sub_category == "Spring":
                example_text = """
                높은 난이도: Spring과 JPA를 사용하여 다중 테이블 간 연관 관계를 매핑하고, 복잡한 쿼리를 최적화하는 방법을 설명하라.
                중간 난이도: Spring MVC 패턴을 활용하여 간단한 CRUD 기능을 갖춘 게시판 애플리케이션을 설계하고 구현하라.
                쉬운 난이도: Spring Boot를 사용하여 간단한 REST API를 생성하고, 이를 통해 기본적인 GET/POST 요청을 처리하라.
                """
            elif sub_category == "Pytorch":
                example_text = """
                높은 난이도: PyTorch로 커스텀 신경망을 설계하고, 대규모 데이터셋을 활용하여 모델 학습 및 최적화 방법을 분석하라.
                중간 난이도: PyTorch에서 CNN을 사용해 이미지 분류 모델을 구현하고, 학습 및 평가 과정을 설명하라.
                쉬운 난이도: PyTorch에서 텐서 기본 연산과 자동 미분 기능을 사용하여 간단한 수학적 계산을 수행하라.
                """
            else:
                example_text = """
                높은 난이도: PyTorch로 커스텀 신경망을 설계하고, 대규모 데이터셋을 활용하여 모델 학습 및 최적화 방법을 분석하라.
                중간 난이도: PyTorch에서 CNN을 사용해 이미지 분류 모델을 구현하고, 학습 및 평가 과정을 설명하라.
                쉬운 난이도: PyTorch에서 텐서 기본 연산과 자동 미분 기능을 사용하여 간단한 수학적 계산을 수행하라.
                """
            prompt_description = "도구의 사용법과 주요 기능을 실습하는 미션"

        # 최종 프롬프트 생성
        prompt = {
            "system": f"""
            너는 개발자의 성장을 위한 일일 미션 생성기야.
            사용자가 관심 있는 개발 분야는 {main_category}의 {sub_category}야.

            [행동 지침]
            - 미션 제목만 출력하며, 미션 설명, 미션 목표 등 추가 내용은 포함하지 않아. '높은 난이도:', '중간 난이도:', '쉬운 난이도:'와 같은 난이도 표시를 포함하지 마.
            - 미션은 반드시 {main_category}, {sub_category}와 관련된 주제여야 하며, 그 외 내용은 포함하지 않아.
            - 예시는 단지 참고용일 뿐이야, 예시 내용에 너무 의존하거나 복사하지 마.
            - 개념을 확인하고 이해를 테스트할 수 있는 미션을 중심으로 생성해.
            - 미션 난이도는 높은 난이도, 중간 난이도, 쉬운 난이도 순으로 구분되며, 난이도 차이가 명확해야 해.
              * 쉬운 난이도의 미션은 개념을 알고 있는지 확인하는 수준보다 어려우면 안 돼.
              * 중간 난이도의 미션은 개념의 작동 원리를 알 수 있는 수준보다 어려우면 안 돼.
              * 높은 난이도의 미션은 개념의 응용을 할 수 있는 수준이어야 합니다.
            - 3가지의 각 미션은 다른 내용이어야 합니다.

            아래는 생성된 미션 예시야.
            ------------------------
            {example_text}
            ------------------------
            """,
            "user": f"""
            질문: {main_category} 안에 {sub_category}를 바탕으로 개발자를 위한 높은 난이도, 중간 난이도, 쉬운 난이도 {prompt_description}을 생성하시오.
            답:
            """,
            "instruction": """
            다음과 같은 JSON schema로 출력해야 합니다:
            {{
                "mission_1": "높은 난이도 미션(100자 이내)",
                "mission_2": "중간 난이도 미션(100자 이내)",
                "mission_3": "쉬운 난이도 미션(100자 이내)"
            }}
            """
        }

        return prompt

# 테스트 코드
# if __name__ == "__main__":
#     # LLM 매니저 인스턴스 생성
#     llm = LLMManager.get_instance()
#
#     # 모델 로드
#     llm.load_model()
#
#     # 미션 생성 테스트
#     result = llm.mission_generator_daily("cs", "알고리즘")
#     print(json.dumps(result, indent=2, ensure_ascii=False))