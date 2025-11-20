# Claude CLI — Project Analyzer, Fixer & Code Generator  
*A powerful local terminal assistant powered by Anthropic Claude.*

This CLI exposes Claude as a **full development tool** capable of:

- One-shot Q&A  
- File fixing / refactoring / explaining  
- Project-wide analysis  
- Project Q&A  
- Project-aware file generation  
- Persistent chat mode  
- Live file attachments  
- Markdown-aware structured output  
- Always available from anywhere on your system  

All through a single command:

```
claude
```

---

#  Features

###  **Project Analyzer Mode**  
Scan an entire folder and get:

- High-level overview  
- Architecture summary  
- Module responsibilities  
- Detected bugs  
- Code smells  
- Security issues  
- Performance concerns  
- Refactoring guide  
- Suggested new features  
- ASCII architecture diagram  
- Quality rating (0–10)

---

###  **Project Q&A Mode**  
Ask Claude anything about a repo:

```bash
claude --project-qa <folder> "Where is the pathfinding implemented?"
```

Claude reads folder tree + truncated code and answers precisely.

---

###  **File Modes**  
Operate on individual files:

- `--fix file.py` — return corrected code only  
- `--explain file.py` — explain how the code works  
- `--refactor file.py` — rewrite with cleaner architecture  
- `-f file.py "question"` — ask questions about a file  

---

###  **Project-Aware Code Generation**
Generate new modules aligned with your existing codebase:

```bash
claude --generate-file "build a metadata parser" --out parser.py --project-root .
```

Claude adapts to your naming, architecture, and conventions.

---

###  **Chat Mode (persistent conversation)**

```bash
claude --chat
```

Commands inside chat:

```
/clear
/exit  /q  /quit
```

---

###  **One-shot prompts**

```bash
claude "explain BFS in simple terms"
```

---

#  Installation

### 1. Install the Anthropic SDK
```bash
py -m pip install anthropic
```

### 2. Set your API key
```bash
setx ANTHROPIC_API_KEY "your-key-here"
```

Reopen the terminal.

### 3. Save `claude_cli.py`
Place it anywhere (Desktop recommended).

### 4. Create `claude.bat`
Place in:

```
C:\Windows\claude.bat
```

With contents:

```bat
@echo off
py "%USERPROFILE%\Desktop\claude_cli.py" %*
```

Now the command `claude` works globally.

---

#  Command Grammar (Full Reference)

```
claude [GLOBAL_OPTIONS] [MODE] [MODE_ARGS] [prompt]
```

### GLOBAL OPTIONS:
```
--temperature <float>
--max-tokens <int>
```

---

## 🟦 Chat Mode
```
claude --chat
```

---

## 🟧 File Modes

### Fix a file
```
claude --fix <file>
```

### Explain a file
```
claude --explain <file>
```

### Refactor a file
```
claude --refactor <file>
```

### Attach a file to your question
```
claude -f <file> "question"
```

### Difference between two files
```
claude --diff old_file.py new_file.py
```

---

## 🟥 Project Modes

### Project Analyzer (full repo scan)
```
claude --analyze-folder <folder> [--focus "text"]
```

Examples:
```bash
claude --analyze-folder .
claude --analyze-folder src/ --focus "security"
```

### Project Q&A
```
claude --project-qa <folder> "question"
claude --project-qa <folder> --question "question"
```

### Fix Whole Folder
Fixes **every `.py` file** inside a project folder (recursively) and saves the corrected project into:
<folder>_fixed/

**Usage:**
```
claude --fix-folder <folder>
```

**Example:**
```
claude --fix-folder "D:\etf\hakatoni\rivian\rivian_ml"
```

### Refactor Whole Folder
Refactors **every `.py` file** inside a project folder (recursively), improving readability, structure, comments, and maintainability, while keeping **exact behavior**.  
Outputs to: <folder>_refactored/

**Usage:**
```
claude --refactor-folder <folder>
```

**Example:**
```
claude --refactor-folder "D:\etf\hakatoni\rivian\rivian_ml"
```

### Rewrite Whole Folder (Aggressive Architecture Rewrite)
This mode performs a **full architectural rewrite** of an entire Python project.  

Unlike `--fix-folder` (bug fixes) and `--refactor-folder` (safe cleanups with no behavior change),  
`--rewrite-folder` is a **high-level redesign tool**.

Note:  
`rewrite-folder` **does not guarantee backward compatibility**.  

### Usage
```
claude --rewrite-folder <folder>
```

### Example
```
claude --rewrite-folder "D:\etf\hakatoni\rivian\rivian_ml"
```

This will generate a completely modernized version of the project inside: rivian_ml_rewritten/

All folder structure is preserved, but each `.py` file receives a full architectural rewrite.

### Output
- Fully rewritten project into `<original>_rewritten/`
- Same folder structure, new code
- Deeply improved clarity, modularity, maintainability

---

## 🟩 File Generation Mode (project aware)
```
claude --generate-file "<spec>" --out <output_file> [--project-root <folder>]
```

Examples:
```bash
claude --generate-file "build a C++ engine class" --out engine.cpp
claude --generate-file "create FastAPI login system" --out auth.py --project-root .
```

---

## 🟨 One-shot Prompt (default)
```
claude "your prompt here"
```

---

#  Examples

### Analyze entire project:
```bash
claude --analyze-folder D:\Projects\RivianSense --focus "performance + architecture"
```

---

### Ask question about a project:
```bash
claude --project-qa . --question "Where is the main state machine implemented?"
```

---

### Fix a file:
```bash
claude --fix backend/server.py > backend/server_fixed.py
```

---

### Explain a file:
```bash
claude --explain ui/main_window.py
```

---

### Refactor a file:
```bash
claude --refactor core/engine.cpp > core/engine_refactored.cpp
```

---

### Ask about a file:
```bash
claude -f model.py "What is wrong with this training loop?"
```

---

### Generate new file based on repo structure:
```bash
claude --generate-file "Create a scene classifier class" --out scene_classifier.py --project-root .
```

---

### Chat:
```bash
claude --chat
```

---

# Internals / Dispatch Order

The CLI resolves modes in this order:

1. `--chat`  
2. `--analyze-folder`  
3. `--project-qa`  
4. `--generate-file`  
5. `--fix` / `--explain` / `--refactor` / `-f`  
6. One-shot mode  

---

# Configuration

Override the model globally:

```bash
setx CLAUDE_MODEL "claude-3-sonnet-20240229"
```

Or tweak per command:

```bash
claude --max-tokens 4000 "long output here"
```

---

#  Notes

- Binary files, images, videos, etc. are skipped automatically.  
- Large files are truncated safely to avoid token overload.  
- Project analysis is optimized for ~200–400 KB of readable context.  
- For deeper analysis, reduce folder size or use `--focus`.

---

