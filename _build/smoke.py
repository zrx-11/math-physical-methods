# -*- coding: utf-8 -*-
"""成品冒烟：章节公式、深度片段展开、图谱页、测验页、控制台错误。"""
import sys
from playwright.sync_api import sync_playwright

INDEX = sys.argv[1]
KEY = "math-physical-methods"


def main():
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/local/bin/chromium")
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto("file://" + INDEX)
        pg.wait_for_timeout(1200)
        print("首页 view 字符数:", len(pg.inner_text("#view")))

        pg.evaluate(f"location.hash='#/book/{KEY}/chapter/ch04'")
        pg.wait_for_timeout(1800)
        print("章节标题:", pg.inner_text("#view").split("\n")[0][:40])
        print("章节 .katex:", pg.eval_on_selector_all(".katex", "e=>e.length"))
        print("章节表格:", pg.eval_on_selector_all("#view table", "e=>e.length"), "| mermaid:", pg.eval_on_selector_all("#view .mermaid", "e=>e.length"), "| mermaid svg:", pg.eval_on_selector_all("#view .mermaid svg", "e=>e.length"))
        pg.evaluate(f"location.hash='#/book/{KEY}/chapter/ch00'")
        pg.wait_for_timeout(1000)
        print("ch00 表格:", pg.eval_on_selector_all("#view table", "e=>e.length"))

        pg.evaluate(f"location.hash='#/book/{KEY}/concept/c403'")
        pg.wait_for_timeout(1600)
        n = pg.eval_on_selector_all("details.depth-fragment", "e=>e.length")
        print("c403 depth details:", n)
        if n:
            pg.click("details.depth-fragment > summary")
            pg.wait_for_timeout(500)
            print("展开后 open:", pg.eval_on_selector("details.depth-fragment", "e=>e.open"))
            print("depth 内 .katex:", pg.eval_on_selector_all("details.depth-fragment .katex", "e=>e.length"))

        pg.evaluate(f"location.hash='#/book/{KEY}/quiz/all'")
        pg.wait_for_timeout(1200)
        txt = pg.inner_text("#view")
        print("测验页含'测验':", "测验" in txt, "| 题块:", pg.eval_on_selector_all("#view .quiz-q, #view .qitem, #view details", "e=>e.length"), "| 选项:", pg.eval_on_selector_all("#view input[type=radio], #view button.opt, #view .option", "e=>e.length"))
        print("测验页字符:", len(txt))

        pg.evaluate(f"location.hash='#/book/{KEY}/graph'")
        pg.wait_for_timeout(2500)
        print("图谱 canvas:", pg.eval_on_selector_all("#graph-container canvas", "e=>e.length"),
              "| done:", pg.eval_on_selector("#graph-container", "e=>e.dataset.done"),
              "| 页面不存在:", "页面不存在" in pg.inner_text("#view"))

        print("控制台错误:", errors[:5], "共", len(errors))
        b.close()


if __name__ == "__main__":
    main()
