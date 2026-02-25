# API 注册指南

## 1. Serper.dev 注册（已完成 ✅）

如果您已完成注册，请忽略此部分。如果您还需要注册：

1. 访问 https://serper.dev
2. 使用 Google 账号登录
3. 在 Dashboard 获取 API Key
4. **免费额度**：每月 2500 次搜索

---

## 2. WxPusher 配置（已完成 ✅）

您已提供 UID: `UID_9k7qT5ksr3aZwlLV4hzCLCsumpxx`

如果您还需要获取 AppToken：
1. 访问 https://wxpusher.zjiecode.com/admin/
2. 登录后点击「创建应用」
3. 填写应用名称（如：每日早报）
4. **创建后立即复制 AppToken**（只显示一次！）

---

## 3. OpenAI API Key 获取指南 🔑

您有 ChatGPT 账号，可以直接获取 OpenAI API Key：

### 步骤 1：访问 OpenAI 平台
打开 https://platform.openai.com/

### 步骤 2：登录账号
点击「Log in」，使用您的 ChatGPT 账号登录

### 步骤 3：创建 API Key
1. 登录后，点击左侧菜单 **API keys**
2. 点击 **Create new secret key**
3. 给 key 命名（如：daily-news-bot）
4. **立即复制**生成的 key（格式：sk-xxxx...）
5. **注意**：key 只显示一次，请立即保存！

### 步骤 4：查看免费额度
- 新用户通常有 $5-$18 的免费额度
- 每次新闻摘要消耗约 $0.01-$0.03
- 免费额度可用几个月

### ⚠️ 重要提示
- 不要在代码中直接写死 API Key
- API Key 只用于 GitHub Secrets 配置（见下文）

---

## 4. GitHub 仓库创建和配置指南 🚀

### 步骤 1：创建 GitHub 仓库
1. 登录 GitHub：https://github.com
2. 点击右上角 **+** → **New repository**
3. 填写：
   - Repository name: `daily-news-bot`（或其他名称）
   - Description: 每日科技商业新闻摘要机器人
   - 选择 **Public** 或 **Private**
   - 勾选 **Add a README file**
4. 点击 **Create repository**

### 步骤 2：上传代码
在仓库页面：
1. 点击 **Upload files**
2. 将文件夹中的以下文件拖入：
   - `main.py`
   - `requirements.txt`
   - `README.md`
   - `.github/workflows/daily_news.yml`
3. 点击 **Commit changes**

### 步骤 3：配置 Secrets（重要！）
1. 在仓库页面，点击 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 逐个添加以下 4 个 secret：

| Secret Name | 值 | 说明 |
|------------|-----|------|
| `SERPER_API_KEY` | 您的 Serper API Key | 搜索新闻用 |
| `OPENAI_API_KEY` | 您的 OpenAI API Key | AI 总结用 |
| `WXPUSHER_APP_TOKEN` | 您的 WxPusher Token | 推送微信用 |
| `WXPUSHER_UID` | UID_9k7qT5ksr3aZwlLV4hzCLCsumpxx | 您的微信 UID |

### 步骤 4：测试运行
1. 在仓库页面，点击 **Actions** → **Daily News Digest**
2. 点击 **Run workflow** → **Run workflow**
3. 等待 1-2 分钟，检查是否成功
4. 成功后，您的微信应该收到推送消息！

---

## 📋 配置检查清单

在开始测试前，请确认您已准备好以下信息：

- [ ] Serper API Key（来自 serper.dev）
- [ ] OpenAI API Key（来自 platform.openai.com）
- [ ] WxPusher AppToken（来自 wxpusher.zjiecode.com）
- [ ] WxPusher UID：`UID_9k7qT5ksr3aZwlLV4hzCLCsumpxx`

全部配置完成后，请告诉我，我将帮您进行首次测试！
