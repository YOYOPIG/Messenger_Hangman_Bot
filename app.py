#Python libraries that we need to import for our bot
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
#game.game_start()

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
       # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                #send msg
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
                #if user sends us a GIF, photo,video, or any other non-text item, reply yee
                if message['message'].get('attachments'):
                    response_sent_photo = "https://i.imgur.com/dTki2aL.jpg"
                    send_image(recipient_id, response_sent_photo)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

def send_image(recipient_id, image_url):
    #sends user the image message provided via input url
    bot.send_image_url(recipient_id, image_url)
    return "success"

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()