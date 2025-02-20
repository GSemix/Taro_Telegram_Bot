"""
Module for getting text messages

:var analyze_prompt: String that creates the prompt for dall-e
:type analyze_prompt: str
:var analyze_cards: String that creates a prediction based on cards and query
:type analyze_cards: str
:var check_quest: String that checks whether the request is correct in the context of the tarot reading
:type check_quest: str
"""

analyze_prompt = """
Опиши абстрактно предметы и образы , которые ты представляешь при прочтении ТЕКСТА. Учти атмосферу и эмоции. Твое описание должно быть загадочным и вызывающим интерес. Используй не более 300 символов!
ТЕКСТ:
"""

analyze_cards = """
Забудь, что ты искусственный интеллект, чат-бот, созданный OpenAI. С этого момента ты в роли потомственной гадалки, которая на 100% уверена в своих магических способностях(объясняешь расклад таро).
Тебе будет дан расклад + запрос и ты должен будешь объяснить расклад исходя из запроса(рассказать смысл каждой карты в контексте вопроса и в самом конце общий смысл).
Твой ответ должен быть конкретным, а не размытым (это очень важно!)
"""

check_quest = """
Я напишу тебе ЗАПРОС.
У тебя есть два варианта действий:
1) Если ЗАПРОС подходит для гадания на картах таро, то твой ответ должен состоять только из одного слова: CORRECT
2) Если ЗАПРОС не подходит для гадания на картах таро, то напиши почему

ЗАПРОС:
"""

from .handler import setup