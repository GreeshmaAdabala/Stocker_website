from flask import Flask, render_template, request, redirect, session, jsonify
import boto3, uuid, datetime
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
app.secret_key = "secret123"

# AWS Connections
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
sns = boto3.client("sns", region_name="us-east-1")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:864981741884:stocktrading"   # Replace with real ARN

# DynamoDB Tables
users = dynamodb.Table("Users")
portfolio = dynamodb.Table("Portfolio")
trades = dynamodb.Table("Trades")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":
        email=request.form.get("email")
        username=request.form.get("username")

        session["email"]=email
        session["user"]=username

        return redirect("/dashboard")

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        email=request.form.get("email")
        username=request.form.get("username")
        password=request.form.get("password")

        users.put_item(Item={
            "email":email,
            "username":username,
            "password":password,
            "wallet":10000
        })

        session["email"]=email
        session["user"]=username

        return redirect("/dashboard")

    return render_template("register.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect("/login")

    user=users.get_item(Key={"email":session["email"]})["Item"]

    return render_template("dashboard.html",
        username=user["username"],
        wallet=user["wallet"]
    )


# ---------------- BUY ----------------

@app.route("/buy", methods=["POST"])
def buy():

    if "email" not in session:
        return jsonify({"error":"Login required"})

    email=session["email"]

    stock=request.json["stock"]
    qty=int(request.json["qty"])
    price=int(request.json["price"])

    total=qty*price

    user=users.get_item(Key={"email":email})["Item"]

    if user["wallet"]<total:
        return jsonify({"error":"Low balance"})

    # update wallet
    users.update_item(
        Key={"email":email},
        UpdateExpression="SET wallet = wallet - :t",
        ExpressionAttributeValues={":t":total}
    )

    # add to portfolio
    portfolio.put_item(Item={
        "email":email,
        "stock":stock,
        "qty":qty,
        "price":price
    })

    # trade history
    trades.put_item(Item={
        "email":email,
        "trade_id":str(uuid.uuid4()),
        "stock":stock,
        "qty":qty,
        "amount":total,
        "type":"BUY",
        "timestamp":str(datetime.datetime.now())
    })

    # 🔥 SNS Notification
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f"BUY ALERT\nStock: {stock}\nQty: {qty}\nAmount: {total}",
        Subject="Stock Purchased"
    )

    return jsonify({"success":True})


# ---------------- SELL ----------------

@app.route("/sell", methods=["POST"])
def sell():

    if "email" not in session:
        return jsonify({"error":"Login required"})

    email=session["email"]

    stock=request.json["stock"]
    qty=int(request.json["qty"])
    price=int(request.json["price"])

    total=qty*price

    # update wallet
    users.update_item(
        Key={"email":email},
        UpdateExpression="SET wallet = wallet + :t",
        ExpressionAttributeValues={":t":total}
    )

    trades.put_item(Item={
        "email":email,
        "trade_id":str(uuid.uuid4()),
        "stock":stock,
        "qty":qty,
        "amount":total,
        "type":"SELL",
        "timestamp":str(datetime.datetime.now())
    })

    # 🔥 SNS Notification
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f"SELL ALERT\nStock: {stock}\nQty: {qty}\nAmount: {total}",
        Subject="Stock Sold"
    )

    return jsonify({"success":True})


# ---------------- PORTFOLIO ----------------

@app.route("/portfolio")
def get_portfolio():

    if "email" not in session:
        return jsonify([])

    email=session["email"]

    data = portfolio.query(
        KeyConditionExpression=Key("email").eq(email)
    )

    return jsonify(data["Items"])


# ---------------- WALLET ----------------

@app.route("/wallet")
def wallet():

    if "email" not in session:
        return jsonify({"wallet":0})

    user=users.get_item(Key={"email":session["email"]})["Item"]
    return jsonify({"wallet":user["wallet"]})


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
