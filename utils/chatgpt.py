import tiktoken
from async_openai import OpenAI, settings, CompletionResponse
from async_openai.types import CompletionModels

from config import OPENAI_TOKEN

desc_style = [{}, {"name": "Сторителлинг", "prompt": "сторителлинг", "is_separate": False},
              {"name": "Убедительный", "prompt": "убедительный", "is_separate": False},
              {"name": "Информационный", "prompt": "информационный", "is_separate": False},
              {"name": "Сравнительный", "prompt": "сравнительный", "is_separate": False},
              {"name": "Проблемно-ориентированный", "prompt": "проблемно-ориентированный", "is_separate": True},
              {"name": "Убедительный", "prompt": "убедительный", "is_separate": False}]

brand_lang = [{}, {"name": "На латинице", "prompt": "на латинице"},
              {"name": "На кириллице", "prompt": "на кириллице"}]

brand_characters = [{}, {"name": "4-8 символов", "prompt": "4-8 символов"},
                    {"name": "6-12 символов", "prompt": "6-12 символов"}]

brand_words_count = [{}, {"name": "1 слово", "prompt": "одного слова"},
                     {"name": "2 слова", "prompt": "двух слов"}]

OpenAI.configure(
    api_key=OPENAI_TOKEN,
    debug_enabled=False,
)


async def get_ans(prompt):
    encoding = tiktoken.encoding_for_model("text-davinci-003")
    prompt_tokens = len(encoding.encode(prompt))
    max_tokens = 4000 - prompt_tokens
    response: CompletionResponse = await OpenAI.completions.async_create(
        prompt=prompt,
        max_tokens=max_tokens,
        model=CompletionModels.davinci
    )
    return response.text[response.text.find("\n\n")+2:]
