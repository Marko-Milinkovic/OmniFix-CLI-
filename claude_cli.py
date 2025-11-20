#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

import anthropic

# ============================================================
#  CONFIG
# ============================================================

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not API_KEY:
    print("[ERROR] Missing ANTHROPIC_API_KEY environment variable.")
    print("Run this in PowerShell:")
    print('  setx ANTHROPIC_API_KEY "sk-ant-..."')
    sys.exit(1)

# Main model (you chose Sonnet).
# If you get 404 errors, fall back to: "claude-3-haiku-20240307"
MODEL_NAME = "claude-3-haiku-20240307"


client = anthropic.Anthropic(api_key=API_KEY)

# ============================================================
#  LANGUAGE SUPPORT
# ============================================================

SUPPORTED_EXTS = {
    ".py", ".pyw",
    ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp",
    ".java",
    ".kt", ".kts",
    ".js", ".jsx",
    ".ts", ".tsx",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".html", ".htm",
    ".css",
    ".json",
    ".yaml", ".yml",
    ".xml",
}


def detect_language(path: Path) -> str:
    ext = path.suffix.lower()

    if ext in {".py", ".pyw"}:
        return "python"
    if ext in {".c", ".cpp", ".cc", ".cxx", ".h", ".hpp"}:
        return "cpp"
    if ext == ".java":
        return "java"
    if ext in {".kt", ".kts"}:
        return "kotlin"
    if ext in {".js", ".jsx"}:
        return "javascript"
    if ext in {".ts", ".tsx"}:
        return "typescript"
    if ext == ".cs":
        return "csharp"
    if ext == ".go":
        return "go"
    if ext == ".rs":
        return "rust"
    if ext == ".php":
        return "php"
    if ext in {".html", ".htm"}:
        return "html"
    if ext == ".css":
        return "css"
    if ext == ".json":
        return "json"
    if ext in {".yaml", ".yml"}:
        return "yaml"
    if ext == ".xml":
        return "xml"
    return "text"


def iter_code_files(root: Path):
    """
    Iterate over all supported 'code-like' files in a folder recursively.
    """
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            yield p

# ============================================================
#  CLAUDE CALL
# ============================================================

def call_claude(messages, max_tokens=4096, temperature=0.1):
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        return f"[API ERROR] {str(e)}"

# ============================================================
#  FILE HELPERS
# ============================================================

def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return p.read_text(encoding="utf-8")


def write_output_if_needed(args, content: str):
    """
    If --out is provided, write to that file. Otherwise print to stdout.
    """
    if not getattr(args, "out", None):
        print(content)
        return

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"\n[OK] Written to {out_path.resolve()}\n")

# ============================================================
#  PROMPT BUILDERS (ONE-SHOT / EXPLAIN)
# ============================================================

def build_single_prompt(args):
    if args.file:
        text = read_file(args.file)
        user_prompt = args.prompt or ""
        return (
            "You are an expert senior software engineer.\n"
            f"File: {args.file}\n\n"
            f"{text}\n\n"
            f"User request: {user_prompt}"
        )
    return args.prompt or ""


def build_explain_prompt(path: str):
    text = read_file(path)
    return (
        "Explain the following file in full detail:\n"
        "- overall purpose\n"
        "- key functions/classes\n"
        "- how data flows\n"
        "- important design decisions\n"
        "- potential pitfalls\n\n"
        f"Path: {path}\n\n"
        f"{text}"
    )

# ============================================================
#  PROMPT BUILDERS (LANGUAGE-AWARE FIX / REFACTOR / REWRITE)
# ============================================================

def _lang_header_fix(lang: str) -> str:
    if lang == "python":
        return (
            "You are a senior Python engineer.\n"
            "Fix all bugs, inefficiencies, missing checks, and anti-patterns.\n"
            "Preserve EXACT external behavior and public API.\n\n"
        )
    if lang == "cpp":
        return (
            "You are a senior C++17 engineer.\n"
            "Fix all bugs, undefined behavior, memory issues, and anti-patterns.\n"
            "Prefer RAII, smart pointers, const-correctness, and modern STL.\n"
            "Preserve observable behavior and public interface.\n\n"
        )
    if lang == "java":
        return (
            "You are a senior Java engineer.\n"
            "Fix all bugs and anti-patterns using modern Java best practices.\n"
            "Preserve behavior and public API.\n\n"
        )
    if lang == "kotlin":
        return (
            "You are a senior Kotlin/Android engineer.\n"
            "Fix all bugs and improve safety using idiomatic Kotlin.\n"
            "Preserve behavior and public API.\n\n"
        )
    if lang in {"javascript", "typescript"}:
        return (
            f"You are a senior {lang} engineer.\n"
            "Fix all bugs, race conditions, and performance issues.\n"
            "Use modern language features and best practices.\n"
            "Preserve the observable behavior.\n\n"
        )
    if lang in {"html", "css"}:
        return (
            f"You are a senior {lang.upper()} engineer.\n"
            "Clean up structure, fix obvious issues, and keep the same visual behavior.\n\n"
        )
    return (
        "You are a senior software engineer.\n"
        "Fix all obvious bugs, inefficiencies, missing checks, and anti-patterns.\n"
        "Preserve the same external behavior and semantics.\n\n"
    )


