import os, sys

from openai import responses

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file))
sys.path.insert(0, project_root)

import pytest
from back_end import app, db
from models import User, Movie, UserJudge, UserFavoriteGenres

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = True  # 启用调试模式
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://violet:s131601@localhost/soft_ware_engineering'

    with app.test_client() as client:
        with app.app_context():
            yield client

class TestUser:

    def test_login_no_data(self, client):
        # 测试json格式错误
        response = client.post('/api/login', json=None)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_no_dict(self, client):
        # 测试不符合格式
        response = client.post('/api/login', json=123)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_no_user_id(self, client):
        # 测试缺失属性
        response = client.post('/api/login', json={'password': 'testpass'})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_no_password(self, client):
        # 测试缺失属性
        response = client.post('/api/login', json={'user_id': '123'})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_all_blank(self, client):
        # 测试为空
        response = client.post('/api/login', json={'user_id': '   ', 'password': '  '})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_user_id_type(self, client):
        # 测试id格式错误
        response = client.post('/api/login', json={'user_id': 'abc', 'password': '123'})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_user_not_exist(self, client):
        # 测试用户不存在
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_id = test_user.user_id
        db.session.delete(test_user)
        db.session.commit()

        data = {
            'user_id': test_id,  # 不存在的用户ID
            'password': 'testpass'
        }

        response = client.post('/api/login', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_successful_login(self, client):
        # 测试成功登录
        # 插入测试数据 - user_name是VARCHAR，所以用字符串
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_id = test_user.user_id

        """测试成功登录 - 使用真实MySQL"""
        data = {
            'user_id': test_id,  # user_name是VARCHAR，所以用字符串
            'password': 'testpass'
        }

        response = client.post('/api/login', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        db.session.delete(test_user)
        db.session.commit()

    def test_login_wrong_password(self, client):
        # 测试错误的登录密码
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_id = test_user.user_id
        data = {
            'user_id': test_id,
            'password': 'wrong password'
        }

        response = client.post('/api/login', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False
        db.session.delete(test_user)
        db.session.commit()

    def test_create_new_user(self, client):
        # 测试注册用户
        data = {
            'user_name': 'test1',
            'password': 'test password'
        }

        response = client.post('/api/register', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        test_user = User.query.filter_by(user_name='test1').first()
        db.session.delete(test_user)
        db.session.commit()

    def test_change_password(self, client):
        """测试修改密码"""
        data = {
            'user_name': 'test1',
            'password': 'test password'
        }
        response = client.post('/api/register', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        test_user = User.query.filter_by(user_name='test1').first()
        change_password_date = {
            'user_id': test_user.user_id,
            'new_password': 'new test password'
        }
        response = client.post('/api/change_password', json=change_password_date)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        db.session.delete(test_user)
        db.session.commit()

    def test_get_no_record(self, client):
        # 测试获取评分记录
        data = {
            'user_name': 'test1',  # 不存在的用户ID
            'password': 'test password'
        }
        response = client.post('/api/register', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        test_user = User.query.filter_by(user_name='test1').first()
        response = client.post('/api/get_record', json={'user_id': test_user.user_id})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        db.session.delete(test_user)
        db.session.commit()

    def test_get_record_success(self, client):
        test_user = UserJudge.query.first()
        response = client.post('/api/get_record', json={'user_id': test_user.user_id})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True


class TestRating:
    def test_rating_add_none(self, client):
        response = client.post('/api/judge', json=None)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_rating_add_no_rating(self, client):
        response = client.post('/api/judge', json={'user_id': 1, 'movie_id': 2})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_rating_add_null(self, client):
        response = client.post('/api/judge', json={'user_id': 1, 'movie_id': 2, 'rating': ' '})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_rating_add_wrong_type(self, client):
        response = client.post('/api/judge', json={'user_id': 1, 'movie_id': 2, 'rating': 'wrong type'})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_rating_add_no_user(self, client):
        test_user = User(user_name='123', password='testpass')
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_user_id = test_user.user_id
        db.session.delete(test_user)
        db.session.commit()
        response = client.post('/api/judge', json={'user_id': test_user_id, 'movie_id': 2, 'rating': 3})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_rating_add_wrong_rating(self, client):
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_user_id = test_user.user_id
        test_movie = Movie(movie_name='test', release_year=1999)
        db.session.add(test_movie)
        db.session.commit()
        test_movie_id = test_movie.movie_id
        response = client.post('/api/judge', json={'user_id': test_user_id, 'movie_id': test_movie_id, 'rating': 2.1})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False
        db.session.delete(test_user)
        db.session.delete(test_movie)
        db.session.commit()

    def test_rating_add_out_of_range(self, client):
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_user_id = test_user.user_id
        test_movie = Movie(movie_name='test', release_year=1999)
        db.session.add(test_movie)
        db.session.commit()
        test_movie_id = test_movie.movie_id
        response = client.post('/api/judge', json={'user_id': test_user_id, 'movie_id': test_movie_id, 'rating': -1})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False
        db.session.delete(test_user)
        db.session.delete(test_movie)
        db.session.commit()

    def test_rating_add_success(self, client):
        test_user_1 = User(user_name='123', password='testpass')
        test_user_2 = User(user_name='123', password='pass')
        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.commit()
        test_user_id_1 = test_user_1.user_id
        test_user_id_2 = test_user_2.user_id
        test_movie = Movie(movie_name='test', release_year=1999)
        db.session.add(test_movie)
        db.session.commit()
        test_movie_id = test_movie.movie_id
        response = client.post('/api/judge', json={'user_id': test_user_id_1, 'movie_id': test_movie_id, 'rating': 2})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        response = client.post('/api/judge', json={'user_id': test_user_id_2, 'movie_id': test_movie_id, 'rating': 3})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        response = client.post('/api/judge', json = {'user_id': test_user_id_1, 'movie_id': test_movie_id, 'rating': 4})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        test_rating_1 = UserJudge.query.filter_by(user_id=test_user_id_1, movie_id=test_movie_id).first()
        test_rating_2 = UserJudge.query.filter_by(user_id=test_user_id_2, movie_id=test_movie_id).first()
        db.session.delete(test_rating_1)
        db.session.delete(test_rating_2)
        db.session.commit()
        db.session.delete(test_user_1)
        db.session.delete(test_user_2)
        db.session.delete(test_movie)
        db.session.commit()

    def test_delete_judge(self, client):
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_movie = Movie.query.first()
        response = client.post('/api/judge', json={'user_id': test_user.user_id, 'movie_id': test_movie.movie_id, 'rating': 2})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        response = client.post('/api/delete_judge', json = {'user_id': test_user.user_id, 'movie_id': test_movie.movie_id})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        db.session.delete(test_user)
        db.session.commit()

"""class TestRecommend:

    def test_cold_success_recommend(self, client):
        test_user = User(user_name='123', password='123')
        db.session.add(test_user)
        db.session.commit()
        response = client.post('/api/recommend', json={'user_id': test_user.user_id, 'record_times': 1})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        db.session.delete(test_user)
        db.session.commit()

    def test_success_recommend(self, client):
        test_user = UserJudge.query.first()
        like = ['War', 'Horror']
        response = client.post('/api/like', json={'user_id': test_user.user_id, 'like': like})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        response = client.post('/api/recommend', json={'user_id': test_user.user_id, 'record_times': 0})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        UserFavoriteGenres.query.filter_by(user_id=test_user.user_id).delete()
        db.session.commit()"""

class Testlike:

    def test_like_no_like(self, client):
        # 测试没有爱好的情况
        test_user = User(user_name='123', password='123')
        db.session.add(test_user)
        db.session.commit()
        test_user_id = test_user.user_id
        like = []
        response = client.post('/api/like', json={'user_id': test_user_id, 'like': like})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        db.session.delete(test_user)
        db.session.commit()

    def test_like_add_like(self, client):
        # 测试增删改查爱好的情况
        test_user = User(user_name='123', password='123')
        db.session.add(test_user)
        db.session.commit()
        test_user_id = test_user.user_id
        like = ['War', 'Horror']
        response = client.post('/api/like_query', json={'user_id': test_user_id})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        response = client.post('/api/like', json={'user_id': test_user_id, 'like': like})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        response = client.post('/api/like_query', json={'user_id': test_user_id})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        response = client.post('/api/like', json={'user_id': test_user_id, 'like': ['Thriller']})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 201
        assert response.get_json()['success'] == True
        response = client.post('/api/like_query', json={'user_id': test_user_id})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
        UserFavoriteGenres.query.filter_by(user_id=test_user_id).delete()
        db.session.commit()
        db.session.delete(test_user)
        db.session.commit()

"""class TestMovie:
    def test_get_movie(self, client):
        test_movie = Movie.query.first()
        responses = client.post('/api/get_movie', json={'movie_id': test_movie.movie_id})
        print(f"Response status: {responses.status_code}")
        print(f"Response JSON: {responses.get_json()}")
        assert responses.status_code == 200
        assert responses.get_json()['success'] == True"""
