from flask import Flask, request
import requests
from rivescript import RiveScript

bot = RiveScript()
bot.load_directory("./eg/brain")
bot.sort_replies()

app = Flask(__name__)

ACCESS_TOKEN = "EAAXZBh5wBB74BACCysn5riSQsjmPt1igZCZCopKWzTW0InXultylLBnbvozZBwpOIu75JMGk62sZAgvyjtp2KHYJ5ezZCrWovgdGdP4zaTcigJEORYJiR0JYlSdefXgCrN2lcsS6BFMx70WlyOShS6aC6YP345nFtpbRgRkeMY5gZDZD" 

def verify_hash (user_id,userinput):
	try:
		score = int(userinput)
		message = "You have earned " + userinput + " points today!"
	except (ValueError):
		message = "Please Type in a Valid Key"	
	reply_user(user_id,message)

def reply_user(user_id,msg):
	data = {
	      "recipient": {"id": user_id},
	      "message": {"text": msg}
					    }
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print(resp.content)

@app.route('/', methods=['GET'])
def handle_verification():
	return request.args['hub.challenge']

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    print message
    reply = bot.reply("localuser", message)
    print reply
    reply_user(sender, reply)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
