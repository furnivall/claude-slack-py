import anthropic
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

HUMAN_PROMPT = '\n\nHuman:'

AI_PROMPT = '\n\nAssistant:'
c = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    # signing_secret=os.environ.get("SLACK_SIGNING_SECRET") # not required for socket mode
)


def respond(user_message):
    resp = c.completion(
        prompt=f"{HUMAN_PROMPT} {user_message} {AI_PROMPT}",
        stop_sequences=[HUMAN_PROMPT],
        model="claude-v1",
        max_tokens_to_sample=10000,
    )
    return resp


# Listens to incoming messages
@app.event("message")
def handle_message_events(event, say):
    msg = respond(event.text)
    print(msg)
    say(msg.get('completion'))


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
