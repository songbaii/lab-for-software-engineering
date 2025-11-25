from flask import Flask, request, jsonify
from config import Config
from models import db
import time
from sqlalchemy import text
from recommend import recommend_by_user_id

app = Flask(__name__)
app.config.from_object(Config)
app.config['JSON_AS_ASCII'] = False

# 初始化数据库
db.init_app(app)

from models import Movie, MovieGenre, UserJudge, UserComment, User, GenreTable, MovieStats

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # 使用text()包装SQL表达式
        db.session.execute(text('SELECT 1'))

        return jsonify({
            'success': True,
            'message': '服务运行正常',
            'database': '连接正常'
        }), 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        import traceback
        traceback.print_exc()

        return jsonify({
            'success': False,
            'message': '数据库连接失败',
            'error': str(e)
        }), 500

@app.route('/api/login', methods=['POST'])# already check
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
    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({'success': False, 'message': "系统错误"}), 500

@app.route('/api/register', methods=['POST'])# check
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
            'user_id': new_user.user_id
        }), 201
    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({'success': False, 'message': "系统错误"}), 500

@app.route('/api/judge', methods=['POST'])
def judge():
    """
    用户评分接口
    接受的JSON格式: {"user_id": "用户账号" number类型， "movie_id": "电影id" number类型， "rating": "用户评分" number类型}
    返回的JSON格式: {"success": "评分结果" boolean类型， "message": "提示信息" string类型}
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': "评分数据格式错误"
            }), 400

        data = request.get_json()

        # 对应根本不存在这个属性的情况
        if not isinstance(data, dict) or 'user_id' not in data or 'movie_id' not in data or 'rating' not in data:
            return jsonify({
                'success': False,
                'message': "评分属性缺失"
            }), 400

        user_id = str(data.get('user_id')).strip()
        movie_id = str(data.get('movie_id')).strip()
        rating = str(data.get('rating')).strip()

        if not user_id or not movie_id or not rating:
            return jsonify({
                'success': False,
                'message': '用户id，电影id，评分均不能为空',
            }), 400

        try:
            user_id = int(user_id)
        except Exception:
            return jsonify({
                'success': False,
                'message': "用户id输入存在问题"
            }), 400

        try:
            movie_id = int(movie_id)
        except Exception:
            return jsonify({
                'success': False,
                'message': "电影id输入存在问题"
            }), 400

        try:
            rating = float(rating)
        except Exception:
            return jsonify({
                'success': False,
                'message': "评分输入存在问题"
            }), 400

        user = User.query.filter_by(user_id=user_id).first()
        movie = Movie.query.filter_by(movie_id=movie_id).first()

        if not user:
            return jsonify({
                'success': False,
                'message': "不存在该用户"
            }), 401

        if not movie:
            return jsonify({
                'success': False,
                'message': "不存在这一部电影"
            }), 401

        if not ((rating > 0) and (rating <= 5) and (rating * 2 == int(rating * 2))):
            return jsonify({
                'success': False,
                'message': "电影的评分不符合评分要求"
            }), 401
        else:
            new_user_judge = UserJudge(user_id=user_id, movie_id=movie_id, rating=rating)
            db.session.merge(new_user_judge)
            db.session.commit()
            now_movie_judge = UserJudge.query.filter_by(movie_id=movie_id).all()
            ratings = [float(judge.rating) for judge in now_movie_judge]  # 转换为float
            avg_rating = sum(ratings) / len(ratings)
            now_stats = MovieStats.query.filter_by(movie_id=movie_id).first()
            if not now_stats:
                now_stats = MovieStats(movie_id=movie_id, avg_rating=avg_rating, vote_count=1)
            else:
                now_stats.avg_rating = avg_rating
                now_stats.vote_count = len(now_movie_judge)
            db.session.merge(now_stats)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': f'成功评分！！！你是第{now_stats.vote_count}位评分者当前电影均分为{now_stats.avg_rating}',
            }), 201
    except Exception as e:
        print(f"发生错误{e}")
        return jsonify({'success': False, 'message': "系统错误"}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    推荐接口
    接受的JSON格式: {"user_id": "用户账号" number类型
    返回的JSON格式: {"success": "推荐结果" boolean类型， "message": "提示信息" string类型, "data": "推荐电影信息" 以数组的形式进行传输，每一个都具有"movie_id", "movie_name", "release_year", "avg_rating", "vote_count"属性}
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'message': "请求电影推荐数据格式错误"
        }), 400

    data = request.get_json()

    # 对应根本不存在这个属性的情况
    if not isinstance(data, dict) or 'user_id' not in data:
        return jsonify({
            'success': False,
            'message': "请求电影推荐属性缺失"
        }), 400

    user_id = str(data.get('user_id')).strip()

    if not user_id :
        return jsonify({
            'success': False,
            'message': '用户id不能为空',
        }), 400

    try:
        user_id = int(user_id)
    except Exception:
        return jsonify({
            'success': False,
            'message': "用户id输入存在问题"
        }), 400

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({
            'success': False,
            'message': "不存在该用户"
        }), 401

    recommend_movies = recommend_by_user_id(user_id, top_k=20, min_sim=0.01, recent_ratings_limit=20, random_factor=0.3)

    return jsonify({
        'success': True,
        'message': "成功推荐电影!!!",
        'recommend_movies': recommend_movies
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)