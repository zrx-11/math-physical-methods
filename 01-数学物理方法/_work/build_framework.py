# -*- coding: utf-8 -*-
"""把框架文案落成知枢目录：章节 MD、概念 MD、术语/模式/速查/卡片/测验、manifest.json。"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chapters_data import CHAPTERS
from concepts_a import CONCEPTS_A
from concepts_b import CONCEPTS_B
from extras_data import (SKILL_MD, GLOSSARY, PATTERNS_MD, CHEATSHEET_MD,
                         FLASHCARDS, QUIZZES, LEARNING_PATH)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLUG = "math-physical-methods"
TITLE = "数学物理方法"

DIFF_NUM = {"ch00": 1, "ch01": 1, "ch02": 2, "ch03": 2, "ch04": 3,
            "ch05": 2, "ch06": 2, "ch07": 2, "ch08": 3, "ch09": 2,
            "ch10": 3, "ch11": 3, "ch12": 3, "ch13": 2}


def w(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main():
    concepts = CONCEPTS_A + CONCEPTS_B
    cids = {c["id"] for c in concepts}
    assert len(cids) == len(concepts), "概念 id 有重复"
    chs = [c["id"] for c in CHAPTERS]

    # 章节
    for ch in CHAPTERS:
        ch["file"] = f"chapters/{ch['id']}.md"
        w(ch["file"], ch["md"].rstrip() + "\n")

    # 概念
    for c in concepts:
        c["file"] = f"concepts/{c['id']}.md"
        assert c["chapter"] in chs, c["id"]
        for p in c["prereq"]:
            assert p in cids, (c["id"], p)
        w(c["file"], c["md"].rstrip() + "\n")

    # 总纲：把索引里的中文文件名换成真实文件名
    skill = re.sub(r"chapters/(ch\d\d)-[^\s）]*?\.md", lambda m: f"chapters/{m.group(1)}.md", SKILL_MD)
    w("SKILL.md", skill)

    # 术语表
    rows = ["# 术语表", "", "| 术语 | 白话定义 | 章节 |", "|---|---|---|"]
    for term, definition, chap in GLOSSARY:
        rows.append(f"| {term} | {definition} | {chap} |")
    w("glossary.md", "\n".join(rows) + "\n")

    w("patterns.md", PATTERNS_MD)
    w("cheatsheet.md", CHEATSHEET_MD)

    # 抽认卡
    card_md = ["# 抽认卡", ""]
    for i, (chap, front, back, tags) in enumerate(FLASHCARDS, 1):
        card_md += [f"## 卡片 {i:02d}", f"**正面**：{front}", f"- **背面**：{back}",
                    f"- **标签**：{', '.join(tags)}", f"- **章节**：{chap}", ""]
    w("flashcards.md", "\n".join(card_md))

    # 测验
    quiz_md = ["# 测验", ""]
    for q in QUIZZES:
        quiz_md.append(f"## {q['id']}（{q['chapterId']}）")
        quiz_md.append(q["question"])
        quiz_md.append("")
        for i, o in enumerate(q["options"]):
            quiz_md.append(f"- {'ABCD'[i]}. {o}")
        quiz_md.append(f"**答案**：{'ABCD'[q['answer']]}　**解析**：{q['explain']}")
        quiz_md.append("")
    w("quiz.md", "\n".join(quiz_md))

    # manifest
    manifest = {
        "slug": SLUG,
        "title": TITLE,
        "subtitle": "从复变到偏微分方程的一条主线",
        "companion": "数学物理方法学习伴侣.html",
        "book": {
            "title": "数学物理方法",
            "author": "通用主线（自拟框架）",
            "source": ["通用课程主线，不绑定单一教材；章节顺序按复变 → 积分变换 → 数理方程 → 特殊函数 → 变分法组织"],
        },
        "audience": "零基础",
        "goal": "从零基础走到能独立完成建模 → 定解 → 求解 → 验算的完整链条",
        "learningPath": LEARNING_PATH,
        "chapters": [
            {
                "id": ch["id"],
                "title": ch["title"],
                "file": ch["file"],
                "difficulty": DIFF_NUM[ch["id"]],
                "source": {"file": "通用主线（自拟框架）"},
                "prerequisites": ch["prereq"],
            } for ch in CHAPTERS
        ],
        "concepts": [
            {
                "id": c["id"],
                "title": c["title"],
                "file": c["file"],
                "chapterIds": [c["chapter"]],
                "difficulty": c["difficulty"],
                "source": {"file": "通用主线（自拟框架）"},
                "prerequisites": c["prereq"],
            } for c in concepts
        ],
        "glossary": [{"term": t, "def": d, "chapterId": ch} for t, d, ch in GLOSSARY],
        "patterns": {"file": "patterns.md"},
        "cheatsheet": {"file": "cheatsheet.md"},
        "quizzes": QUIZZES,
        "flashcards": [
            {"id": f"f{i:02d}", "chapterId": chap, "front": front, "back": back, "tags": tags}
            for i, (chap, front, back, tags) in enumerate(FLASHCARDS, 1)
        ],
        "misconceptions": [],
        "claims": [],
    }
    with open(os.path.join(ROOT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"章节 {len(CHAPTERS)} · 概念 {len(concepts)} · 测验 {len(QUIZZES)} · 卡片 {len(FLASHCARDS)} · 术语 {len(GLOSSARY)}")
    print("manifest:", os.path.join(ROOT, "manifest.json"))


if __name__ == "__main__":
    main()
