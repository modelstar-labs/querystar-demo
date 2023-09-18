import querystar as qs
import os, requests, json

s = requests.Session()

ANYSCALE_TOKEN = os.getenv('ANYSCALE_TOKEN')       # add your own Anyscale token
url = "https://api.endpoints.anyscale.com/v1/chat/completions"

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
    body = {
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": prompt,
        "temperature": 0
        }

    with s.post(url, 
                headers={"Authorization": f"Bearer {ANYSCALE_TOKEN}"}, 
                json=body) as resp:
        response = resp.json()

    try:
        product = json.loads(response['choices'][0]['message']['content'])
        product['valid LLM answer'] = True
    except:
        product = {'valid LLM answer': False}
    
    return product


message = qs.triggers.slack.new_message(channel_id='C05S0STJ1E1')   # add your own slack channel id

product = extract_product(message['text'])

qs.actions.google_sheets.add_row(
    spreadsheet_id='1nCRGIMe10zmBpP2wQUHMFRvyuHfvoRTBJjw1CKVdDck', # add your own Google Sheet id
    worksheet_id='Sheet1',   # add your own Worksheet id
    data=[[message['user'], message['text'], product['valid GPT answer'], 
           repr(product['product']), product['category'] ]]
    )
