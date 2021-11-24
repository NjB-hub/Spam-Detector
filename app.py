from flask import Flask, request, render_template
import pickle


app = Flask(__name__)

#syntaxe pour définir une route
#app.route(endpoint, methods = ["POST, GET"])

cv = pickle.load(open('SpamPretreatModel.sav', 'rb'))
lr = pickle.load(open('SpamModel.sav', 'rb'))
@app.route('/')
def nothing():
    return render_template('index.html')

@app.route("/api/spamdetector/", methods = ["POST","GET"])

def detector():
    if request.method == 'POST':
        mail = request.form["mail"]
        mail2 = cv.transform([mail])
        p = lr.predict_proba(mail2.toarray().reshape(1, -1))[0]

        spam, ham = p[0], p[1]

        if spam > ham:
            result = "This mail is a spam at " + str(spam * 100) + " %."
        
        else:
            result = "This mail is a ham at " + str(ham * 100) + " %."
        
        return render_template('index.html',mail=mail, result=result)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port = "8000", debug = True, host = "127.0.0.1")