import pytest
from back_end import app, db
from models import User

@pytest.fixture
def client_and_id():
    app.config['TESTING'] = True
    app.config['DEBUG'] = True  # 启用调试模式
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://violet:s131601@localhost/soft_ware_engineering'

    with app.test_client() as client:
        with app.app_context():
            # 创建表（如果不存在）
            db.create_all()

            # 插入测试数据 - user_name是VARCHAR，所以用字符串
            test_user = User(user_name='123', pass_word='testpass')
            db.session.add(test_user)
            db.session.commit()
            test_id = test_user.user_id
            yield client, test_id

            # 测试结束后清理数据
            User.query.filter_by(user_name='123').delete()
            db.session.commit()


class TestLoginWithMySQL:
    def test_successful_login(self, client_and_id):
        client, test_id = client_and_id
        """测试成功登录 - 使用真实MySQL"""
        data = {
            'user_id': test_id,  # user_name是VARCHAR，所以用字符串
            'password': 'testpass'
        }
        print(data)
        print("需要传递的json数据已经显示")
        response = client.post('/api/login', json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.get_json()}")
        assert response.status_code == 200
        assert response.get_json()['success'] == True
