# 前端部署
1. 首先git pull获取最新源码
2. 安装前端依赖
```shell
    # 在Frontend/SElab 目录下
    npm install
```
3. 运行开发服务器，命令行中会显示前端页面的链接
+ 不连接后端，用MSW拦截请求做前端独立测试
```shell
    # 在Frontend/SElab 目录下
    npm run dev
```
+ 连接后端测试
    + 修改Frontend\SElab\.env.development
    令环境变量`VITE_APP_MSW_ENABLED=false`
    + 然后在Frontend/SElab 目录下使用`npm run dev`命令运行前端
**注意**：
+ 修改环境变量后再次运行前端，配置**不会**自动恢复
+ 检查Frontend\SElab\.env.development中VITE_APP_BACKEND_URL变量对应端口，要和后端端口一致
