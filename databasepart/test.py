import pytest
from back_end import app, db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = True  # 启用调试模式
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://violet:s131601@localhost/soft_ware_engineering'

    with app.test_client() as client:
        with app.app_context():
            yield client

class TestLoginWithMySQL:

    def test_login_no_data(self, client):
        response = client.post('/api/login', json=None)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_no_dict(self, client):
        response = client.post('/api/login', json=123)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_no_user_id(self, client):
        response = client.post('/api/login', json={'password': 'testpass'})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_no_password(self, client):
        response = client.post('/api/login', json={'user_id': '123'})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_all_blank(self, client):
        response = client.post('/api/login', json={'user_id': '   ', 'password': '  '})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_user_id_type(self, client):
        response = client.post('/api/login', json={'user_id': 'abc', 'password': '123'})
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 400
        assert response.get_json()['success'] == False

    def test_login_user_not_exist(self, client):
        test_user = User(user_name='123', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        test_id = test_user.user_id
        db.session.delete(test_user)
        db.session.commit()
        """测试用户不存在的情况"""
        data = {
            'user_id': test_id,  # 不存在的用户ID
            'password': 'testpass'
        }

        response = client.post('/api/login', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 401
        assert response.get_json()['success'] == False

    def test_successful_login(self, client):
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



