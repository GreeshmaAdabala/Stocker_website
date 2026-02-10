from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# Temporary user storage
users = {}

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ABOUT ----------------

@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- CONTACT ----------------

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        session["user"] = username
        session["email"] = email

        return redirect("/dashboard")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Just store session (no checking)
        session["user"] = username
        session["email"] = email

        return redirect("/dashboard")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", username=session["user"])

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
