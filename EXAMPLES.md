# Usage Examples / 使用示例

## Quick Start / 快速开始

### 1. List All Sessions / 查看所有会话

```bash
$ python opencode_session_manager.py --list-all

====================================================================================================
Found 6 session(s):
====================================================================================================

[1] Active
    ID:       ses_0fe011b31ffe40VqSCykMJktK4
    Title:    Project Discussion
    Created:  2026-06-26 11:35:09
    Updated:  2026-06-26 11:50:17

[2] Archived
    ID:       ses_0fe10c08fffe8Dfuw4e9eHBjrT
    Title:    Bug Fix Session
    Created:  2026-06-26 11:18:04
    Archived: 2026-06-26 11:18:19
```

### 2. List Archived Only / 只查看已归档

```bash
$ python opencode_session_manager.py --list-archived

=== Archived Sessions ===

[1] Archived
    ID:       ses_0fe10c08fffe8Dfuw4e9eHBjrT
    Title:    Bug Fix Session
    Created:  2026-06-26 11:18:04
    Archived: 2026-06-26 11:18:19
```

### 3. Restore Specific Session / 恢复指定会话

```bash
$ python opencode_session_manager.py --restore ses_0fe10c08fffe8Dfuw4e9eHBjrT

✓ Successfully restored session: Bug Fix Session
```

### 4. Restore All / 恢复所有

```bash
$ python opencode_session_manager.py --restore-all

✓ Successfully restored 3 session(s):
  - Bug Fix Session
  - Code Review
  - Documentation Update
```

### 5. Interactive Mode / 交互模式

```bash
$ python opencode_session_manager.py

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

Enter option (0-5): 4

Restore all archived sessions? (y/N): y

✓ Successfully restored 3 session(s):
  - Bug Fix Session
  - Code Review
  - Documentation Update
```

---

## Common Workflows / 常见工作流程

### Workflow 1: Find and Restore / 查找并恢复

```bash
# Step 1: Find the session you want to restore
python opencode_session_manager.py --list-archived

# Step 2: Copy the session ID and restore it
python opencode_session_manager.py --restore ses_xxx
```

### Workflow 2: Bulk Restore / 批量恢复

```bash
# Restore all archived sessions at once
python opencode_session_manager.py --restore-all
```

### Workflow 3: Custom Database Path / 自定义数据库路径

```bash
# If your database is in a non-standard location
python opencode_session_manager.py \
  --db /custom/path/opencode.db \
  --list-all
```

---

## Database Locations / 数据库位置

### Linux / macOS
```
~/.local/share/opencode/opencode.db
```

### Windows
```
%USERPROFILE%\.local\share\opencode\opencode.db
# Usually: C:\Users\<Username>\.local\share\opencode\opencode.db
```

---

## Safety Tips / 安全提示

⚠️ **Always backup before bulk operations**

```bash
# Create a backup
cp ~/.local/share/opencode/opencode.db ~/.local/share/opencode/opencode.db.backup

# Now it's safe to run restore-all
python opencode_session_manager.py --restore-all
```

✅ **The tool is read-only by default**  
Listing sessions (`--list-all`, `--list-archived`) never modifies your data.
