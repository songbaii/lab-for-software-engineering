# 后端部署方法

1. 安装依赖：pip install -r requirements.txt
2. 启动本地数据库服务后，用table_build.sql创建数据库
3. 新建.env文件 参考.env.example文件格式
4. 运行databasepart/data_download&import.py导入数据
5. 运行back_end.py启动后端服务
