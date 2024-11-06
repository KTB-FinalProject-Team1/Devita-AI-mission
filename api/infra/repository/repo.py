from api.domain.repository.repo import IRepository
from model.llm import LLMManager
from api.interface.controllers.model.model import Field
import json


class Repository(IRepository):
    def daily(
            self,
            user_id: str,
            field: list[Field]
    # ) -> list[str]:
    ) -> str:
        res = LLMManager.get_instance().mission_generator_daily(field[0].main_category, field[0].sub_category)
        print(str(res))
        return str(res)
#         return ["""
# 자바에서 new와 this 키워드는 각각 어떤 역할을 하는지 설명하라. new 키워드를 사용해 객체를 생성하는 과정과, this 키워드가 메서드와 생성자에서 어떻게 쓰이는지 구체적인 예를 들어 설명하라.
# """,
#                 """
# 자바에서 상속(Inheritance)과 다형성(Polymorphism)의 차이를 설명하고, 이 두 개념이 객체 지향 프로그래밍에서 어떻게 유용하게 쓰이는지 실제 사례를 들어 설명하라. 특히 다형성이 어떻게 코드 재사용성을 높이는지 중점적으로 논의하라.
# """,
#                 """
# 자바에서 멀티스레드 프로그래밍의 기본 개념을 설명하고, 멀티스레드 환경에서 발생할 수 있는 문제(예: 데드락, 레이스 컨디션)에 대해 설명하라. 또한, 자바 버전의 설계적 결함을 조사하고, 해당 결함이 프로그램에 미치는 영향을 분석하라.
# """]

    def autonomous(
            self,
            user_id: str,
            field: list[Field]
    ) -> list[str]:
        pass
#         return ["""
# 자바에서 new와 this 키워드는 각각 어떤 역할을 하는지 설명하라. new 키워드를 사용해 객체를 생성하는 과정과, this 키워드가 메서드와 생성자에서 어떻게 쓰이는지 구체적인 예를 들어 설명하라.
# """,
#                 """
# 자바에서 상속(Inheritance)과 다형성(Polymorphism)의 차이를 설명하고, 이 두 개념이 객체 지향 프로그래밍에서 어떻게 유용하게 쓰이는지 실제 사례를 들어 설명하라. 특히 다형성이 어떻게 코드 재사용성을 높이는지 중점적으로 논의하라.
# """,
#                 """
# 자바에서 멀티스레드 프로그래밍의 기본 개념을 설명하고, 멀티스레드 환경에서 발생할 수 있는 문제(예: 데드락, 레이스 컨디션)에 대해 설명하라. 또한, 자바 버전의 설계적 결함을 조사하고, 해당 결함이 프로그램에 미치는 영향을 분석하라.
# """,
#                 """
# 자바에서 new와 this 키워드는 각각 어떤 역할을 하는지 설명하라. new 키워드를 사용해 객체를 생성하는 과정과, this 키워드가 메서드와 생성자에서 어떻게 쓰이는지 구체적인 예를 들어 설명하라.
# """,
#                 """
# 자바에서 상속(Inheritance)과 다형성(Polymorphism)의 차이를 설명하고, 이 두 개념이 객체 지향 프로그래밍에서 어떻게 유용하게 쓰이는지 실제 사례를 들어 설명하라. 특히 다형성이 어떻게 코드 재사용성을 높이는지 중점적으로 논의하라.
# """
#         ]
