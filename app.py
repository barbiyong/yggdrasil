# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
from decimal import Decimal
import detail
from read_data import check_data_is_up_to_date
import get_template_result as scan
from classify import classify
app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def main():
    # update data
    check_data_is_up_to_date()
    function_name = request.args.get('function_name')
    if function_name == 'get_stock_detail':
        stock_name = request.args.get('stock_name')
        message = detail.get_stock_data(stock_name)
        return jsonify(message)
    elif function_name == 'trading_summary':
        message = detail.trading_summary()
        return jsonify(message)
    elif function_name == 'tfex_summary':
        message = detail.tfex_summary()
        return jsonify(message)
    elif function_name == 'set_realtime_summary':
        message = detail.set_realtime_summary()
        return jsonify(message)
    elif function_name == 'scan_template_manual':
        stock_type = request.args.get('stock_type')
        growth = request.args.get('growth')
        lose = request.args.get('most_lose')
        periods = request.args.get('period')
        print(stock_type, growth, lose, periods)
        message = scan.get_stock_name_of_growth_more_than_percent_with_period(stock_type, Decimal(growth), Decimal(lose), int(periods))
        # message = 0
        return jsonify(message)
    elif function_name == 'scan_template_auto':
        stock_type = request.args.get('stock_type')
        period = request.args.get('period')
        message = {
            "message": [{
                "text": "hello, world!"
            }]
        }
        if period == 'Daily':
            message = scan.get_stock_name_of_growth_more_than_percent_with_period(stock_type, Decimal(5), Decimal(100), 2)
        elif period == 'Weekly':
            message = scan.get_stock_name_of_growth_more_than_percent_with_period(stock_type, Decimal(10), Decimal(100), 5)
        elif period == 'Monthly':
            message = scan.get_stock_name_of_growth_more_than_percent_with_period(stock_type, Decimal(20), Decimal(100), 20)
        print(message)
        print("ready to send back")
        print(jsonify(message))
        return jsonify(message)
    elif function_name == 'classify':
        stock_type = request.args.get('stock_type')
        growth = Decimal(request.args.get('growth'))
        period = request.args.get('period')
        loss = Decimal(request.args.get('most_lose'))
        print(stock_type, growth, loss, period)
        message = classify(stock_type=stock_type, growth=growth, lose=loss, periods=int(period))
        print(message)
        print("ready to send back")
        print(jsonify(message))
        # message = {
        #     "message": [{
        #         "text": "hello, world!"
        #     }]
        # }
        return jsonify(message)
    elif function_name == 'update_data':
        check_data_is_up_to_date()
    else:
        message = {
            "messages": [
                {"text": u" Feature นี้ กำลังอยู่ระหว่างพัฒนาครับ ! "}
            ]
        }
        return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
