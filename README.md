# Stocker - Stock Market Trading Website

Stocker is a web-based stock market trading application developed using Flask and AWS cloud services. The application provides users with a simple interface to register, log in, manage a virtual wallet, buy and sell stocks, view their portfolio, and maintain trade history.

The project demonstrates the integration of a Flask web application with AWS services for cloud-based data storage and real-time trade notifications.

## Features

- User Registration and Login
- User Session Management
- Virtual Wallet with an initial balance
- Stock Buying
- Stock Selling
- Portfolio Management
- Trade History
- Wallet Balance Tracking
- Buy/Sell Transaction Records
- AWS Cloud Database Integration
- AWS SNS Notifications for Stock Transactions
- Responsive Web Interface

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### AWS Cloud Services
- Amazon DynamoDB
- Amazon SNS

### Python Libraries
- Flask
- Boto3

## AWS Integration

The AWS-enabled version of the application uses Amazon DynamoDB to store application data and Amazon SNS to send notifications when stock transactions occur.

### Amazon DynamoDB

The application uses three DynamoDB tables:

- `Users` - Stores user details and wallet balance.
- `Portfolio` - Stores stocks purchased by users.
- `Trades` - Stores buy and sell transaction history.

### Amazon SNS

Amazon Simple Notification Service (SNS) is integrated into the application to generate notifications for stock transactions.

When a user:

- Buys a stock → a **Stock Purchased** notification is generated.
- Sells a stock → a **Stock Sold** notification is generated.

## Application Workflow

1. User registers on the website.
2. User receives a virtual wallet balance.
3. User logs into the application.
4. User accesses the trading dashboard.
5. User can buy or sell stocks.
6. The wallet balance is updated according to the transaction.
7. Purchased stocks are stored in the portfolio.
8. Each transaction is recorded in the trade history.
9. AWS SNS generates a notification for the transaction.

## Project Structure

```text
Stocker_website/
│
├── app.py
├── aws_app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
└── static/
    ├── css/
    ├── js/
    ├── img/
    └── lib/
