from flask import Flask, request
import requests
from rivescript import RiveScript

bot = RiveScript()
bot.load_directory("./eg/brain")
bot.sort_replies()
#Relevant Parameters for HERE Technologies
app_id="KJAW38LhkUzE9mqhLkhJ"
app_code="JwkhODcTyZm4egOPsL5b-w"
latitude=2
longitude=3
#Relevant parameters for HERE technologies
app = Flask(__name__)

userlist = {1: 3} #I'm doing whatever works now. Sorry.
		  #Placeholder value, because the thing might crash if 
		  #the user screws around with his responses and accidentally 
		  #triggers this function below (when no users)

def calculate_average ():
	output = 0	
	for i in userlist:
		output += userlist[i]
	return output / len(userlist)

def send_recycle(latitude,longitude):
    '''send location of nearest recycling bins '''
    ''' minimum is  the minimum distance in coordinate units'''
    list_of_coordinates=[[1.2965272,103.7848397],[1.2962203,103.7848397],[1.2965300,103.781241],[1.2965272,103.7823425],[1.2964362,103.7848397]] #Hard Coded Lord bless my soul
 
    for arr in list_of_coordinates:
        if((arr[0]-latitude)**2 +(arr[1]-longitude)**2)<1: #no time to test this.
            latitude=arr[0]
            longitude=arr[1]
 
    return requests.get("https://image.maps.cit.api.here.com/mia/1.6/mapview?c=" +str(latitude)+"%2"+str(longitude)+"&z=14"+ "&app_id="+app_id+"&app_code="+app_code)

ACCESS_TOKEN = "EAAXZBh5wBB74BACCysn5riSQsjmPt1igZCZCopKWzTW0InXultylLBnbvozZBwpOIu75JMGk62sZAgvyjtp2KHYJ5ezZCrWovgdGdP4zaTcigJEORYJiR0JYlSdefXgCrN2lcsS6BFMx70WlyOShS6aC6YP345nFtpbRgRkeMY5gZDZD" 

def get_maps():
	'''Return map image of location'''
	return requests.get("https://image.maps.cit.api.here.com/mia/1.6/mapview?c=" +latitude+"%2"+longitude+"&z=14"+ "&app_id="+app_id+"&app_code="+app_code)


def send_location(user_id):
    '''asks user to share location'''
    location={
    "recipient":{
    "id":user_id
    },
    "message":{
    "text":"Please share your location:",
    "quick_replies":[
      {
        "content_type":"location",
      }
    ]
    }
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=location)

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

def post_message (user_id, msg):
	# Migrated the function to post the message to here
	# Allows for multiple calls so the bot can post twice
	# Probably.
	data = {"recipient": {"id": user_id}, "message": {"text": msg}}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print resp
	
def post_image (user_id, msg):
	image = {"recipient":{"id":user_id},"message":{"attachment":{"type":"image","payload":{"url":msg}}}}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=image)




def reply_user(user_id,msg,lat, lon):
	# Function to Reply the user. Checks for case of API calls beforehand.		
	flag = -10
	msg = msg[0].upper() + msg[1:]
	if "||s" in msg:
		flag = 1
	elif "||d" in msg:
		flag = 2
	elif "||a" in msg:
		flag = 3
	elif "||q" in msg: 
	#This is for the gamification aspect. 
	#Format of msg is "*||q", * is a digit corresponding to the user's score
		global userlist #Yes. I'm doing whatever works now. Sorry.
		if user_id not in userlist:
			userlist[user_id] = 0
		userlist[user_id] = userlist[user_id] + int(msg[0])
		msg = "Congrats, You have earned " + msg[0] + " points"
		post_message (user_id, msg)
		msg = "You have " + str(userlist[user_id]) + " points in total!"
		flag = -3 #Duct Tape
	elif "||w" in msg:
		flag = 4
	elif "||z" in msg:
		flag = 5
	elif "||e" in msg:
		flag = 6
		msg = msg [:-4]
		post_message(user_id, msg)
		msg = "https://goo.gl/EChDtd |||"
	elif "||x" in msg:
		msg = msg [:-4]
		post_message(user_id, msg)
		msg = "https://goo.gl/m1UQWS"
		post_image(user_id, msg)
		return
	elif "||l" in msg:
		msg = msg [:-4]
		post_message(user_id, msg)
		msg = "https://image.ibb.co/bJuiyQ/Here_Maps.png"
		post_image(user_id, msg)
		return
	elif "|||" in msg:
		flag = -2
	if flag > -3: #Duct Tape
		msg = msg [:-4] #Duct Tape
		# Removes flags from the message if there are flags

	post_message (user_id, msg)
	#This is to post the message

	if flag == 1:
		choices_list = ["Recycle", "Daily Tips", "Event", "Claim Rewards"]
		title_text = "Select what you would like help with."
	elif flag == 2:
		choices_list = ["Instant Tip", "Subscribe", "Top Stories"]
		title_text = "How may I help you with your tips?"
	elif flag == 3:
		choices_list = ["Create Reminder", "Join Event"]
		title_text = "What do you want to do?"
	elif flag == -3	: #Duct tape.
		avg = calculate_average ()
		msg = "The Average score of users is " + str(avg)		
		post_message (user_id, msg)
	elif flag == 4:
		choices_list = ["Show the average"]
		title_text = "Want to see how you fare with the average?"
	elif flag == 5:
		choices_list = ["Get another tip", "Back to menu"]
		title_text = "Would you like another tip?"
	elif flag == 6:
		choices_list = ["See more"]
		title_text = "Would you like to see more stories?"
	if flag > -2: #Duct Tape
		quick_reply_API(user_id, choices_list, title_text)
		# Posts the quick reply if necessary
	elif flag == -2:
		send_location(user_id)

@app.route('/', methods=['GET'])
def handle_verification():
	return request.args['hub.challenge']

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    print data
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
#    latitude=data['entry'][0]['messaging'][0]['message']["attachments"][0]["payload"]["coordinates"]["lat"]
#    longitude=data['entry'][0]['messaging'][0]['message']["attachments"][0]["payload"]["coordinates"]["long"]
    # I cannot make this work. Im sorry.
    latitude = 1.2965272
    longitude = 103.7848397
    reply = bot.reply("localuser", message)
    reply_user(sender, reply, latitude, longitude)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
