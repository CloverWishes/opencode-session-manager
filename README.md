# OpenCode Session Manager

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()

**A simple tool to list and restore archived OpenCode chat sessions**

[English](#english) | [中文](#中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### Overview

OpenCode Session Manager is a lightweight Python tool that helps you manage your OpenCode chat sessions. When sessions are archived in OpenCode, they disappear from the sidebar. This tool allows you to:

- 📋 **List all sessions** - View both active and archived sessions
- 🔍 **Filter archived** - See only archived sessions
- 🔄 **Restore sessions** - Unarchive specific or all sessions
- 📦 **Archive sessions** - Archive sessions you don't need (optional)

### Installation

No installation required! Just download the script and run it with Python 3.7+.

```bash
# Clone or download the repository
git clone https://github.com/CloverWishes/opencode-session-manager.git
cd opencode-session-manager

# Run the tool
python opencode_session_manager.py
```

### Usage

#### Interactive Mode (Recommended)

Simply run the script without arguments for an interactive menu:

```bash
python opencode_session_manager.py
```

You'll see a menu like this:
```
============================================================
OpenCode Session Manager - Interactive Mode
============================================================

Select an option:
  1. List all sessions (active + archived)
  2. List archived sessions only
  3. Restore a specific session
  4. Restore all archived sessions
  5. Archive a specific session
  0. Exit
```

#### Command Line Mode

```bash
# List all sessions
python opencode_session_manager.py --list-all

# List only archived sessions
python opencode_session_manager.py --list-archived

# Restore a specific session
python opencode_session_manager.py --restore ses_xxx

# Restore all archived sessions
python opencode_session_manager.py --restore-all

# Specify custom database path (if needed)
python opencode_session_manager.py --db /path/to/opencode.db --list-all
```

### How It Works

OpenCode stores session data in a SQLite database at:
- **Linux/macOS**: `~/.local/share/opencode/opencode.db`
- **Windows**: `%USERPROFILE%\.local\share\opencode\opencode.db`

When a session is archived, OpenCode sets the `time_archived` field to a timestamp. This tool simply sets it back to `NULL` to restore the session.

### Requirements

- Python 3.7 or higher
- OpenCode desktop client (sessions must exist in the database)

### Safety

✅ **Read-only by default** - Listing sessions never modifies data  
✅ **Backup recommended** - The tool is safe, but backing up `opencode.db` before bulk operations is wise  
✅ **No external dependencies** - Uses only Python standard library

---

<a name="中文"></a>
## 🇨🇳 中文

### 简介

OpenCode Session Manager 是一个轻量级 Python 工具，帮助你管理 OpenCode 的聊天会话。当会话在 OpenCode 中被归档后，它们会从侧边栏消失。这个工具可以帮助你：

- 📋 **列出所有会话** - 查看活跃和已归档的会话
- 🔍 **筛选已归档** - 只查看已归档的会话
- 🔄 **恢复会话** - 取消归档特定或所有会话
- 📦 **归档会话** - 归档不需要的会话（可选功能）

### 安装

无需安装！只需下载脚本并用 Python 3.7+ 运行即可。

```bash
# 克隆或下载仓库
git clone https://github.com/CloverWishes/opencode-session-manager.git
cd opencode-session-manager

# 运行工具
python opencode_session_manager.py
```

### 使用方法

#### 交互模式（推荐）

直接运行脚本，无需参数，会显示交互式菜单：

```bash
python opencode_session_manager.py
```

你会看到如下菜单：
```
============================================================
OpenCode Session Manager - Interactive Mode
============================================================

Select an option:
  1. List all sessions (active + archived)
  2. List archived sessions only
  3. Restore a specific session
  4. Restore all archived sessions
  5. Archive a specific session
  0. Exit
```

#### 命令行模式

```bash
# 列出所有会话
python opencode_session_manager.py --list-all

# 只列出已归档的会话
python opencode_session_manager.py --list-archived

# 恢复指定会话
python opencode_session_manager.py --restore ses_xxx

# 恢复所有已归档会话
python opencode_session_manager.py --restore-all

# 指定自定义数据库路径（如有需要）
python opencode_session_manager.py --db /path/to/opencode.db --list-all
```

### 工作原理

OpenCode 会将会话数据存储在 SQLite 数据库中：
- **Linux/macOS**: `~/.local/share/opencode/opencode.db`
- **Windows**: `%USERPROFILE%\.local\share\opencode\opencode.db`

当会话被归档时，OpenCode 会将 `time_archived` 字段设置为时间戳。这个工具只是将其重新设置为 `NULL` 来恢复会话。

### 系统要求

- Python 3.7 或更高版本
- OpenCode 桌面客户端（数据库中必须存在会话）

### 安全性

✅ **默认只读** - 列出会话不会修改任何数据  
✅ **建议备份** - 工具本身是安全的，但批量操作前备份 `opencode.db` 是明智的  
✅ **无外部依赖** - 仅使用 Python 标准库

---

## Example Output / 示例输出

```
====================================================================================================
Found 6 session(s):
====================================================================================================

[1] Active
    ID:       ses_0fe011b31ffe40VqSCykMJktK4
    Title:    Restore archived OpenCode chat sessions
    Created:  2026-06-26 11:35:09
    Updated:  2026-06-26 11:50:17

[2] Archived
    ID:       ses_0fe10c08fffe8Dfuw4e9eHBjrT
    Title:    OpenCode会话归档查看与恢复
    Created:  2026-06-26 11:18:04
    Archived: 2026-06-26 11:18:19
```

---

## License / 许可证

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing / 贡献

Contributions are welcome! Feel free to submit issues or pull requests.

欢迎贡献！请随时提交 issue 或 pull request。

## Acknowledgments / 致谢

- Created for the OpenCode community
- Thanks to all contributors and users
