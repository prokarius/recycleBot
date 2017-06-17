from flask import Flask, request
import requests
from rivescript import RiveScript

bot = RiveScript()
bot.load_directory("./eg/brain")
bot.sort_replies()
#Relevant Parameters for HERE Technologies
app_id=123
app_code=1
latitude=2
longitude=3
#Relevant parameters for HERE technologies
app = Flask(__name__)

ACCESS_TOKEN = "EAAXZBh5wBB74BACCysn5riSQsjmPt1igZCZCopKWzTW0InXultylLBnbvozZBwpOIu75JMGk62sZAgvyjtp2KHYJ5ezZCrWovgdGdP4zaTcigJEORYJiR0JYlSdefXgCrN2lcsS6BFMx70WlyOShS6aC6YP345nFtpbRgRkeMY5gZDZD" 

def get_maps():
	'''Return map image of location'''
	return requests.get("https://image.maps.cit.api.here.com/mia/1.6/mapview?c=" +latitude+"%2"+longitude+"&z=14"+ "&app_id="+app_id+"&app_code="+app_code)


def quick_reply_API(user_id,list_of_text, displaytext):
	"""
	Sends the API call to generate the button.
	"""
	#The API call for buttons. Takes a list of text to display. Generates the JSON code to submit as the API call. Display text is what the chat bot will reply to the user. Generally limit list of text to at more 4 strings. Display text can be capitalised.
	startthing = {
		"recipient":{
	    "id":user_id
		},
		"message":{
    		"text": displaytext,
    		"quick_replies":[]
		}
	}
	for i in list_of_text:
		phdict = {}
		phdict ["content_type"] = "text"
		phdict ["title"] = i
		phdict ["payload"] = "placeholder"	
		startthing["message"]["quick_replies"].append(phdict)

	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=startthing)


def reply_user(user_id,msg):
	# Function to Reply the user. Checks for case of API calls beforehand.	
	flag = -1
	msg = msg[0].upper() + msg[1:]
	if "||s" in msg:
		flag = 1
		msg = msg[:-4]
	elif "||d" in msg:
		flag = 2
		msg = msg[:-4]
	data = {"recipient": {"id": user_id}, "message": {"text": msg}}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	if flag == 1:
		
		quick_reply_API(user_id, ["Recycle", "Daily Tips", "Events"], "Select what you would like help with.")
	
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
