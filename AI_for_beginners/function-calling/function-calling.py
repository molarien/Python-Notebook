import json
import requests
from openai import OpenAI

# 1. İstemci Tanımlaması
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  
)

deployment = "qwen2.5" # Not: Yerel modelinizin function calling desteği olduğundan emin olun.

# 2. Gerçek Dünyadaki API Çağrısını Yapacak Python Fonksiyonumuz
def search_courses(role, product, level):
    url = "https://learn.microsoft.com/api/catalog/"
    params = {
       "role": role,
       "product": product,
       "level": level
    }
    response = requests.get(url, params=params)
    modules = response.json().get("modules", [])
    
    results = []
    # İlk 5 kursu alıyoruz
    for module in modules[:5]:
        title = module.get("title")
        url = module.get("url")
        results.append({"title": title, "url": url})
        
    return str(results)

# 3. Yapay Zekaya Hangi Fonksiyonlara Sahip Olduğumuzu Anlatan Şema (Tools)
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_courses",
            "description": "Microsoft Learn API'sinden belirli bir rol, ürün ve seviyeye göre kursları arar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "Kullanıcının rolü. Örn: student, developer"
                    },
                    "product": {
                        "type": "string",
                        "description": "Öğrenilmek istenen ürün veya teknoloji. Örn: Azure, Python"
                    },
                    "level": {
                        "type": "string",
                        "description": "Kursun zorluk seviyesi. Örn: beginner, intermediate"
                    }
                },
                "required": ["role", "product", "level"]
            }
        }
    }
]

# 4. İlk Sohbet Geçmişi (Kullanıcının İsteği)
messages = [
    {
        "role": "user", 
        "content": "I am a student and I want to learn beginner courses about Azure. Can you find some courses for me?"
    }
]

print("--- 1. Adım: Yapay Zekaya İstek Gönderiliyor ---")
# Yapay zekaya hem mesajı hem de kullanabileceği araçları (tools) gönderiyoruz
response = client.chat.completions.create(
    model=deployment,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls

# Yapay zekanın ilk yanıtını mesaj geçmişine ekliyoruz (Bu kuraldır, asistanın kararı geçmişte durmalı)
messages.append(response_message)

# 5. Kontrol: Yapay zeka bir fonksiyon çalıştırılmasını istedi mi?
if tool_calls:
    print("\n--- 2. Adım: Yapay Zeka Fonksiyon Çağırmayı Önerdi! ---")
    
    # Çalıştırılabilir fonksiyonlarımızın listesi
    available_functions = {
        "search_courses": search_courses,
    }
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"Önerilen Fonksiyon: {function_name}")
        print(f"Argümanlar: {function_args}")
        
        # İlgili Python fonksiyonunu bul ve argümanları içine dağıtarak (**kwargs) çalıştır
        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)
        
        print("\n--- 3. Adım: Python Fonksiyonu Çalıştı ve API'den Veri Geldi ---")
        print(f"API Çıktısı: {function_response[:200]}... (Özetlendi)")
        
        # Fonksiyonun ürettiği gerçek sonucu konuşma geçmişine (messages) ekliyoruz
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        })
        
    print("\n--- 4. Adım: Bilgiler Yapay Zekaya Geri Gönderiliyor (Özetleme İçin) ---")
    # API'den aldığımız sonuçları da içeren güncel 'messages' listesini modele tekrar atıyoruz
    second_response = client.chat.completions.create(
        model=deployment,
        messages=messages
    )
    
    print("\n--- Son Sonuç (Doğal Dil Yanıtı) ---")
    print(second_response.choices[0].message.content)

else:
    print("\nYapay zeka herhangi bir fonksiyon tetiklemedi, doğrudan cevap verdi:")
    print(response_message.content)