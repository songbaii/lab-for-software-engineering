from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# 接收GET请求中的账号密码
@app.route('/login', methods=['GET'])
def login_get():
    username = request.args.get('username')
    password = request.args.get('password')

    # 这里应该添加密码验证逻辑
    print(f"GET方式接收 - 用户名: {username}, 密码: {password}")

    return jsonify({
        'status': 'success',
        'message': '登录成功',
        'username': username
    })


# 接收POST请求中的账号密码（推荐方式）
@app.route('/login', methods=['POST'])
def login_post():
    # 检查Content-Type
    content_type = request.content_type

    if 'application/json' in content_type:
        # 接收JSON格式数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    elif 'application/x-www-form-urlencoded' in content_type:
        # 接收表单格式数据
        username = request.form.get('username')
        password = request.form.get('password')
    else:
        # 其他格式
        username = request.values.get('username')
        password = request.values.get('password')

    # 简单的验证逻辑（实际应用中应该更复杂）
    if not username or not password:
        return jsonify({
            'status': 'error',
            'message': '用户名和密码不能为空'
        }), 400

    print(f"POST方式接收 - 用户名: {username}, 密码: {password}")

    # 这里应该添加数据库验证等逻辑
    if username == 'admin' and password == '123456':
        return jsonify({
            'status': 'success',
            'message': '登录成功',
            'username': username
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '用户名或密码错误'
        }), 401


if __name__ == '__main__':
    app.run(debug=True)