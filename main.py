from flask import Flask, request, redirect, render_template, url_for
from markupsafe import escape
from flask import jsonify
from flask import session
from flask import json
from flask_cors import CORS
from flaskext.mysql import MySQL





app = Flask(__name__)

mysql = MySQL()
mysql.init_app(app)


cors = CORS(app, resources={r"/api/*": {"origins": "*"}})




EstadoLed = True


#MYSQL_DATABASE_HOST	default is ‘127.0.0.1’
#MYSQL_DATABASE_PORT	default is 3306
#MYSQL_DATABASE_USER	default is None
#MYSQL_DATABASE_PASSWORD	default is None
#MYSQL_DATABASE_DB	default is None
#MYSQL_DATABASE_CHARSET	default is ‘utf-8’


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!" 


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/arduino', methods=['GET', 'POST'])
def arduino():
    Edo = leer()
    print(Edo)

    try:
        if Edo ==  "ON":

            return "ON"
        elif Edo == "OFF":

            return "OFF"

    except Exception as e:
        response = {
            "Error": "True",
            "Message" :"Error  {} ".format(e)
        }
        return json(response)

def cambiaestado(std):
    EstadoLed = std
    return EstadoLed

def getstado():
    return EstadoLed

@app.route('/index')
def template():

    return render_template('index.html')

@app.route('/api/serveriot',  methods=['GET'])
def getstatus():
    text = leer()
    return text

@app.route('/api/enviadata',  methods=['POST'])
def getpost():
    datajson = request.get_json()
    return datajson


@app.route('/api/serveriot/<status>' , methods=['GET'])
def dummy(status):
    try:
        if status=='1':

            EstadoLed = escribir("ON")

            response = {
                "Error": "False",
                "Message": "Estado {} ".format(status),
                "Edo": EstadoLed
            }

            #response = app.response_class(
            #    response=json.dumps(data),
            #    status=200,
            #    mimetype='application/json'
            #)

            return jsonify(response)

        elif status=='0':
            EstadoLed = escribir("OFF")
            response = {
                "Error": "False",
                "Message": "Estado {} ".format(status),
                "Edo": EstadoLed
            }

            # response = app.response_class(
            #    response=json.dumps(data),
            #    status=200,
            #    mimetype='application/json'
            # )

            return jsonify(response)

        else:

            response = {
                "Error": "False",
                "Message": "Estado no valido"
            }

            # response = app.response_class(
            #    response=json.dumps(data),
            #    status=200,
            #    mimetype='application/json'
            # )

            return jsonify(response)


    except Exception as e:
        response = {
            "Error": "True",
            "Message" :"Error  {} ".format(e)
        }
        return jsonify(response)


def escribir(EDO):
    file1 = open("guardado.txt", "w")
    #file1.write("%s = %s\n" % ("dict1", dict1))
    file1.write(EDO)

    file1.close()

def leer():
    f = open('guardado.txt', 'r')
    if f.mode == 'r':
        contents = f.read()

        print(contents)
    return contents


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    #verDebug = True if (os.environ.get('Debug', "True")) == "True") else  False
    app.run(debug=True,host= '0.0.0.0' , port=5000)