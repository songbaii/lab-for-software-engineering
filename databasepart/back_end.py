from flask import Flask, request, jsonify
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 创建数据库表（首次运行）
with app.app_context():
    db.create_all()

    # 创建测试用户（首次运行后可以注释掉）
    if not User.query.filter_by(username='admin').first():
        test_user = User(username='admin')
        test_user.set_password('admin123')
        db.session.add(test_user)
        db.session.commit()
        print("测试用户已创建: admin / admin123")


@app.route('/login', methods=['POST'])
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
                'message': '请求数据不能为空'
            }), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400

        # 在数据库中查找用户
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 401

        # 验证密码
        if user.check_password(password):
            return jsonify({
                'success': True,
                'message': '登录成功',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '密码错误'
            }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
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