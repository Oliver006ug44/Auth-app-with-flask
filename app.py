from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "coolpassword"

def init_db():
    conn = sqlite3.connect("user.db")
    conn.execute("""
                    CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        password TEXT
                 )
            """)
    conn.close()


@app.route("/home")
def home():
    if "username" in session:
        return render_template("index.html", name=session["username"])
    return redirect(url_for("login"))




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
    
        conn = sqlite3.connect("user.db")
        curs = conn.cursor()
        curs.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        user = curs.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "USER NOTFOUND!"
        
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
    
        conn = sqlite3.connect("user.db")
        curs = conn.cursor()
        curs.execute("SELECT * FROM user WHERE username = ?", (username,))
        if curs.fetchone():
            return "USER ALREADY EXISTS!"
        
        curs.execute("INSERT INTO user (username,password) VALUES (?,?)",(username,password))
        conn.commit()

        conn.close()

        return redirect(url_for('login'))
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)