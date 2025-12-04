# 后端部署方法

1. 安装依赖：pip install -r requirements.txt
2. 启动本地数据库服务后，用table_build.sql创建数据库
3. 新建.env文件 参考.env.example文件格式
4. 运行databasepart/data_download&import.py导入数据
5. 运行add_index.sql文件实现索引插入和数据初始化
6. 运行databasepart/compute_item_sim.py计算相似度矩阵，然后可以使用recommend.recommend_by_user_id函数进行推荐
7. 运行back_end.py启动后端服务
8. 在命令行进入项目的Frontend/SElab下执行命令npm run dev。即可查看到前端的端口，使用ctrl+左键点击后即可开始使用
