import requests


GITHUB_TOKEN = "Token"
url = "https://models.github.ai/inference/chat/completions"


def apigpt(document):
    headers = {
        "Authorization": GITHUB_TOKEN}
    data = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "Кратко расскажи что за информация в этом документе"
            },
            {
                "role": "user",
                "content": document
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    # Проверяем наличие ключей перед обращением
    if 'choices' in response_data and response_data['choices']:
        gpt_response = response_data['choices'][0]['message']['content']
        return gpt_response
    else:
        print("Ответ API:", response_data)
        return "Ошибка ответа"
