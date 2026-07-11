from openai import OpenAI

client = OpenAI(
    api_key="ollama-no-key-needed",
    base_url="http://localhost:11434/v1",
)

deployment_name = "phi3"
prompt = "Show me 5 recipes for a dish with the following ingredients: chicken, potatoes, and carrots. Per recipe, list all the ingredients used"


response = client.chat.completions.create(
    model=deployment_name,
    messages=[{"role": "user", "content": prompt}],
    stream=True
)


for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()


"""

chunk                         --> Gelen kargo kutusu
  └── .choices[0]             --> Kutunun içindeki 1. alternatif paket
        └── .delta            --> O paketin içindeki "yeni eklenen" kısım
              └── .content    --> O kısmın içindeki asıl KARAKTER / KELİME ("Tavuk", "Merhaba" vb.)



"""