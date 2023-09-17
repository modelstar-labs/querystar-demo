import querystar as qs
import openai
import json

openai.api_key = 'sk-***' #add your own openai api key

def extract_product(message: str) -> dict:
    prompt = [
        {
            "role": "system",
            "content": ("You're a technologist. "
                        "Your goal is to find what technical products are discussed "
                        "in the user message, and what their category is. "
                        "Output a dict: \n"
                        "{\"product\": [\"product1\", \"product2\"],"
                        "  \"category\": \"cloud service\"}\n\n"
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


message = qs.triggers.slack.new_message(
    channel_id='C***',                  # add your own slack channel id
    trigger_for_bot_messages=False
    )

product = extract_product(message['text'])

qs.actions.google_sheets.add_row(
    spreadsheet_id='1nCRGIMe10zmBpP2wQUHMFRvyuHfvoRTBJjw1CKVdDck',
    worksheet_id='Sheet2',
    data=[[message['user'], message['text'], product['valid GPT answer'], 
           repr(product['product']), product['category'] ]]
    )