def _lang_header_refactor(lang: str) -> str:
    if lang == "python":
        return (
            "You are a senior Python engineer.\n"
            "Refactor this file for readability, maintainability, structure, and comments.\n"
            "Maintain EXACT external behavior.\n\n"
        )
    if lang == "cpp":
        return (
            "You are a senior C++17 engineer.\n"
            "Refactor for clarity, RAII, const-correctness, and better structure.\n"
            "Keep the public API and semantics unchanged.\n\n"
        )
    if lang == "java":
        return (
            "You are a senior Java engineer.\n"
            "Refactor using clean OOP design, clear naming, and modern Java patterns.\n"
            "Maintain existing behavior and public API.\n\n"
        )
    if lang == "kotlin":
        return (
            "You are a senior Kotlin/Android engineer.\n"
            "Refactor to idiomatic Kotlin, improving null-safety and readability.\n"
            "Preserve behavior and signatures.\n\n"
        )
    if lang in {"javascript", "typescript"}:
        return (
            f"You are a senior {lang} engineer.\n"
            "Refactor for readability, modularity, and maintainability.\n"
            "Use modern language features. Preserve behavior.\n\n"
        )
    if lang in {"html", "css"}:
        return (
            f"You are a senior {lang.upper()} engineer.\n"
            "Refactor for cleaner structure, semantics, and maintainability.\n"
            "Keep the same visual behavior.\n\n"
        )
    return (
        "You are a senior software engineer.\n"
        "Refactor this file for readability, maintainability, structure, and comments.\n"
        "Maintain the same external behavior.\n\n"
    )


def _lang_header_rewrite(lang: str) -> str:
    base = (
        "You are a principal-level software architect.\n"
        "Completely REWRITE this module with a modern, clean, modular architecture.\n"
        "You MAY:\n"
        "- change function and class names\n"
        "- split large functions into smaller ones\n"
        "- introduce classes or interfaces where appropriate\n"
        "- reorganize responsibilities (I/O vs core logic vs config)\n"
        "- move script-style code into a main() or classes\n"
        "- remove dead code and legacy hacks\n"
        "You MUST:\n"
        "- preserve the overall PURPOSE of the module\n"
        "- keep it usable in the same general context\n"
        "- write idiomatic, production-quality code for this language\n"
        "- add clear docstrings/comments where helpful\n\n"
    )
    if lang == "python":
        return (
            base
            + "Language: Python. Use modern Python best practices (type hints, clear modules).\n\n"
        )
    if lang == "cpp":
        return (
            base
            + "Language: C++17. Use RAII, smart pointers, STL, and avoid raw new/delete where possible.\n\n"
        )
    if lang == "java":
        return (
            base
            + "Language: Java. Use clear packages, interfaces, and patterns.\n\n"
        )
    if lang == "kotlin":
        return (
            base
            + "Language: Kotlin. Use idiomatic Kotlin with data classes, extension functions, and proper null-safety.\n\n"
        )
    if lang in {"javascript", "typescript"}:
        return (
            base
            + f"Language: {lang}. Use modern modules, async/await, and clear separation of concerns.\n\n"
        )
    if lang in {"html", "css"}:
        return (
            base
            + f"Language: {lang.upper()}. Use semantic structure and maintain visual intent.\n\n"
        )
    return base + "Language: generic code/text.\n\n"


def build_fix_prompt(path: str):
    p = Path(path)
    lang = detect_language(p)
    text = read_file(path)

    header = _lang_header_fix(lang)
    return (
        header
        + f"File path: {path}\n\n"
        + "Current content:\n"
        "----------------\n"
        f"{text}\n"
        "----------------\n"
    )


def build_refactor_prompt(path: str):
    p = Path(path)
    lang = detect_language(p)
    text = read_file(path)

    header = _lang_header_refactor(lang)
    return (
        header
        + f"File path: {path}\n\n"
        + "Current content:\n"
        "----------------\n"
        f"{text}\n"
        "----------------\n"
    )


