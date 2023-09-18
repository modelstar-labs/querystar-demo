import querystar as qs
import openai
import json
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_product(message: str) -> dict:
    prompt = [
        {
            "role": "system",
            "content": ("You're a technologist. "
                        "Your goal is to find what technical products are discussed "
                        "in the user message, and what their category is. "
                        "Output a dict: \n"
                        "{\"product\": [\"product1\", \"product2\"],"
                        "  \"category\": \"product category\"}\n\n"
                        "If no product can be found, return an empty dict: {}")
        },
        {
            "role": "user",
            "content": message
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0,
        max_tokens=500)
    try:
        product = json.loads(response.choices[0].message['content'])
        product['valid GPT answer'] = True
    except:
        product = {'valid GPT answer': False}
    
    return product


message = qs.triggers.slack.new_message(channel_id='C05S0STJ1E1')   # add your own slack channel id

product = extract_product(message['text'])

qs.actions.google_sheets.add_row(
    spreadsheet_id='1nCRGIMe10zmBpP2wQUHMFRvyuHfvoRTBJjw1CKVdDck', # add your own Google Sheet id
    worksheet_id='Sheet1',   # add your own Worksheet id
    data=[[message['user'], message['text'], product['valid GPT answer'], 
           repr(product['product']), product['category'] ]]
    )

