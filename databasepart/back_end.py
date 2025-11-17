from flask import Flask, request, jsonify
from config import Config
from models import db
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

from models import Movie, MovieGenre, UserJudge, UserComment, User, GenreTable

@app.route('/api/login', methods=['POST'])
def login():
    """
    用户登录接口
    接收JSON格式: {"user_id": "用户账号" number类型, "password": "密码" string类型}
    返回JSON格式: {"success": "登录结果" boolean类型, "message": "提示信息" string类型}
    """

    # 获取前端发送的数据
    # 验证数据完整性
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': "请求数据格式错误"
            }), 400

        data = request.get_json()

        # 对应根本不存在这个属性的情况
        if not isinstance(data, dict) or 'user_id' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': "请求数据格式错误"
            }), 400

        # 去除空格并检查空值
        user_id = str(data.get('user_id')).strip()
        password = str(data.get('password')).strip()

        # 对应全是空格的情况
        if not user_id or not password:
            return jsonify({
                'success': False,
                'message': "用户ID和密码不能为空"
            }), 400

        try:
            user_id = int(user_id)
        except Exception:
            return jsonify({
                'success': False,
                'message': "用户id输入存在问题"
            }), 400

        # 在数据库中查找用户
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
            return jsonify({
                'success': False,
                'message': "不存在该用户"
            }), 401

        # 验证密码
        if user.check_password(password):
            return jsonify({
                'success': True,
                'message': "登录成功"
            }), 200
        else:
            return jsonify({
                'success': False,
                "message": "密码错误"
            }), 401
    except Exception:
        return jsonify({'success': False, 'message': "系统错误"}), 500



@app.route('/api/register', methods=['POST'])
def register():
    """
    用户注册接口
    接收JSON格式: {"user_name": "用户账号" string类型, "password": "密码" string类型}
    返回的JSON: {"success": "登录结果" boolean类型, "message": "提示信息" string类型, "user_id": "分配的用户账号" number类型}
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': "请求数据格式错误",
                'user_id': -1
            }), 400

        data = request.get_json()

        # 对应根本不存在这个属性的情况
        if not isinstance(data, dict) or 'user_name' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': "请求数据格式错误",
                'user_id': -1
            }), 400

        user_name = str(data.get('user_name')).strip()
        password = str(data.get('password')).strip()

        # 验证数据完整性
        if not user_name or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码都不能为空',
                'user_id': -1
            }), 400

        # 创建新用户
        new_user = User(user_name=user_name, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '注册成功',
            'user': new_user.user_id
        }), 201
    except Exception:
        return jsonify({'success': False, 'message': "系统错误"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)