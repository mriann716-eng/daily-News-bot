"""
每日科技商业新闻摘要机器人
每天自动抓取过去24小时的科技、科学、商业新闻，AI提炼核心要点，推送到微信
"""

import os
import sys
import json
import requests
import datetime
from typing import List, Dict

# 导入 OpenAI
try:
    from openai import OpenAI
except ImportError:
    print("请安装 openai 库: pip install openai")
    sys.exit(1)


# ==================== 配置区域 ====================
# 从环境变量获取配置
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WXPUSHER_APP_TOKEN = os.getenv("WXPUSHER_APP_TOKEN")
USER_UID = os.getenv("WXPUSHER_UID", "UID_9k7qT5ksr3aZwlLV4hzCLCsumpxx")

# 检查必要的环境变量
def check_config():
    """检查配置是否完整"""
    missing = []
    if not SERPER_API_KEY:
        missing.append("SERPER_API_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not WXPUSHER_APP_TOKEN:
        missing.append("WXPUSHER_APP_TOKEN")
    
    if missing:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing)}")
        print("请在环境变量中配置这些值")
        return False
    return True


# ==================== 新闻获取 ====================
def get_news_from_serper(keywords: str = "科技 商业 科学", num: int = 10) -> List[Dict]:
    """
    使用 Serper API 获取 Google 新闻搜索结果
    
    Args:
        keywords: 搜索关键词
        num: 获取新闻数量
    
    Returns:
        新闻列表
    """
    url = "https://google.serper.dev/search"
    
    # 搜索过去24小时的新闻
    payload = json.dumps({
        "q": keywords,
        "num": num,
        "tbs": "qdr:d",  # 过去24小时
        "gl": "cn",      # 中国
        "hl": "zh-cn"    # 中文
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"🔍 正在搜索新闻...")
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        news_list = []
        
        # 提取有机搜索结果
        for item in data.get('organic', [])[:num]:
            news_list.append({
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', ''),
                'source': item.get('source', ''),
                'date': item.get('date', '')
            })
        
        print(f"✅ 获取到 {len(news_list)} 条新闻")
        return news_list
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取新闻失败: {e}")
        return []


# ==================== AI 总结 ====================
def summarize_with_openai(news_list: List[Dict], max_items: int = 6) -> str:
    """
    使用 OpenAI API 提炼新闻核心要点
    
    Args:
        news_list: 原始新闻列表
        max_items: 最多处理几条新闻
    
    Returns:
        格式化后的新闻摘要 (HTML格式)
    """
    if not news_list:
        return "暂无新闻"
    
    # 只取前几条，避免超出 token 限制
    news_items = news_list[:max_items]
    
    # 构建新闻内容
    content_text = ""
    for idx, item in enumerate(news_items, 1):
        content_text += f"""
【新闻 {idx}】
标题：{item.get('title', '')}
来源：{item.get('source', '')}
摘要：{item.get('snippet', '')}
链接：{item.get('link', '')}
"""
    
    # 构建 Prompt
    prompt = f"""你是一位专业的科技和商业新闻分析师。请阅读以下过去24小时的重要新闻。

任务要求：
1. 筛选出最值得关注的 {max_items} 条科技、科学或商业新闻
2. 每条新闻提炼一个核心要点（不超过30字）
3. 必须保留原始新闻链接

输出格式（严格使用以下HTML格式）：
<div style="margin-bottom: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
    <strong style="color: #1a73e8;">📰 新闻标题</strong><br/>
    <span style="color: #666;">💡 核心要点</span><br/>
    <a href="链接" style="color: #1a73e8;">查看原文 →</a>
</div>

新闻数据：
{content_text}

请直接输出HTML内容，不要添加其他说明文字。"""

    try:
        print(f"🤖 正在使用 AI 提炼要点...")
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位专业的科技和商业新闻分析师，擅长提炼核心要点。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        summary = response.choices[0].message.content.strip()
        print(f"✅ AI 总结完成")
        return summary
        
    except Exception as e:
        print(f"❌ AI 总结失败: {e}")
        # 如果 AI 失败，返回简单格式的原始新闻
        fallback = ""
        for item in news_items[:5]:
            fallback += f"""
<div style="margin-bottom: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
    <strong style="color: #1a73e8;">📰 {item.get('title', '')}</strong><br/>
    <span style="color: #666;">💡 {item.get('snippet', '')}</span><br/>
    <a href="{item.get('link', '')}" style="color: #1a73e8;">查看原文 →</a>
</div>"""
        return fallback


# ==================== 微信推送 ====================
def push_to_wxpusher(content: str) -> bool:
    """
    使用 WxPusher 推送消息到微信
    
    Args:
        content: HTML 格式的内容
    
    Returns:
        是否推送成功
    """
    url = "https://wxpusher.zjiecode.com/api/send/message"
    
    # 构建消息数据
    data = {
        "appToken": WXPUSHER_APP_TOKEN,
        "content": content,
        "summary": f"📰 {datetime.date.today()} 每日科技简报",
        "contentType": 2,  # HTML 内容
        "uids": [USER_UID]
    }
    
    try:
        print(f"📱 正在推送消息到微信...")
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get('success'):
            print(f"✅ 推送成功！")
            return True
        else:
            print(f"❌ 推送失败: {result.get('msg', '未知错误')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 推送失败: {e}")
        return False


# ==================== 主函数 ====================
def main():
    """主函数"""
    print("=" * 50)
    print(f"🚀 每日新闻摘要机器人启动")
    print(f"📅 日期: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 检查配置
    if not check_config():
        sys.exit(1)
    
    # 2. 获取新闻
    news_list = get_news_from_serper(
        keywords="科技 商业 科学 重大新闻",
        num=10
    )
    
    if not news_list:
        print("❌ 未获取到新闻，尝试备用搜索...")
        # 备用搜索：英文关键词
        news_list = get_news_from_serper(
            keywords="technology business science breaking news",
            num=10
        )
    
    if not news_list:
        print("❌ 无法获取新闻，程序退出")
        sys.exit(1)
    
    # 3. AI 总结
    summary = summarize_with_openai(news_list, max_items=6)
    
    # 4. 构建完整消息
    today = datetime.date.today()
    full_content = f"""
<h2 style="color: #333; border-bottom: 2px solid #1a73e8; padding-bottom: 10px;">
    📊 {today} 每日科技商业简报
</h2>
<p style="color: #666; font-size: 14px;">
    过去24小时科技、科学、商业领域重点新闻
</p>
<br/>
{summary}
<br/><br/>
<p style="color: #999; font-size: 12px; text-align: center;">
    —— 由 AI 自动生成 ——
</p>
"""
    
    # 5. 推送
    success = push_to_wxpusher(full_content)
    
    if success:
        print("=" * 50)
        print("🎉 任务完成！请检查微信消息")
        print("=" * 50)
    else:
        print("=" * 50)
        print("❌ 任务失败，请检查配置")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
