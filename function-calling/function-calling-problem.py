import os
import json
from openai import OpenAI

# 1. İstemciyi başlatıyoruz
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  
)

deployment = "phi3"

student_1_description = "Emily Johnson is a sophomore majoring in computer science at Duke University. She has a 3.7 GPA. Emily is an active member of the university's Chess Club and Debate Team. She hopes to pursue a career in software engineering after graduating."
student_2_description = "Michael Lee is a sophomore majoring in computer science at Stanford University. He has a 3.8 GPA. Michael is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after finishing his studies."

# Modele anahtarları (keys) şablon olarak vermek işini kolaylaştırır
prompt1 = f'''
Please extract the following information from the given text and return it strictly as a raw JSON object:
{{
  "name": "",
  "major": "",
  "school": "",
  "grades": "",
  "club": ""
}}

This is the body of text to extract the information from:
{student_1_description}
'''

prompt2 = f'''
Please extract the following information from the given text and return it strictly as a raw JSON object:
{{
  "name": "",
  "major": "",
  "school": "",
  "grades": "",
  "club": ""
}}

This is the body of text to extract the information from:
{student_2_description}
'''

# 2. Doğru fonksiyonu (chat.completions.create) çağırıyoruz
# response_format ekleyerek modelin dışına taşmasını engelliyoruz
openai_response1 = client.chat.completions.create(
    model=deployment,
    messages=[{'role': 'user', 'content': prompt1}],
    response_format={"type": "json_object"}
)

openai_response2 = client.chat.completions.create(
    model=deployment,
    messages=[{'role': 'user', 'content': prompt2}],
    response_format={"type": "json_object"}
)

# 3. Yanıt metnini doğru özellikten (.choices[0].message.content) alıyoruz
raw_text1 = openai_response1.choices[0].message.content
raw_text2 = openai_response2.choices[0].message.content

# 4. JSON olarak güvenle yüklüyoruz
json_response1 = json.loads(raw_text1)
print(json.dumps(json_response1, indent=2))

json_response2 = json.loads(raw_text2)
print(json.dumps(json_response2, indent=2))