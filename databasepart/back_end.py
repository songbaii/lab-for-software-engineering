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
    try:
        # 获取前端发送的数据
        data = request.get_json()

        # 验证数据完整性
        if not data:
            return jsonify({
                'success': False,
                'message': "未接收到信息"
            }), 400

        if not isinstance(data, dict):
            return jsonify({
                'success': False,
                'message': "请求数据格式错误"
            }), 400

        # 检查参数是否存在
        user_id = data.get('user_id')
        password = data.get('password')
        if user_id is None or password is None:
            return jsonify({
                'success': False,
                'message': "用户ID和密码不能为空"
            }), 400

        # 去除空格并检查空值
        user_id_str = str(data.user_id).strip()
        password = str(data.password).strip()
        user_id = int(data.get('user_id'))
        password = data.get('password')

        if not user_id or not password:
            return (jsonify({
                'success': False,
                'messge': "传递信息存在缺失",
                'user_id': user_id,
                'password': password
            }), 400)

        # 在数据库中查找用户
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
            return jsonify({
                'success': False,
                'messge': "不存在该用户"
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
                "messge": "密码错误"
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': "未知错误"
        }), 500


@app.route('/api/register', methods=['POST'])
def register():
    """
    用户注册接口
    接收JSON格式: {"user_name": "用户账号" string类型, "password": "密码" string类型}
    返回的JSON: {"success": "登录结果" boolean类型, "message": "提示信息" string类型, "user_id": "分配的用户账号" number类型}
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': '请求数据不能为空',
                'user_id': ''
            }), 400

        user_name = data.get('user_name')
        password = data.get('password')

        # 验证数据完整性
        if not user_name or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码都不能为空',
                'user_id': ''
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

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500

@app.route('/debug/sql-mode')
def debug_sql_mode():
    try:
        # 使用text()包装SQL表达式
        result = db.session.execute(text("SELECT @@SESSION.sql_mode")).fetchone()
        return jsonify({
            'success': True,
            'sql_mode': result[0],
            'message': 'SQL模式配置成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)