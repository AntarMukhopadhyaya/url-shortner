from ast import If
import sqlite3 as db, random, string

from flask import Flask, render_template, redirect, request, flash
app = Flask(__name__)
app.secret_key = 'Your Secret Key'

conn = db.connect("urls.db")
conn.execute("CREATE TABLE  IF NOT EXISTS urls (url_id INT AUTO_INCREMENT PRIMARY KEY, input_url VARCHAR(255) NOT NULL, short_url VARCHAR(255) NOT NULL, created_at DATETIME default current_timestamp);")


@app.route("/", methods=['POST', "GET"])
def home():
    if request.method == "POST":
        input_url = request.form['input_url']
        if input_url == None or len(input_url) < 0:
        
            return redirect("/")
        short_url = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=8))
        with db.connect("urls.db") as conn :
            cursor = conn.cursor()
            cursor.execute("INSERT INTO  urls (input_url, short_url) VALUES(?,?)",(input_url, short_url))
            conn.commit()
            flash("Successfully Shortened the following URL")
        conn.close()
        short_url = request.base_url + short_url

        return render_template("index.html",input_url = input_url, short_url=short_url)

    return render_template("index.html")
@app.route("/<string:short_url>",methods=["GET"])
def redirect_url(short_url):
    if short_url and short_url != None:
        with db.connect("urls.db") as conn:
            cursor = conn.cursor()
            if cursor.execute("SELECT * FROM urls WHERE short_url=?",(short_url,)):
                data = cursor.fetchone()

                return redirect(data[1],code=302 )
        conn.close()
    else:
        return redirect("/")
                
            


if __name__ == "__main__":
    app.run(debug=True)
