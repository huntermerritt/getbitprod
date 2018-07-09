from flask import Flask, render_template, request, redirect
import redis

app = Flask(__name__)

db = redis.Redis('127.0.0.1')

#@app.route('/')
#def hello_world():

#    return render_template('home.html')

#@app.route('/search')
#def search():
#    return render_template('search.html')

@app.route('/', defaults={'name': ''}, methods=['GET', 'POST'])
@app.route('/<name>', methods=['GET', 'POST'])
def register(name):

    if request.method == "GET":

        if name == "":
            return render_template("home.html")
        else:
            locationstr = db.get(name).decode('UTF-8')

            if locationstr == 'None':
                return render_template('home.html')

            return redirect(locationstr)

    if request.method == "POST":
        searchterm = str(request.form['project'])
        searchterm = searchterm.lower()
        searchterm = searchterm.replace(" ", "_")
        cur = str(db.get(searchterm))
        cur = cur.lower()


        if cur == "none":
            cur = request.form['project']
            cur = cur.lower()
            cur = cur.replace(" ", "_")
            db.getset(cur, str(request.form['location']))

            return render_template('registersuccess.html', proj='http://getbit.host/' + cur)
        else:
            return render_template('registerfailure.html')

    return render_template('home.html')

#@app.route('/find/<name>')
#def find(name):

#    locationstr = db.get(name).decode('UTF-8')

 #   if locationstr == 'None':
  #      return render_template('index.html')

   # return redirect(locationstr)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
