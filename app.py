from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

customers = {
    "123": {"name": "Justin", "balance": 5000},
    "124": {"name": "Sarah", "balance": 9000}
}

tokens = {
    "DEMO_TOKEN_123": "123",
    "DEMO_TOKEN_124": "124"
}
permissions = {
    "123": ["vacation.txt", "benefits.txt"],
    "124": ["vacation.txt", "benefits.txt", "payroll.txt"]
}

@app.route("/account/<account_id>")
def get_account(account_id):

    token = request.headers.get("Authorization")

    if token not in tokens:
        return jsonify({"error": "INVALID TOKEN"}), 401

    logged_in_user = tokens[token]

    if account_id != logged_in_user:

        with open("logs/security.log", "a") as log:
            log.write(
            f"{datetime.now()} | user={logged_in_user} | "
            f"requested={account_id} | result=DENIED\n"
        )

        return jsonify({"error": "ACCESS DENIED"}), 403

    return jsonify(customers[account_id])

#agentperms

@app.route("/documents/<requested_document>")
def get_document(requested_document):

    user_token = request.headers.get("Authorization")

    if user_token not in tokens:
        return jsonify({"error": "INVALID TOKEN"}), 401

    logged_in_user = tokens[user_token]

    if requested_document not in permissions[logged_in_user]:

        with open("logs/security.log", "a") as log:
            log.write(
            f"{datetime.now()} | user={logged_in_user} | "
            f"requested={requested_document} | result=DENIED\n"
        )

        return jsonify({"error": "ACCESS DENIED"}), 403

     
    with open(f"documents/{requested_document}", "r") as file:
        content = file.read()

    return jsonify({"content": content})


if __name__ == "__main__":
    app.run(port=5000)