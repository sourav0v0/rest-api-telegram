from flask import Flask,request,jsonify
import random
import requests

app = Flask(__name__)
url = "http://numbersapi.com/"
@app.route("/",methods=['GET'])
def respond():
    req = request.args
    print(req)  #ImmutableiDict([('name', 'Neel')])
    return "You have reached the root endpoint"


#curl -d '({"name":"advait","age":"21"})'
#curl -d '{"name":"advait","age":"21"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/

@app.route("/",methods=['POST'])
def verify():
    #data = request.data
    data = request.get_json()
    print(data.keys())
    return jsonify(data)

@app.route("/getfact",methods=['POST'])
def getFact():
    req = request.get_json()
    intent = req.get("queryResult").get("parameters").get("displayName")
    number = req.get("queryResult").get("parameters").get("number")
    qtype = req.get("queryResult").get("parameters").get("type")
    number2 = req.get("queryResult").get("parameters").get("number2")
    print(req)
    if number is None or not number.isnumeric():
        number = 1;
    if number2 is None or not number2.isnumeric():
        number2 = 1;
    print(number, number2)
    if intent == "numbers":
        if qtype == "random":
            qtype = random.choice(["trivia","year","math"])
        qurl = url + str(int(number)) + "/" + qtype + "?json"
        res = requests.get(qurl).json()["text"]
        print("-----")
        print(res)
        print("-----")
        print(qurl)
        return jsonify({"fulfillmentText":res}) #prinnt on dialofflow
    if intent == "addition":
        addition = int(number) + int(number2);
        print(addition)
        return jsonify({"fulfillmentText":addition});
    elif intent == "multiply":
        multiply = int(number) * int(number2);
        print(multiply)
        return jsonify({"fulfillmentText":multiply});
    elif intent == "substraction":
        substraction = int(number) - int(number2);
        print(substraction)
        return jsonify({"fulfillmentText":substraction});
    elif intent == "division":
        try:
            division = int(number) / int(number2);
        except: 
            return jsonify({"fulfillmentText":"Ohh Your cant divide it by Zero"}); 
        return jsonify({"fulfillmentText":division});
    elif intent == "joke":
        jsonRespone = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw&type=single').json()
        return jsonify({"fulfillmentText":jsonRespone['joke']});
    print(intent,number,qtype)
    print(req)  #print on server side
    return jsonify({"fulfillmentText":"Flask server hit"}) #return on client side

if __name__ == "__main__":
    app.run()
