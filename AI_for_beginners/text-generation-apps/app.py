from openai import OpenAI

print("1. İstemci başlatılıyor...")
client = OpenAI(
    api_key = "local-no-key-needed",
    base_url = "http://localhost:11434/v1"
)

deployment_name = "phi3"

prompt = "Complete the following: Once upon a time there was a"

print("2. Yerel modele istek gönderiliyor")
response = client.responses.create(
    model = deployment_name,
    input = prompt,
    store = False
)

print(response.output_text)

