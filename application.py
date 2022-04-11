from chatbot import model,labels,bag_of_words,words,data
import sys
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = "0"
# if sys.version_info.major < 3:
#     reload(sys)
# sys.setdefaultencoding('utf8')
import razorpay
from flask import Flask, render_template, request
import numpy as np
import random
from flask_cors import CORS

application = Flask(__name__, static_url_path='/static')
client = razorpay.Client(auth=("rzp_live_OgpgPeLThwTOSQ", "iVeCou0uXEequRrdQqEDK7x3"))

CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

application.static_folder = 'static'

@application.route("/")
def home():
    return render_template("index.html")

@application.route("/get")
def get_bot_response():
    
    inp = request.args.get('msg')
    inp=" "+inp+" "
    inp=inp.replace(' ur '," your ")
    inp=inp.replace(' r '," are ")
    inp=inp.replace(' u '," you ")
    results = model.predict([bag_of_words(inp, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

    return (random.choice(responses))

@application.route("/order", methods=["GET"])
def razorpay():

    order=  client.order.create({
    "amount": 10000,
    "currency": "INR",
    "receipt": "receipt#1",
    })
    return order


if __name__ == "__main__":
    application.run()