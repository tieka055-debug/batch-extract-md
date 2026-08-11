# Biji Archive

将自己有权访问的 Get笔记知识库导出成 Markdown 的本地工具。

## 设计

- **浏览器渲染提取**：适配 SPA 跳转后的完整正文，避免依赖未公开接口。
- **独立持久登录配置**：首次在弹出的浏览器中登录；后续复用登录态。
- **机器可读 CLI**：结束时输出 JSON，方便 Codex、Claude Code 等 Agent 集成。
- **可演进架构**：后续增加 GUI、断点续传、API 适配器和多格式导出，而不耦合到页面选择器。

## 安装

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
playwright install chromium
```

## 使用

```bash
biji-archive "https://www.biji.com/subject/TARGET/DEFAULT?followId=TARGET&followName=NAME"
```

首次运行会打开浏览器，请在该窗口完成登录。导出结果默认保存在 `exports/`。

## 路线图

1. 完成真实页面选择器回归测试与断点续传。
2. 增加可选的 API 适配器、Token 刷新和知识库/博主选择器。
3. 提供桌面 GUI、Windows/macOS 打包和 GitHub Actions 发布。

## 致谢与许可

见 [NOTICE.md](NOTICE.md)。本项目采用 MIT 许可证。
