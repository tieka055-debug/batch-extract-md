---
name: biji-archive
description: Export the user’s authorised Get笔记 knowledge-base notes into Markdown through a persistent local Chrome profile.
---

# Biji Archive

Use this skill when the user asks to export, archive, or back up a Get笔记 / biji.com knowledge base they can access.

## First use

Run the command below with the full knowledge-base URL. A separate Chrome window opens; ask the user to complete login in that window. The profile is retained for future exports.

```bash
{{CLI_COMMAND}} "https://www.biji.com/subject/TARGET/DEFAULT?followId=TARGET&followName=NAME"
```

## Output

Read the JSON result. Return the `output_dir` as the saved result. Do not expose browser-profile files or credentials.

## Useful options

- `--output /ABSOLUTE/OUTPUT/DIRECTORY` chooses the export root.
- `--max 10` runs a small verification export before a complete archive.
- `--profile /ABSOLUTE/PROFILE/DIRECTORY` uses a dedicated login profile.
