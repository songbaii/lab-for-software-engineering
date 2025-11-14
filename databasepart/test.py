import pytest
from back_end import app, db
from models import User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://violet:s131601@localhost/soft_ware_engineering'

    with app.test_client() as client:
        with app.app_context():
            # 开始事务
            connection = db.engine.connect()
            transaction = connection.begin()

            # 绑定会话到当前事务
            db.session = db.create_scoped_session(options={'bind': connection})

            # 创建表（如果不存在）,如果存在的话也不会影响，所以无需担心
            db.create_all()

            # 插入测试数据
            test_user = User(username=123, password='testpass')
            db.session.add(test_user)
            db.session.commit()  # 这个提交在事务内

            yield client

            # 测试结束后回滚，不保存数据
            transaction.rollback()
            connection.close()


class TestLoginWithMySQL:
    def test_successful_login(self, client):
        """测试成功登录 - 使用真实MySQL"""
        data = {
            'username': 123,
            'password': 'testpass'
        }

        response = client.post('/api/login', json=data)
        assert response.status_code == 200
        assert response.get_json()['success'] == True

    def test_user_creation_persists_in_transaction(self, client):
        """测试在事务内创建用户"""
        # 这个测试可以验证数据库操作
        with app.app_context():
            user = User.query.filter_by(username=123).first()
            assert user is not None
            assert user.check_password('testpass')