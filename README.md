## 一、本地运行流程

### 1. 安装依赖
#### 1.1 Linux系统需要，Windows 和 MacOS 跳过

```bash
apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
``` 

#### 1.2 安装 pip 库

```bash
pip3 install -r requirements.txt
```

### 2. 运行 app
在终端输入以下代码，直接运行 app，默认端口为 80。关闭终端后，app 会停止运行。
```bash
streamlit run app.py --server.port=80
```

## 二、部署
### 1. 运行 app
在后台运行 app，并将输出重定向到 log.txt 文件中，关闭终端后，app 不会停止运行。
```bash
nohup streamlit run app.py --server.port=80 > log.txt 2>&1 &
```

### 2. 查看输出
```bash
tail -f log.txt
```

### 3. 查找并杀死进程
```bash

ps aux | grep streamlit
```
```bash

kill <pid>
```

### 4. 附录
- 完成了许可认证。
- 完成了计算结果的修改与保存。