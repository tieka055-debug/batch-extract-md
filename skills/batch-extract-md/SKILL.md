---
name: batch-extract-md
description: 批量提取文案md：将用户有权访问的 Get笔记知识库文章导出为 Markdown，并返回输出目录。
---

# 批量提取文案md

当用户要求批量提取、备份、整理 Get笔记 / biji.com 知识库文案时使用本 Skill。

## 你需要向用户确认的输入

- 完整知识库 URL，例如 `https://www.biji.com/subject/TARGET/DEFAULT?followId=TARGET&followName=NAME`。
- 可选的输出目录；默认写入当前目录的 `exports/`。
- 可选的试运行篇数；建议先用 `--max 3` 验证登录和页面结构。

## 执行方式

```bash
{{CLI_COMMAND}} "https://www.biji.com/subject/TARGET/DEFAULT?followId=TARGET&followName=NAME"
```

首次执行会打开独立 Chrome。请提示用户在该窗口中完成 biji 登录；登录信息保存在独立 profile 中，不读取日常 Chrome 的资料。登录完成后工具会逐篇点击列表、打开原文、抓取标题和正文，并写入 Markdown。

## 常用参数

```bash
# 先提取 3 篇做验证
{{CLI_COMMAND}} "URL" --max 3

# 指定输出根目录
{{CLI_COMMAND}} "URL" --output "/ABSOLUTE/OUTPUT/DIRECTORY"

# 指定独立登录 profile
{{CLI_COMMAND}} "URL" --profile "/ABSOLUTE/PROFILE/DIRECTORY"
```

## 返回结果

CLI 标准输出是 JSON。读取 `ok`、`exported` 和 `output_dir` 字段，并把 `output_dir` 返回给用户。不要输出浏览器 profile、Cookie、Token 或调试信息。

## 失败处理

- 没有弹出浏览器：检查 Python、Playwright 浏览器内核和 Chrome 安装。
- 页面停在登录：让用户在独立窗口完成扫码/验证，不要替用户填写验证码。
- 列表选择器超时：先用 `--max 3` 重试，并保留失败日志供后续适配页面结构。
- 输出目录已存在：工具会保留已有文件，并为同名文件生成不冲突的文件名。
