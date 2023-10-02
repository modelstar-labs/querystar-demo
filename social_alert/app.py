import querystar as qs
import openai
from datetime import date

openai.api_key = "sk-xxx"   # add your own key

def analyze_sentiment(input_text):
    prompt = [
        {
            "role": "system",
            "content": ("You're a brand expert, and will be given a speaker note. "
                        "Analyze if the speaker really likes SpaceX's brand. "
                        "Brand includes SpaceX's founders, employees, products or business.\n"
                        "Output positive if the speaker supports the brand. "
                        "Output negative if the speaker clearly dislike SpaceX brand. "
                        "Otherwise, output neutral.\n"
                        "Note: if a speaker argues with others, without showing position "
                        "about liking SpaceX or not, then it's neutral.\n"
                        "Only output positive, negative, neutral. "
                        )
        },
        {
            "role": "user",
            "content": input_text
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0,
        max_tokens=500)
    return response.choices[0].message['content']


post = qs.triggers.reddit.new_message("spacex")

sentiment = analyze_sentiment(post['text'])
today = date.today()
date_str = today.strftime("%Y-%m-%d")

qs.actions.slack.add_message(
    channel_id="...", # add your channel id
    message=f"{sentiment} post alert: {post['permalink']}")

qs.actions.google_sheets.add_row(
    spreadsheet_id='add your spreadsheet_id here',
    worksheet_id='Sheet1',
    data=[[post['text'], date_str, sentiment]])