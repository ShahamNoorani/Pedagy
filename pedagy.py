from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
# from lookatevent import showTenEvents

# The session object makes use of a secret key.
SECRET_KEY = '38'
app = Flask(__name__)
app.config.from_object(__name__)

class Assignment:
    def __init__(self, cls, dueIn=-1, notes="none", complete=False):
        self.cls = cls
        self.dueIn = dueIn
        self.notes = notes
        self.complete = complete

    def desc(self):
        return("Class: " + str(self.cls) + ", due in: " + str(self.dueIn) + ", " + self.notes)

class Event:
    def __init__(self, desc, date):
        self.desc = desc
        self.date = date

class User:
    def __init__(self, phone, name, homework=[], events=[], returning=False, responses=[]):
        self.homework = homework
        self.events = events
        self.returning = returning
        self.phone = phone
        self.responses = responses
        self.name = name
        
users = []
re = "How else may I help you?"


@app.route("/", methods=['GET', 'POST'])
def hello():
    """Respond with the number of text messages sent between two parties."""
    # Increment the counter
    counter = session.get('counter', 0)
    currentTask = session.get('currentTask', 0)

    if request.method == 'POST':
        userMsg = request.form['Body']
    userMsg = userMsg.lower()
    currentUser = ""
    message = ""

    # Save the new counter value in the session

    from_number = request.values.get('From')

    for u in users:
        if u.phone == from_number:
            currentUser = u

    if counter == 0:
        counter = 1
    
    if counter == 1:
        message = "Hello, my name is Pedagy, may I have yours?"

    if counter == 2:
        if currentUser != "":
            message = "How else may I help you?"
        else:
            currentUser = User(from_number, userMsg)
            users.append(currentUser)
            message = "Hi " + currentUser.name + ", it's nice to meet you. How may I help you today?"
        
    if counter == 3:
        need = userMsg
        if need == "add hw":
            session['currentTask'] = "homework"
            message = "For what class?"
        elif need == "schedule an event":
            session['currentTask'] = "schedule"
            message = "Could you describe the event?"
        elif need == "show hw":
            if len(currentUser.homework) == 0:
                message += "You have no homework, you lucky bastard. How else can I help you?"
                counter = 2
            for hw in currentUser.homework:
                message += hw.desc() + "\n"
                counter = 2
        elif need == "show schedule":
            for event in currentUser.events:
                message += event.desc + ", " + event.date + "\n"
            counter = 2
        else:
            message += "I'm sorry, I don't understand \'" + need + "\', how can I help you?"
            counter = 2

    if counter >= 4:
        if currentTask == "homework":
            if len(currentUser.homework) == 0:
                currentUser.homework.append(Assignment(""))
            currentHW = currentUser.homework[-1]
            if len(currentHW.cls) == 0:
                currentHW.cls = userMsg
                message = "How many days till it's due?"
            elif currentHW.dueIn == -1:
                currentHW.dueIn = userMsg
                message = "Any notes about this assignment?"
            else:
                currentHW.notes = userMsg
                message += "How else may I help you?"
                counter = 2
        elif currentTask == "schedule":
            if len(currentUser.events) == 0:
                currentUser.events.append(Event("", ""))
            currentEvent = currentUser.events[-1]
            if len(currentEvent.desc) == 0:
                currentEvent.desc = userMsg
                message = "When is it?"
            else:
                currentEvent.date = userMsg
                message += "How else may I help you?"
                counter = 2
        else:
            print(str(counter))
            counter = 2

    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message + " " + str(counter))
    session['counter'] = counter + 1

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)