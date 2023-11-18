from decimal import Decimal

from flask import Flask, jsonify, render_template, request
from flask_cors import cross_origin

from pay import Grade

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/payslip", methods=["GET", "POST"])
@cross_origin()
def payslip():
    gross = Decimal(request.form["gross"])
    health = request.form["health"]
    contrib = request.form["contrib"]
    housing = request.form["housing"]
    health = bool(health)
    contrib = bool(contrib)
    housing = bool(housing)
    print(f"gross: {gross}")
    print(f"health: {health}, {type(health)}")
    print(f"contrib: {contrib}, {type(contrib)}")
    grade = Grade(
        gross=gross,
        health_ins=bool(health),
        contrib=bool(contrib),
        housing=housing,
    )  # type: ignore
    monthly_pay = grade.get_net_pay()
    payee = grade.monthly_payee()
    health = grade.get_health_empl()
    housing = grade.get_housing()
    pension = grade.get_total_pension() / 12
    emp_pension = grade.get_pension_employees() / 12
    nsitf = grade.get_nsitf()/12
    response = jsonify(
        {
            "payslip": f"{monthly_pay:,}",
            "payee": f"{payee:,}",
            "health": f"{health:,}",
            "housing": f"{housing:,}",
            "pension": f"{pension:,}",
            "emp_pension": f"{emp_pension:,}",
            "nsitf": f"{nsitf:,}",
        }
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Payslip...")
    app.run(host='127.0.0.1',debug=True)
