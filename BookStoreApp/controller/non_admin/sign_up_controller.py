import json
from flask import request, jsonify
from BookStoreApp import app
from BookStoreApp.service.non_admin.sign_up_service import set_sign_up as siu, get_verification as gv, \
    is_username_exactly as iue
from BookStoreApp.controller.utils.utils_controller import send_mail


# lấy dữ liệu và gửi qua service để tạo tài khoản
@app.route('/client/api/sign-up', methods=['post'])
def set_sign_up():
    data = json.loads(request.data)
    listData = {
        'last_name': data.get('last_name'),
        'first_name': data.get('first_name'),
        'date_of_birth': data.get('date_of_birth'),
        'phone_number': data.get('phone_number'),
        'email': data.get('email'),
        'city': data.get('city'),
        'district': data.get('district'),
        'address': data.get('address'),
        'username': data.get('username'),
        'password': data.get('password')
    }
    if iue(listData['username']):  # username đã tồn tại
        return jsonify('exist')

    try:
        siu(listData)
    except:
        return jsonify('error')

    return jsonify("successful")


# gửi email xác nhận
@app.route('/client/api/sign-up-confirm', methods=['post'])
def set_confirm():
    data = json.loads(request.data)
    email = data.get('email')
    info = gv()
    try:
        send_mail(from_gmail_account='dream.bookstore.main@gmail.com',
                  from_gmail_password='qezdqucuugmlnlkr',
                  to_mail_account=email,
                  message=info['message'])

    except:
        return jsonify('error')

    return jsonify(info['number'])
