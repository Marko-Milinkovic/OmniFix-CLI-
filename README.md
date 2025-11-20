# OmniFix CLI — Project Analyzer, Fixer & Code Generator  
*A powerful local AI engineering tool powered by Anthropic Claude.*

OmniFix CLI turns Claude into a **full development assistant**, available directly from your terminal.  
It can fix files, refactor entire projects, analyze multi-file codebases, generate new modules, rewrite project architecture, and answer deep questions about your code — all via a single command:
```
claude
```

This tool is designed to function as a **local autonomous code engineer**, not just a chatbot.

---

## Table of Contents

- [General Properties of the Agent](#general-properties-of-the-agent)
  - [Multi-Mode Developer Agent](#multi-mode-developer-agent)
  - [Works on Entire Codebases, Not Just Files](#works-on-entire-codebases-not-just-files)
  - [Local, Safe, and Controlled](#local-safe-and-controlled)
  - [Multi-Language Capable](#multi-language-capable)
  - [Fast & Lightweight (Haiku Model)](#fast--lightweight-haiku-model)
  - [Deterministic and Repeatable](#deterministic-and-repeatable)
- [Why This Beats Cursor / Claude Web UI](#why-this-beats-cursor--claude-web-ui)
  - [What Claude CLI Can Do That Cursor Cannot](#what-claude-cli-can-do-that-cursor-cannot)
- [Features](#features)
  - [🟦 Project Analyzer Mode](#-project-analyzer-mode)
  - [🟧 Project Q&A Mode](#-project-qa-mode)
  - [🟨 File Modes](#-file-modes)
  - [🟥 Folder Modes](#-folder-modes)
  - [🟩 Project-Aware File Generation](#-project-aware-file-generation)
  - [🟪 Chat Mode](#-chat-mode)
  - [🟫 One-Shot Prompt](#-one-shot-prompt)
- [🚀 Chat Mode (Detailed)](#-chat-mode-detailed)
  - [Why Use Chat Mode?](#why-use-chat-mode)
  - [When NOT to Use Chat Mode](#when-not-to-use-chat-mode)
  - [Chat Mode vs Non-Chat Mode](#chat-mode-vs-non-chat-mode)
  - [The Rule of Thumb](#the-rule-of-thumb)
- [Installation](#installation)
- [ Top 10 OmniFix Superpowers](#-top-10-omnifix-superpowers)
- [ 50 OmniFix CLI Usage Examples](#-50-omnifix-cli-usage-examples)
  - [🟨🟫 1–10: One-Shot Prompts & File-Level Operations](#-110-one-shot-prompts--file-level-operations)
  - [🟦🟧🟩 11–20: Project-Wide Analysis & Q&A](#-1120-project-wide-analysis--qa)
  - [🟥 21–30: Full-Folder Fix, Refactor, Rewrite](#-2130-full-folder-fix-refactor-rewrite)
  - [31–40: Advanced Multi-Language Assistance](#-3140-advanced-multi-language-assistance)
  - [🚀 41–50: Chat Mode + Bonus Abilities](#-4150-chat-mode--bonus-abilities)
- [Internals / Dispatch Order](#internals--dispatch-order)
- [Notes](#notes)

---

# General Properties of the Agent

### **Multi-Mode Developer Agent**  
The OmniFix CLI switches between engineering roles depending on the mode you choose:

- Fixing engineer — `--fix`  
- Code reviewer — `--explain`  
- Refactoring specialist — `--refactor`  
- Principal architect — `--analyze-folder`  
- System designer — `--rewrite-folder`  
- Project consultant — `--project-qa`  
- File generator — `--generate-file`  
- Conversational assistant — `--chat`

---

### **Works on Entire Codebases, Not Just Files**  
The agent can:

- recursively scan your repo  
- rewrite every file  
- detect design flaws  
- produce architectural summaries  
- generate rebuilt folder structures  
- output full refactor & rewrite versions of projects

---

### **Local, Safe, and Controlled**  
- No files overwritten unless you choose via `--out`  
- Safe folder-wide operations:  
  - `<project>_fixed/`  
  - `<project>_refactored/`  
  - `<project>_rewritten/`  
- No execution of your code  
- No hidden memory or storing state  

---

### **Multi-Language Capable**  
Supports any text-based source file:

- Python  
- C++  
- Java / Kotlin  
- JavaScript / TypeScript  
- HTML / CSS  
- Rust  
- Go  
- C#  
- JSON / YAML / XML  

---

### **Fast & Lightweight (Haiku Model)**  
Using:
```
claude-3-haiku-20240307
```

Makes it:

- extremely fast  
- extremely cheap  
- ideal for rapid engineering  

---

### **Deterministic and Repeatable**  
In contrast to the Claude Web UI:

- no chat drift  
- no forgotten context  
- no hallucinated memory  

The OmniFix CLI uses clean deterministic prompts.

---

# Why This Beats Cursor / Claude Web UI

### **Cursor is interactive. OmniFix CLI is automated.**

Cursor requires:

- clicking through files  
- opening tabs  
- asking manually  

OmniFix CLI does:

- **entire folder scans automatically**  
- architectural rewrites  
- deterministic outputs  
- can run inside pipelines  
- works in PowerShell, CMD, Bash  
- requires **no editor**  
- works offline except for API  

---

## What Claude CLI Can Do That Cursor Cannot

| Feature | OmniFix CLI | Cursor |
|--------|------------|--------|
| Fix entire folder recursively | ✅ | ❌ |
| Refactor whole project | ✅ | ❌ |
| Rewrite architecture | ✅ | ❌ |
| Runs outside editor | ✅ | ❌ |
| Diff generation | ✅ | ❌ |
| Script automation | ✅ | ❌ |
| CI/CD support | ✅ | ❌ |
| Multi-language folder ops | ✅ | ⚠️ limited |
| Deterministic behavior | ✅ | ❌ |

---

# Features

## 🟦 Project Analyzer Mode
```
claude --analyze-folder <folder>
```

Returns:

- Architecture summary  
- Module responsibilities  
- Bug list  
- Performance issues  
- Security risks  
- Dead code  
- Refactoring roadmap  
- Quality rating (0–10)  
- ASCII architecture diagram  

---

## 🟧 Project Q&A Mode
```
claude --project-qa <folder> "Where is main state machine implemented?"
```

Claude loads:

- file list  
- truncated code  
- structure  

Then answers precisely.

---

## 🟨 File Modes

### Fix a file
```
claude --fix file.py
```

### Explain a file
```
claude --explain engine.cpp
```

### Refactor a file
```
claude --refactor utils.py
```

### Ask about a file
```
claude -f model.py "What is wrong with this training loop?"
```

### Show diff
```
claude --diff old.py new.py
```

---

## 🟥 Folder Modes

### Fix Entire Folder
```
claude --fix-folder <project>
```

Output: `<project>_fixed/`

---

### Refactor Entire Folder
```
claude --refactor-folder <project>
```

Output: `<project>_refactored/`

---

### Rewrite Entire Folder (Aggressive)
```
claude --rewrite-folder <project>
```

Claude is allowed to:

- reorganize modules  
- redesign architecture  
- add patterns  
- rename classes  
- remove bloat  
- split giant files  
- rebuild folder hierarchy  

Output: `<project>_rewritten/`

---

## 🟩 Project-Aware File Generation
```
claude --generate-file "create metadata loader" --out loader.py --project-root .
```

Claude adapts to your architecture.

---

## 🟪 Chat Mode
```
claude --chat
```

Commands:

- `/clear`  
- `/exit`  
- `/help`  

---

## 🟫 One-Shot Prompt
```
claude "explain CNN in simple terms"
```

---

# 🚀 Chat Mode (Detailed)

OmniFix CLI includes a persistent **Chat Mode**, turning Claude into an interactive terminal-native AI developer, similar to having a senior engineer working with you in real time.

You can start it with:
```bash
claude --chat
```

Once inside chat mode, you can converse naturally:
* ask questions
* request explanations
* iteratively refine code
* explore architectures
* fix bugs interactively
* attach files or project folders
* maintain an ongoing engineering session

Chat mode behaves more like an AI pair-programmer than a one-shot command execution tool.

---

## Why Use Chat Mode?

Chat mode is ideal when you want:

### 1. Iterative reasoning and long discussions

Example:
```
Explain the model architecture
Now rewrite it using a cleaner design
Now generate unit tests
Now integrate metadata parsing
```

Claude remembers context, improving output with each step.

### 2. Multi-step workflows

Chat allows back-and-forth tasks like:
* debugging + rewriting + testing
* designing system architecture
* exploring alternative implementations
* learning / teaching sessions

### 3. Project-aware memory

In chat mode you can attach files:
```
/file main.cpp
```

Or entire projects:
```
/project D:\MyGames\Engine\
```

Claude will remember these across messages.

### 4. Real-time AI engineering companion

Chat mode offers:
* persistent memory throughout conversation
* adaptive reasoning
* complex instructions broken into steps
* the ability to correct or refine outputs

This is something one-shot modes cannot do.

---

## When NOT to Use Chat Mode

Use normal modes instead of chat when you want:

**Deterministic file output**
```bash
claude --fix file.py
claude --refactor engine.cpp
```

**Full-project operations**
```bash
claude --fix-folder project/
claude --refactor-folder project/
claude --rewrite-folder project/
```

**One-shot, clean output**
```bash
claude --project-qa src/ "Where is inference done?"
```

---

## Chat Mode vs Non-Chat Mode

| Scenario | Best Mode |
|----------|-----------|
| Designing architecture | Chat |
| Debug conversation | Chat |
| Explain code file-by-file | Chat |
| Fix whole folder | Non-chat |
| Refactor one file | Non-chat |
| Generate new file | Non-chat |
| Project-wide Q&A | Non-chat |
| Simple questions | Non-chat |

---

## The Rule of Thumb

> **Use Chat Mode for thinking. Use standard modes for doing.**

---

# Installation

### 1. Install SDK
```
py -m pip install anthropic
```

### 2. Set API key
```
setx ANTHROPIC_API_KEY "your-key-here"
```

### 3. Save `claude_cli.py` anywhere (Desktop recommended)

### 4. Create launcher
`C:\Windows\claude.bat`
```bat
@echo off
py "%USERPROFILE%\Desktop\claude_cli.py" %*
```

Now run from anywhere:
```
claude
```

---

# Top 10 OmniFix Superpowers

## 1. Full-Folder Healing (Automatic Project-Wide Bug Fixer)

Run one command and OmniFix will recursively scan your entire project (Python, C++, Java, JS, Kotlin, Rust, Go, HTML, CSS…) and produce a fully fixed, cleaned, and safer version of your entire codebase.

**No IDE on Earth does that.**
```bash
claude --fix-folder myproject
```

---

## 2. Multi-Language AI Refactoring Engine

OmniFix intelligently rewrites and modernizes:
* **Python** → Type hints, cleaner architecture
* **C++** → RAII, smart pointers, const-correctness
* **Java** → OOP cleanup, package structure
* **Kotlin** → Idiomatic, null-safe, Android-ready
* **JS/TS** → Modern ES6+, modular, async improvements
```bash
claude --refactor file.cpp
```

It applies language-aware engineering best practices automatically.

---

## 3. Architectural Rewrite Mode (New Project Structure)

This is the **nuclear option**. A single command produces an entirely redesigned, modern architecture for your project.
```bash
claude --rewrite-folder legacy_app
```

You get a new clean codebase while preserving the same functional purpose.

---

## 4. Repository-Level AI Analysis

OmniFix generates a deep architecture report:
* Purpose of every file
* Dependency flow
* Detected bugs
* Security issues
* Dead code
* Style and OOP violations
* Refactor & improvement plan
* ASCII diagrams
* Quality score
```bash
claude --analyze-folder .
```

**Equivalent to a professional code audit.**

---

## 5. Diff Understanding Like a Senior Engineer

OmniFix doesn't just generate diffs. It **explains** them:
* What changed
* Why it changed
* Possible regressions
* Improvements
* Architectural insights
```bash
claude --diff old.cpp new.cpp
```

This is beyond `git diff` — it is **semantic diffing**.

---

## 6. Full Project Q&A (Codebase Genius Mode)

Ask OmniFix anything about your project, and it answers with context from the entire repository.
```bash
claude --project-qa src/ "Where is the rendering pipeline implemented?"
```

This creates **instant understanding** of new or inherited projects.

---

## 7. Contextual File/Module Generation

Generate new modules in perfect alignment with your project's architecture.
```bash
claude --generate-file "Create a scene detector class" --out detector.py --project-root .
```

The new file looks like it was written by the same engineering team.

---

## 8. OmniFix Chat Mode (Live Engineering Assistant)

Advanced REPL chat that supports attaching files and entire projects:
```bash
claude --chat
/file model.py
/project backend/
```

OmniFix becomes an interactive senior engineer inside your terminal.

---

## 9. Multi-File Thinking & Deep Context Integration

Attach unlimited files and entire project structures during Chat Mode, making OmniFix capable of:
* Multi-file debugging
* Understanding cross-file logic
* Tracing flows (e.g., controller → service → model)
* Answering architecture questions

This works better than typical LLM chat because you explicitly supply structured context.

---

## 10. Full Cross-Language Power

OmniFix is truly **polyglot**.

Supports fixing/refactor/rewrite for:
* Python
* C / C++
* Java
* Kotlin
* JavaScript / TypeScript
* Rust
* Go
* C#
* PHP
* HTML/CSS/XML/JSON/YAML

It expands Claude into a **universal engineering refactoring tool**.

---

# ✅ 50 OmniFix CLI Usage Examples
(command → effect)

---

## 🟨🟫 1–10: One-Shot Prompts & File-Level Operations

### 1. One-shot natural language answer
```bash
claude "explain BFS in simple terms"
```
→ One-shot natural language answer.

### 2. Attach file + ask a question
```bash
claude -f main.py "What is wrong with this function?"
```
→ Attaches file + asks a question.

### 3. Full file explanation
```bash
claude --explain server.py
```
→ Full explanation of server.py: purpose, flow, pitfalls.

### 4. Fix file to stdout
```bash
claude --fix dataset.py
```
→ Returns fixed version of dataset.py to stdout.

### 5. Fix file and save output
```bash
claude --fix dataset.py --out dataset_fixed.py
```
→ Saves corrected dataset to dataset_fixed.py.

### 6. Refactor file to stdout
```bash
claude --refactor model.py
```
→ Clean, readable, commented version of model.py.

### 7. Refactor C++ file and save
```bash
claude --refactor model.cpp --out model_refactored.cpp
```
→ Modernized C++17 refactor of a cpp file.

### 8. Semantic diff explanation
```bash
claude --diff old.cpp new.cpp
```
→ Unified diff + explanation.

### 9. Generate Python file from description
```bash
claude --generate-file "build a CNN class" --out cnn.py
```
→ Creates a new architecture-aware file.

### 10. Generate C++ header file
```bash
claude --generate-file "create a header-only C++ vector math library" --out math.hpp
```
→ Generates C++ code.

---

## 🟦🟧🟩 11–20: Project-Wide Analysis & Q&A

### 11. Full project analysis
```bash
claude --analyze-folder .
```
→ Full root project analysis.

### 12. Performance-focused analysis
```bash
claude --analyze-folder backend/ --focus "performance"
```
→ Architecture + performance review.

### 13. Project Q&A - find implementation
```bash
claude --project-qa src/ "Where is the main state machine implemented?"
```
→ Precise answer with file references.

### 14. Project Q&A - routing explanation
```bash
claude --project-qa app/ --question "How is routing handled?"
```
→ Responds with routing explanation.

### 15. Memory safety audit
```bash
claude --analyze-folder engine/ --focus "memory safety"
```
→ C++ RAII/memory-safety audit.

### 16. Project Q&A - AI logic flow
```bash
claude --project-qa mygame/ "Explain enemy AI decision flow"
```
→ Describes logic across files.

### 17. Security-focused analysis
```bash
claude --analyze-folder frontend/ --focus "security+auth"
```
→ Security-oriented review.

### 18. Project Q&A - database connection
```bash
claude --project-qa . "Where is database connection created?"
```
→ Gives filename, line ranges, and structure.

### 19. OOP design improvement plan
```bash
claude --analyze-folder . --focus "improve OOP design"
```
→ High-level architecture refactor plan.

### 20. Project Q&A - architecture suggestion
```bash
claude --project-qa src/ "Where should I add caching layer?"
```
→ Suggests design + placement.

---

## 🟥 21–30: Full-Folder Fix, Refactor, Rewrite

### 21. Fix entire project
```bash
claude --fix-folder myproject
```
→ Fixes ALL files → myproject_fixed/

### 22. Refactor entire backend
```bash
claude --refactor-folder backend
```
→ Refactors all code → backend_refactored/

### 23. Rewrite engine with new architecture
```bash
claude --rewrite-folder engine
```
→ Creates fully rewritten engine_rewritten/ with new architecture.

### 24. Fix C++ project
```bash
claude --fix-folder cpp_project
```
→ Fixes .cpp/.h files using C++17 best practices.

### 25. Modernize JavaScript project
```bash
claude --refactor-folder js_app
```
→ Modern ES6+ modularization across JS project.

### 26. Rewrite legacy Java project
```bash
claude --rewrite-folder legacy_java
```
→ Produces clean modern Java package structure.

### 27. Fix web project
```bash
claude --fix-folder web/
```
→ HTML/CSS/JS cleanup.

### 28. Refactor algorithms folder
```bash
claude --refactor-folder algorithms/
```
→ Refactors entire algorithms folder with comments.

### 29. Rewrite parser architecture
```bash
claude --rewrite-folder parser/
```
→ Rewrites parser into new architecture (e.g., classes, modules).

### 30. Fix PyTorch training code
```bash
claude --fix-folder pytorch_training
```
→ Fixes PyTorch issues: device handling, gradients, etc.

---

## 31–40: Advanced Multi-Language Assistance

### 31. Fix C++ file
```bash
claude --fix main.cpp
```
→ Patch memory bugs, UB, modern C++ cleanup.

### 32. Refactor Java file
```bash
claude --refactor Engine.java
```
→ Pure Java refactor, idiomatic naming, better OOP.

### 33. Fix JavaScript async issues
```bash
claude --fix script.js
```
→ Fixes race conditions + async flow.

### 34. Refactor HTML semantically
```bash
claude --refactor index.html
```
→ Semantic cleanup + structuring.

### 35. Rewrite React app
```bash
claude --rewrite-folder react_app
```
→ Fully rewritten modern React architecture.

### 36. Generate TypeScript types
```bash
claude --generate-file "TypeScript interface definitions for API" --out types.ts
```
→ Generates TS types.

### 37. Fix Go server code
```bash
claude --fix server.go
```
→ Idiomatic Go code cleanup.

### 38. Refactor Kotlin app
```bash
claude --refactor app.kt
```
→ Kotlin idiomatic refactor.

### 39. Clean up CSS
```bash
claude --fix styles.css
```
→ Cleans up CSS without altering layout.

### 40. Generate Rust module
```bash
claude --generate-file "Rust struct for telemetry parser" --out parser.rs
```
→ Creates Rust module.

---

## 🚀 41–50: Chat Mode + Bonus Abilities

### 41. Start chat mode
```bash
claude --chat
```
→ Start full REPL chat session.

### 42. Attach file in chat
Inside chat:
```
/file model.py
```
→ Attaches model.py into the chat context.

### 43. Load project in chat
Inside chat:
```
/project D:\Projects\Engine
```
→ Loads project tree into memory.

### 44. Multi-step architecture redesign
Inside chat:
```
Explain the architecture and redesign it
```
→ Multi-step reasoning with Claude remembering context.

### 45. Localized modern C++ rewrite
Inside chat:
```
Rewrite only this function into modern C++
```
→ Precise localized rewrites.

### 46. Iterative debugging session
Inside chat:
```
Help me debug this training loop
```
→ Iterative debugging with follow-up questions.

### 47. File-attached debugging
```bash
claude -f train.py "Why is my model not converging?"
```
→ File-attached debugging.

### 48. Detect dead code
```bash
claude --analyze-folder . --focus "dead code"
```
→ Detects unused modules/functions.

### 49. Natural text transformation
```bash
claude "Rewrite this prompt for a 10-year-old"
```
→ Natural text transformation.

### 50. Production-level code generation
```bash
claude --generate-file "C++ header for vector class with operator overloading" --out vector.hpp
```
→ Production-level code generation.

---

# Internals / Dispatch Order
```
--chat
--analyze-folder
--project-qa
--generate-file
--fix / --explain / --refactor / -f
default: one-shot
```

---

# Notes

- binary files skipped  
- large files truncated  
- recursive safe scanning  
- speed optimized  
- architecture-aware  
- editor-independent  

---

Enjoy building with your new **local AI engineer**.
