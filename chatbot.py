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

#The API call for buttons for after you say Hi to Rize. <3
startthing = {
  "recipient":{
    "id":"USER_ID"
  },
  "message":{
    "text":"Pick a color:",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Tips",
        "payload":"Tips"
      },
      {
        "content_type":"text",
        "title":"Recycling Help!",
        "payload":"Recycling Help"
      }
    ]
  }
}

def get_maps():
	'''Return map image of location'''
	return requests.get("https://image.maps.cit.api.here.com/mia/1.6/mapview?c=" +latitude+"%2"+longitude+"&z=14"+ "&app_id="+app_id+"&app_code="+app_code)


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
