import querystar as qs
from llama_index import StorageContext, load_index_from_storage
import os, openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def ask_llamaindex(question: str):

    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    # load index
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)

    return response

# Slack trigger event
data = qs.triggers.slack.new_message(channel_id='C05PRRJ0H4N',  # channel: llama-qa
                                     trigger_string='ask llama') 
question = data.get('text', None)
answer = ask_llamaindex(question)
# send answer to Slack
qs.actions.slack.add_message(channel_id='C05PRRJ0H4N', message=f'Llama says: {answer}')