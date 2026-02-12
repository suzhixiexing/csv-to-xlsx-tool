# CSV转XLSX工具部署方案

## 项目概述

这是一个基于Python + Flask + Pandas的CSV转XLSX在线工具，提供以下功能：
- 上传CSV文件
- 自动转换为XLSX格式
- 下载转换后的文件
- 文件处理完成后自动删除，保护隐私

## 部署方案

### 方案1：使用Vercel部署（推荐）

**优点**：
- 免费套餐足够使用
- 部署简单，支持自动构建
- 全球CDN加速
- 自动HTTPS

**步骤**：
1. **准备项目**：
   - 在项目根目录创建 `vercel.json` 文件
   - 创建 `api/index.py` 文件作为Vercel入口

2. **创建vercel.json**：
   ```json
   {
     "builds": [
       {
         "src": "api/index.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "api/index.py"
       }
     ]
   }
   ```

3. **创建api/index.py**：
   ```python
   from app import app
   
   # Vercel入口点
   def handler(event, context):
       return app(event, context)
   ```

4. **部署到Vercel**：
   - 访问 https://vercel.com/
   - 登录并连接GitHub
   - 导入项目仓库
   - 按照提示完成部署

### 方案2：使用Heroku部署

**优点**：
- 免费套餐可用
- 支持自定义域名
- 成熟的云平台

**步骤**：
1. **准备项目**：
   - 创建 `Procfile` 文件
   - 创建 `requirements.txt` 文件（已存在）

2. **创建Procfile**：
   ```
   web: gunicorn app:app
   ```

3. **添加gunicorn依赖**：
   ```bash
   pip3 install gunicorn
   pip3 freeze > requirements.txt
   ```

4. **部署到Heroku**：
   - 访问 https://www.heroku.com/
   - 登录并创建新应用
   - 按照提示部署代码

### 方案3：使用AWS EC2部署

**优点**：
- 完全控制服务器
- 可扩展性强
- 适合高流量场景

**步骤**：
1. **创建EC2实例**：
   - 选择Ubuntu 20.04 LTS
   - 配置安全组，开放80端口

2. **配置服务器**：
   ```bash
   # 连接服务器后执行
   sudo apt update
   sudo apt install python3-pip python3-venv nginx gunicorn
   
   # 克隆项目
   git clone <项目仓库>
   cd csv-to-xlsx
   
   # 创建虚拟环境
   python3 -m venv venv
   source venv/bin/activate
   
   # 安装依赖
   pip install -r requirements.txt
   
   # 配置Gunicorn服务
   sudo nano /etc/systemd/system/csv-to-xlsx.service
   ```

3. **配置Gunicorn服务**：
   ```ini
   [Unit]
   Description=CSV to XLSX Converter
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/csv-to-xlsx
   ExecStart=/home/ubuntu/csv-to-xlsx/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **启动服务**：
   ```bash
   sudo systemctl start csv-to-xlsx
   sudo systemctl enable csv-to-xlsx
   ```

5. **配置Nginx**：
   ```bash
   sudo nano /etc/nginx/sites-available/csv-to-xlsx
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   ```bash
   sudo ln -s /etc/nginx/sites-available/csv-to-xlsx /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## 长期维护建议

1. **定期更新依赖**：
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **监控服务状态**：
   - 使用云服务提供商的监控工具
   - 设置错误告警

3. **备份代码**：
   - 使用Git版本控制
   - 定期推送代码到远程仓库

4. **安全更新**：
   - 定期更新服务器系统
   - 更新依赖包以修复安全漏洞

5. **性能优化**：
   - 对于大型CSV文件，考虑增加服务器内存
   - 配置适当的超时设置

## 访问链接

部署完成后，你将获得一个公网访问地址，例如：
- Vercel: https://csv-to-xlsx-tool.vercel.app
- Heroku: https://csv-to-xlsx-tool.herokuapp.com
- AWS: https://your-domain.com

## 故障排查

### 常见问题

1. **文件上传失败**：
   - 检查文件大小是否超过限制（默认16MB）
   - 检查网络连接

2. **转换失败**：
   - 检查CSV文件格式是否正确
   - 查看服务器日志获取详细错误信息

3. **服务无法访问**：
   - 检查服务器是否运行
   - 检查防火墙设置
   - 检查域名解析是否正确

### 查看日志

- **Vercel**：在Vercel控制台查看部署日志
- **Heroku**：使用 `heroku logs --tail` 命令
- **AWS**：使用 `sudo journalctl -u csv-to-xlsx` 命令

## 总结

推荐使用Vercel部署方案，因为它：
- 部署最简单
- 无需维护服务器
- 免费且稳定
- 提供全球访问能力

通过以上部署方案，你的CSV转XLSX工具将可以：
- 不受局域网限制，全球可访问
- 长期稳定运行
- 自动HTTPS保护
- 快速响应转换请求