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
    # print(f"gross: {gross}")
    # print(f"health: {health}, {type(health)}")
    # print(f"contrib: {contrib}, {type(contrib)}")
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
    nsitf = grade.get_nsitf() / 12
    response = jsonify(
        {
            "payslip": f"{monthly_pay:,.2f}",
            "payslip2": monthly_pay,
            "payee": f"{payee:,.2f}",
            "payee2": payee,
            "health": f"{health:,.2f}",
            "health2": health,
            "housing2": housing,
            "housing": f"{housing:,.2f}",
            "pension": f"{pension:,.2f}",
            "pension2": pension,
            "emp_pension": f"{emp_pension:,.2f}",
            "emp_pension2": emp_pension,
            "nsitf": f"{nsitf:,.2f}",
            "nsitf2": nsitf,
        }
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# @app.route("/chart_data", methods=["GET", "POST"])
# @cross_origin()
# def chart_data():
#     gross = Decimal(request.form["gross"])
#     health = request.form["health"]
#     contrib = request.form["contrib"]
#     housing = request.form["housing"]
#     health = bool(health)
#     contrib = bool(contrib)
#     housing = bool(housing)
#     grade = Grade(
#         gross=gross,
#         health_ins=bool(health),
#         contrib=bool(contrib),
#         housing=housing,
#     )  # type: ignore
#     monthly_pay = grade.get_net_pay()
#     payee = grade.monthly_payee()
#     health = grade.get_health_empl()
#     housing = grade.get_housing()
#     pension = grade.get_total_pension() / 12
#     emp_pension = grade.get_pension_employees() / 12
#     nsitf = grade.get_nsitf() / 12
#     response = jsonify(
#         {
#             "payslip": monthly_pay,
#             "payee": payee,
#             "health": health,
#             "housing": housing,
#             "pension": pension,
#             "emp_pension": emp_pension,
#             "nsitf": nsitf,
#         }
#     )
#     print(response)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Headers", "*")
#     response.headers.add("Access-Control-Allow-Methods", "*")
#     return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Payslip...")
    app.run(host="127.0.0.1", debug=True)
