import querystar as qs

# Triggered by new messages sent to channel #introduction
qs.triggers.slack.new_message(channel_id='C05Q36Z6GGM',
                              trigger_for_bot_messages=True)

qs.actions.slack.add_message(channel_id='C05Q36Z6GGM', 
                             message='Hello!')