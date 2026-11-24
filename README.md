# 数学物理方法 · 知枢学习系统

一套按依赖关系组织的数学物理方法学习网页。打开根目录的 `index.html` 就是总入口；单书完整版在 `01-数学物理方法/数学物理方法学习伴侣.html`。

## 这是什么

- **框架版**：十四章结构、61 个概念、依赖图、学习路径、术语表、模式库、速查表、28 道检查题、42 张抽认卡已经齐了。
- 章节页给到"本章解决什么问题 + 学习目标 + 概念链 + 难点地图 + 检查点"；概念页给到"一句话定义 + 体系位置 + 核心结论 + 常见误解"。
- 逐章零基础精讲与高难概念的第一性原理推导，留在后续版本往 Markdown 里补，不改结构。

## 目录结构

| 路径 | 说明 |
|---|---|
| `index.html` | 总入口（单文件，含总览、章节、概念、测验、卡片、术语、图谱、诊断、全局搜索） |
| `index.md` | 总入口的 Markdown 导航 |
| `00-总览/README.md` | 课程总览：主线、十四章结构、依赖读法、四阶段路径、框架边界 |
| `01-数学物理方法/` | 单书知识库：`SKILL.md` 总纲、`chapters/`、`concepts/`、`glossary.md`、`patterns.md`、`cheatsheet.md`、`quiz.md`、`flashcards.md`、`manifest.json` |
| `01-数学物理方法/数学物理方法学习伴侣.html` | 单书伴侣，功能最全（含原生知识图谱页） |
| `01-数学物理方法/_work/` | 框架生成用的文案数据与生成脚本 |
| `_build/` | 总入口组装、知识图谱补丁、验证报告 |
| `.nojekyll` | GitHub Pages 关闭 Jekyll |

## 怎么用

1. 双击 `index.html`，或部署后用网址打开。
2. 先看「总览」，知道十四章怎么排、依赖链怎么读。
3. 进「学习路径」，按 15 步推进；每步过了检查点再往下。
4. 章节页看目标与难点，概念页当前置索引；答错测验时用「诊断测试」沿前置链倒推。
5. 进度存在浏览器本地，可导出/导入 JSON，跨设备迁移。

## 部署 GitHub Pages

```bash
# 把 zip 解压后的内容（index.html 所在那层）作为仓库根
cd 数学物理方法-知枢
git init
git add .
git commit -m "数学物理方法学习系统（框架版）"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

然后在仓库 Settings → Pages → Source 选 `main` / `(root)`，保存后等一分钟。

## 重新生成

```bash
cd 01-数学物理方法
python3 _work/build_framework.py
python3 <zhishu>/scripts/build_companion.py --manifest manifest.json --out 数学物理方法学习伴侣.html
python3 <zhishu>/scripts/apply_visual_theme.py --file 数学物理方法学习伴侣.html
cd ..
python3 <zhishu>/scripts/build_handbook.py --root . --cross-dir 00-总览
python3 <zhishu>/scripts/apply_visual_theme.py --root . --all-html
python3 _build/patch_graph.py
```

顺序不能反：`build_handbook.py` 会覆盖 `index.html`，视觉层与图谱补丁都要放在它之后。

## 已知限制

- 总入口的「知识图谱」页用 `_build/patch_graph.py` 接入（zhishu 1.9.0 的总入口脚本未注册该路由）。vis-network 已内联，`index.html` 因此约 1 MB。
- 公式走 CDN（jsDelivr / npmmirror / unpkg 三源回退）。断网时公式显示为源码，文字与导航不受影响；要完全离线可用 `--offline all` 重建。
- 内容处于框架阶段，精讲与深度推导尚未展开。
