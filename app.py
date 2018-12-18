import random
import os
from flask import Flask, request
from pymessenger.bot import Bot
from hangman import Hangman

app = Flask(__name__)
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
VERIFY_TOKEN = 'TooTiredToYEE'
bot = Bot(ACCESS_TOKEN)

game = Hangman("hangman")

# Handle received messages that Facebook sends our bot here 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Deal with the verify token when the program receive a GET request from facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # Handle user's message and reply to them when we get a POST request
    else:
       # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                # Facebook Messenger ID of user to reply to
                recipient_id = message['sender']['id']
                # Read msg and reply
                if message['message'].get('text') == "start":
                    ret_msg = game.game_start()
                    send_message(recipient_id, ret_msg)
                elif message['message'].get('text'):
                    # User is playing
                    if game.get_game_done():
                        send_message(recipient_id, "Hi there! Type start to start playing!")
                    else:
                        ret_msg = game.input_word(message['message'].get('text'))
                        send_message(recipient_id, ret_msg)
                        ret_msg = game.check_game_status()
                        ret_img = game.get_hangman_photo_url()
                        send_image(recipient_id, ret_img)
                        send_message(recipient_id, ret_msg)
                # If user sends a non-text item such as photos or videos, reply yee
                if message['message'].get('attachments'):
                    response_sent_photo = "https://i.imgur.com/dTki2aL.jpg"
                    send_image(recipient_id, response_sent_photo)
    return "Message Processed"


def verify_fb_token(token_sent):
    """Verify the token sent by facebook which should match the verify token you sent
    allow the request only when they match, else return an error"""
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# Use PyMessenger to send response to user
def send_image(recipient_id, image_url):
    # Send user the image thru image_url
    bot.send_image_url(recipient_id, image_url)
    return "success"

def send_message(recipient_id, response):
    # Send user the text response
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()