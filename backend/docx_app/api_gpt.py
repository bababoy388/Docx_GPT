import json
import requests


token = "TOKEN"

def apigpt(question):
    url = "https://models.github.ai/inference/chat/completions"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "system", "content": """Ты должен вернуть ТОЛЬКО JSON без каких-либо объяснений, комментариев или дополнительного текста.
    Пользователь передаст тебе шаблон с ключами в формате '${КЛЮЧ}'. 
    Создай JSON где ключом будет сам ключ из шаблона а значением - заполнение для этого ключа.
    Пример ответа: {"ИМЯ": "Иван Иванов", "ДАТА": "2024-01-15", "НОМЕР": "12345"}"""},
            {"role": "user", "content": question}
        ],
        "response_format": {"type": "json_object"}
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']

            try:
                json_response = json.loads(content)
                return json_response
            except json.JSONDecodeError:
                return content
        else:
            return f"Ошибка: Неожиданная структура ответа: {result}"

    except Exception as e:
        return f"Ошибка: {str(e)}. Ответ сервера: {response.text}"
