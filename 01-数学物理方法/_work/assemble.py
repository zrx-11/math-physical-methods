# -*- coding: utf-8 -*-
"""把子智能体产出的题卡 JSON 与深度片段合并进 manifest，并重生成 quiz.md / flashcards.md。

用法：python3 _work/assemble.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "_work")
CARDS = os.path.join(WORK, "quiz_cards")
MANIFEST = os.path.join(ROOT, "manifest.json")

DEPTH = {
    "c403": "concepts/c403-depth.md",
    "c802": "concepts/c802-depth.md",
    "c1001": "concepts/c1001-depth.md",
    "c1101": "concepts/c1101-depth.md",
    "c1201": "concepts/c1201-depth.md",
}


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        m = json.load(f)

    # 深度片段
    for c in m["concepts"]:
        df = DEPTH.get(c["id"])
        if df and os.path.exists(os.path.join(ROOT, df)):
            c["depthFragment"] = df
            print("depth:", c["id"], df)
        elif c.get("depthFragment") and not os.path.exists(os.path.join(ROOT, c["depthFragment"])):
            print("深度文件缺失，跳过：", c["depthFragment"])

    # 题与卡
    m["quizzes"] = [q for q in m["quizzes"] if not q.get("_added")]
    m["flashcards"] = [f for f in m["flashcards"] if not f.get("_added")]
    old_q = max(int(q["id"][1:]) for q in m["quizzes"]) if m["quizzes"] else 0
    old_f = max(int(f["id"][1:]) for f in m["flashcards"]) if m["flashcards"] else 0
    added_q = added_f = 0
    for name in sorted(os.listdir(CARDS)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(CARDS, name), encoding="utf-8") as f:
            data = json.load(f)
        ch = data["chapterId"]
        for q in data.get("quizzes", []):
            old_q += 1
            m["quizzes"].append({
                "id": f"q{old_q:02d}",
                "chapterId": ch,
                "type": "single",
                "question": q["question"],
                "options": q["options"],
                "answer": int(q["answer"]),
                "explain": q["explain"],
                "relatedConceptId": q.get("relatedConceptId"),
                "_added": True,
            })
            added_q += 1
        for c in data.get("flashcards", []):
            old_f += 1
            m["flashcards"].append({
                "id": f"f{old_f:02d}",
                "chapterId": ch,
                "front": c["front"],
                "back": c["back"],
                "tags": c.get("tags", [ch]),
                "_added": True,
            })
            added_f += 1
        print(f"{ch}: +{len(data.get('quizzes', []))} 题 +{len(data.get('flashcards', []))} 卡")

    # 校验每章题/卡数量
    import collections
    qc = collections.Counter(q["chapterId"] for q in m["quizzes"])
    fc = collections.Counter(f["chapterId"] for f in m["flashcards"])
    bad = [(ch["id"], qc[ch["id"]], fc[ch["id"]]) for ch in m["chapters"]
           if qc[ch["id"]] < 5 or fc[ch["id"]] < 5]
    if bad:
        print("章节题卡不足 5：", bad)
    else:
        print("每章题/卡均 ≥5：", dict(qc), dict(fc))

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)

    # quiz.md
    lines = ["# 测验", ""]
    for q in m["quizzes"]:
        lines.append(f"## {q['id']}（{q['chapterId']}）")
        lines.append(q["question"])
        lines.append("")
        for i, o in enumerate(q["options"]):
            lines.append(f"- {'ABCD'[i]}. {o}")
        lines.append(f"**答案**：{'ABCD'[q['answer']]}　**解析**：{q['explain']}")
        lines.append("")
    with open(os.path.join(ROOT, "quiz.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # flashcards.md
    lines = ["# 抽认卡", ""]
    for i, c in enumerate(m["flashcards"], 1):
        lines += [f"## 卡片 {i:02d}", f"**正面**：{c['front']}", f"- **背面**：{c['back']}",
                  f"- **标签**：{', '.join(c['tags'])}", f"- **章节**：{c['chapterId']}", ""]
    with open(os.path.join(ROOT, "flashcards.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"合并完成：+{added_q} 题 / +{added_f} 卡；总计 {len(m['quizzes'])} 题 / {len(m['flashcards'])} 卡")


if __name__ == "__main__":
    main()