def build_rewrite_prompt(path: str):
    p = Path(path)
    lang = detect_language(p)
    text = read_file(path)

    header = _lang_header_rewrite(lang)
    return (
        header
        + f"Original file path: {path}\n\n"
        + "Original file content:\n"
        "----------------------\n"
        f"{text}\n"
        "----------------------\n"
        "Now output ONLY the full rewritten file content.\n"
    )

# ============================================================
#  PROJECT-LEVEL PROMPTS
# ============================================================

def build_folder_analysis_prompt(folder: str):
    folder_path = Path(folder)
    file_list = "\n".join(str(p) for p in folder_path.rglob("*") if p.is_file())

    return (
        "You are a principal-level software architect.\n"
        f"Analyze the ENTIRE project located at:\n{folder_path}\n\n"
        "Files included:\n"
        f"{file_list}\n\n"
        "For EVERY important code file, provide:\n"
        "- purpose summary\n"
        "- logic explanation\n"
        "- major bugs or risks\n"
        "- inefficiencies\n"
        "- weak architecture\n"
        "- security issues\n"
        "- dead code\n"
        "- concrete refactor recommendations\n\n"
        "Then propose:\n"
        "- improved folder structure\n"
        "- improved module boundaries\n"
        "- improved architecture\n"
        "- cleanup and modernization plan\n"
    )


def build_project_qa_prompt(folder: str, question: str):
    folder_path = Path(folder)
    file_list = "\n".join(str(p) for p in folder_path.rglob("*") if p.is_file())

    return (
        "You are an expert senior engineer. Answer questions about this codebase.\n\n"
        f"Project root: {folder_path}\n\n"
        f"Files:\n{file_list}\n\n"
        f"User question:\n{question}"
    )


def build_diff_prompt(file_a: str, file_b: str):
    text_a = read_file(file_a)
    text_b = read_file(file_b)

    return (
        "You are an expert senior engineer. Compare the following two files.\n"
        "Provide:\n"
        "- a unified diff\n"
        "- summary of functional changes\n"
        "- improvements introduced\n"
        "- potential regressions\n"
        "- style / architecture changes\n"
        "- recommendations for further improvements\n\n"
        f"File A: {file_a}\n{text_a}\n\n"
        f"File B: {file_b}\n{text_b}\n\n"
        "Now produce the full analysis."
    )

# ============================================================
#  EXECUTION MODES
# ============================================================

def run_one_shot(args):
    prompt = build_single_prompt(args)
    reply = call_claude(
        [{"role": "user", "content": prompt}],
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )
    write_output_if_needed(args, reply)


def run_explain(args):
    prompt = build_explain_prompt(args.explain)
    reply = call_claude([{"role": "user", "content": prompt}])
    write_output_if_needed(args, reply)


def run_fix(args):
    prompt = build_fix_prompt(args.fix)
    reply = call_claude([{"role": "user", "content": prompt}])
    write_output_if_needed(args, reply)


def run_refactor(args):
    prompt = build_refactor_prompt(args.refactor)
    reply = call_claude([{"role": "user", "content": prompt}])
    write_output_if_needed(args, reply)


def run_analyze_folder(args):
    prompt = build_folder_analysis_prompt(args.analyze_folder)
    reply = call_claude(
        [{"role": "user", "content": prompt}],
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )
    write_output_if_needed(args, reply)


def run_project_qa(args):
    prompt = build_project_qa_prompt(args.project_qa, args.question)
    reply = call_claude([{"role": "user", "content": prompt}])
    write_output_if_needed(args, reply)


def run_generate_file(args):
    prompt = (
        "Generate the requested file. Output ONLY valid file content.\n\n"
        f"User specification:\n{args.generate_file}"
    )
    reply = call_claude([{"role": "user", "content": prompt}])
    write_output_if_needed(args, reply)


def run_diff(args):
    file_a, file_b = args.diff
    prompt = build_diff_prompt(file_a, file_b)
    reply = call_claude([{"role": "user", "content": prompt}])
    write_output_if_needed(args, reply)


def run_fix_folder(args):
    root = Path(args.fix_folder)
    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Folder not found or not a directory: {root}")
        return

    out_root = root.with_name(root.name + "_fixed")
    print(f"[INFO] Fixing all supported code files in:\n  {root}\n[INFO] Output folder:\n  {out_root}\n")

    count = 0
    for src in iter_code_files(root):
        rel = src.relative_to(root)
        dst = out_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        prompt = build_fix_prompt(str(src))
        reply = call_claude(
            [{"role": "user", "content": prompt}],
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )

        dst.write_text(reply, encoding="utf-8")
        print(f"[OK] Fixed {src} -> {dst}")
        count += 1

    print(f"\n[DONE] Fixed {count} file(s). Output project folder:\n  {out_root}\n")


