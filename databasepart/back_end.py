from flask import Flask, request, jsonify
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

@app.route('api/login', methods=['POST'])
def login():
    """
    用户登录接口
    接收JSON格式: {"username": "用户名", "password": "密码"}
    """
    try:
        # 获取前端发送的数据
        data = request.get_json()

        # 验证数据完整性
        if not data:
            return jsonify({
                'success': False,
            }), 400

        username = int(data.get('username'))
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'success': False,
            }), 400

        # 在数据库中查找用户
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({
                'success': False,
            }), 401

        # 验证密码
        if user.check_password(password):
            return jsonify({
                'success': True,
            }), 200
        else:
            return jsonify({
                'success': False,
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
        }), 500


@app.route('/register', methods=['POST'])
def register():
    """
    用户注册接口
    接收JSON格式: {"username": "用户名", "password": "密码"}
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': '请求数据不能为空'
            }), 400

        username = data.get('username')
        password = data.get('password')

        # 验证数据完整性
        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码都不能为空'
            }), 400

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': '用户名已存在'
            }), 400

        # 创建新用户
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '注册成功',
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500


@app.route('/check_health', methods=['GET'])
def check_health():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': '服务运行正常',
        'database': 'connected'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)