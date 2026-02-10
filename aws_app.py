from flask import Flask, render_template, request, redirect, session
import boto3
import uuid

app = Flask(__name__)
app.secret_key = "secret123"

# AWS Clients
dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
sns = boto3.client("sns", region_name="ap-south-1")

TABLE_NAME = "Users"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:ACCOUNT_ID:TOPIC_NAME"


table = dynamodb.Table(TABLE_NAME)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user_id = str(uuid.uuid4())

        # Save to DynamoDB
        table.put_item(
            Item={
                "user_id": user_id,
                "username": username,
                "email": email,
                "password": password
            }
        )

        # SNS Notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"New user registered: {username}",
            Subject="New Registration"
        )

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
    app.run(host="0.0.0.0", port=5000)
