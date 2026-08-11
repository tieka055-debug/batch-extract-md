# Biji Archive

一个本地运行的 Get笔记知识库归档工具：在独立 Chrome 中登录后，把自己可访问的知识库内容导出为 Markdown。

## 已实现

- SPA 页面跳转后的正文提取与 Markdown 文件保存
- 独立、持久化 Chrome 登录配置，不读取日常浏览器资料
- 终端 CLI：结果以 JSON 输出，便于 Agent 稳定调用
- 简洁桌面 GUI：填写 URL、选择目录、查看完成状态
- 内置 Agent Skill：一条命令安装到 Codex 或 Claude Code
- GitHub Actions 的基础语法与单元测试检查

## 安装

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/biji-archive.git
cd biji-archive
python -m venv .venv
. .venv/bin/activate
pip install -e .
playwright install chromium
```

## 导出

```bash
biji-archive export-url "https://www.biji.com/subject/TARGET/DEFAULT?followId=TARGET&followName=NAME"
```

首次执行会打开独立 Chrome。请在该窗口中登录，脚本随后会继续导出；文件默认写入 `exports/`。

小范围验证：

```bash
biji-archive export-url "URL" --max 3
```

桌面版：

```bash
python -m biji_archive.gui
```

## 安装 Agent Skill

```bash
biji-archive install-skill --agent codex
# 或
biji-archive install-skill --agent claude
```

安装完成后，可直接对 Agent 说：

> 导出这个 Get笔记知识库：URL

## 开源发布清单

1. 将 README 中的 `YOUR_GITHUB_USERNAME` 改成你的账号。
2. 创建 GitHub 仓库 `biji-archive`，并推送当前分支。
3. 在自己的 macOS 和 Windows 设备上各做一次登录、3 篇试导出和全量导出验证。
4. 通过后创建 `v0.1.0` Release。

## 许可证

MIT
