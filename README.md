# 每日新闻摘要机器人

## 项目说明
每天自动抓取过去24小时的以下领域重点新闻，通过 AI 提炼核心要点，推送到微信：

- 🔬 **科技·科学·商业**：科技、科学、商业领域重要进展
- ⚔️ **伊朗·中东局势**：伊朗及中东地区战争、地缘政治最新动态

## 新闻分类
机器人会智能分类并以不同样式呈现：
- 科技商业新闻（蓝色主题）
- 中东战争新闻（红色主题）

## 环境要求
- Python 3.9+

## 本地运行
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
# Windows (PowerShell)
$env:SERPER_API_KEY="your-serper-key"
$env:OPENAI_API_KEY="your-openai-key"
$env:WXPUSHER_APP_TOKEN="your-wxpusher-token"

# 3. 运行
python main.py
```

## 部署到 GitHub Actions
1. 将代码推送到 GitHub 仓库
2. 在 Settings > Secrets and variables > Actions 中添加：
   - SERPER_API_KEY
   - OPENAI_API_KEY  
   - WXPUSHER_APP_TOKEN
3. 定时任务会自动在每天 9:00 运行