def run_refactor_folder(args):
    """
    Refactor all supported code files in a folder recursively.
    Writes results into <folder>_refactored/, mirroring structure.
    """
    root = Path(args.refactor_folder)
    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Folder not found or not a directory: {root}")
        return

    out_root = root.with_name(root.name + "_refactored")
    print(f"[INFO] Refactoring all supported code files in:\n  {root}\n[INFO] Output folder:\n  {out_root}\n")

    count = 0
    for src in iter_code_files(root):
        rel = src.relative_to(root)
        dst = out_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        prompt = build_refactor_prompt(str(src))
        reply = call_claude(
            [{"role": "user", "content": prompt}],
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )

        dst.write_text(reply, encoding="utf-8")
        print(f"[OK] Refactored {src} -> {dst}")
        count += 1

    print(f"\n[DONE] Refactored {count} file(s). Output project folder:\n  {out_root}\n")


def run_rewrite_folder(args):
    """
    Aggressively rewrite all supported code files in a folder with a new architecture.
    Writes results into <folder>_rewritten/, mirroring structure.
    """
    root = Path(args.rewrite_folder)
    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Folder not found or not a directory: {root}")
        return

    out_root = root.with_name(root.name + "_rewritten")
    print(f"[INFO] REWRITING all supported code files in:\n  {root}\n[INFO] Output folder:\n  {out_root}\n")
    print("[WARN] This is an aggressive mode. Resulting code may not be drop-in compatible.\n")

    count = 0
    for src in iter_code_files(root):
        rel = src.relative_to(root)
        dst = out_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        prompt = build_rewrite_prompt(str(src))
        reply = call_claude(
            [{"role": "user", "content": prompt}],
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )

        dst.write_text(reply, encoding="utf-8")
        print(f"[OK] Rewrote {src} -> {dst}")
        count += 1

    print(f"\n[DONE] Rewrote {count} file(s). Output project folder:\n  {out_root}\n")

# ============================================================
#  ARGUMENT PARSER
# ============================================================

def build_parser():
    p = argparse.ArgumentParser(description="Claude CLI Assistant")

    # One-shot
    p.add_argument("prompt", nargs="?", help="Prompt for one-shot mode")

    # File operations
    p.add_argument("-f", "--file", help="Attach a file for context")
    p.add_argument("--explain", help="Explain a file")
    p.add_argument("--fix", help="Fix a file")
    p.add_argument("--refactor", help="Refactor a file")

    # Project modes
    p.add_argument("--analyze-folder", help="Full project analysis")
    p.add_argument("--project-qa", help="Ask a question about a project")
    p.add_argument("--question", help="Question for project QA mode")

    # File generation
    p.add_argument("--generate-file", help="Specification to generate a new file")

    # Diff
    p.add_argument(
        "--diff",
        nargs=2,
        metavar=("FILE_OLD", "FILE_NEW"),
        help="Compare two files and explain all differences",
    )

    # Folder-wide modes
    p.add_argument(
        "--fix-folder",
        help="Fix all supported code files in a folder into <folder>_fixed",
    )
    p.add_argument(
        "--refactor-folder",
        help="Refactor all supported code files in a folder into <folder>_refactored",
    )
    p.add_argument(
        "--rewrite-folder",
        help="Aggressively rewrite all supported code files in a folder into <folder>_rewritten",
    )

    # Output redirection
    p.add_argument("--out", help="Write output to a file")

    # Model tuning
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--temperature", type=float, default=0.1)

    return p

# ============================================================
#  MAIN
# ============================================================

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.explain:
        return run_explain(args)
    if args.fix:
        return run_fix(args)
    if args.refactor:
        return run_refactor(args)
    if args.analyze_folder:
        return run_analyze_folder(args)
    if args.project_qa and args.question:
        return run_project_qa(args)
    if args.generate_file:
        return run_generate_file(args)
    if args.diff:
        return run_diff(args)
    if args.fix_folder:
        return run_fix_folder(args)
    if args.refactor_folder:
        return run_refactor_folder(args)
    if args.rewrite_folder:
        return run_rewrite_folder(args)

    # Default: one-shot chat
    return run_one_shot(args)


if __name__ == "__main__":
    main()
