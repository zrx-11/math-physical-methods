# 数学物理方法 · 知枢学习系统

一套按依赖关系组织的数学物理方法学习网页。打开根目录的 `index.html` 就是总入口；单书完整版在 `01-数学物理方法/数学物理方法学习伴侣.html`。

## 这是什么

- **填充版**：十四章正文已写成零基础精讲（每章 2500–4900 字），61 个概念页都有"详解"，5 个高难概念挂了第一性原理深度片段。
- 每章按"这一章解决什么问题 → 学习目标 → 一句话核心 → 零基础讲解 → 图示 → 类比与实例 → 常见误解 → 自测题（带解析）→ 复习锚点"组织；实例都能拿纸算通。
- 每个概念页在原有四块（定义、位置、核心结论、常见误解）之后加了"白话解释 / 能验算的小例子 / 与相邻概念的区别"。
- 100 道测验题、120 张抽认卡，每章 7–8 题、8–9 张卡。依赖图、学习路径、诊断、搜索、进度保存全部保留。

## 目录结构

| 路径 | 说明 |
|---|---|
| `index.html` | 总入口（单文件，含总览、章节、概念、测验、卡片、术语、图谱、诊断、全局搜索） |
| `index.md` | 总入口的 Markdown 导航 |
| `00-总览/README.md` | 课程总览：主线、十四章结构、依赖读法、四阶段路径 |
| `01-数学物理方法/` | 单书知识库：`SKILL.md` 总纲、`chapters/`、`concepts/`、`glossary.md`、`patterns.md`、`cheatsheet.md`、`quiz.md`、`flashcards.md`、`manifest.json` |
| `01-数学物理方法/数学物理方法学习伴侣.html` | 单书伴侣，功能最全（含原生知识图谱页） |
| `01-数学物理方法/_work/` | 写作规范、题卡手稿、合并脚本与旧版框架数据 |
| `_build/` | 总入口组装、知识图谱补丁、渲染冒烟、验证报告 |
| `.nojekyll` | GitHub Pages 关闭 Jekyll |

## 怎么用

1. 双击 `index.html`，或部署后用网址打开。
2. 先看「总览」，知道十四章怎么排、依赖链怎么读。
3. 进「学习路径」，按 15 步推进；每步过了检查点再往下。
4. 章节页读精讲与自测，概念页查定义与例子；答错测验时用「诊断测试」沿前置链倒推。
5. 五个高难概念页底部的「展开完整第一性原理推导」默认收起，卡住时再展开。
6. 进度存在浏览器本地，可导出/导入 JSON，跨设备迁移。

## 部署 GitHub Pages

当前已部署：<https://zrx-11.github.io/math-physical-methods/>（仓库 <https://github.com/zrx-11/math-physical-methods>）。

```bash
# 把 zip 解压后的内容（index.html 所在那层）作为仓库根
cd 数学物理方法-知枢
git init
git add .
git commit -m "数学物理方法学习系统（填充版）"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

然后在仓库 Settings → Pages → Source 选 `main` / `(root)`，保存后等一分钟。

## 重新生成

```bash
cd 01-数学物理方法
python3 _work/assemble.py
python3 <zhishu>/scripts/build_companion.py --manifest manifest.json --out 数学物理方法学习伴侣.html
python3 <zhishu>/scripts/apply_visual_theme.py --file 数学物理方法学习伴侣.html
cd ..
python3 <zhishu>/scripts/build_handbook.py --root . --cross-dir 00-总览
python3 <zhishu>/scripts/apply_visual_theme.py --root .
python3 _build/patch_graph.py
```

顺序不能反：`build_handbook.py` 会覆盖 `index.html`，视觉层与图谱补丁都要放在它之后。

`_work/build_framework.py` 是上一版用框架文案生成 Markdown 的脚本，现在执行会把精讲覆盖回骨架，不要跑。

## 已知限制

- 总入口的「知识图谱」页用 `_build/patch_graph.py` 接入（zhishu 1.9.0 的总入口脚本未注册该路由）。vis-network 已内联，`index.html` 因此约 1.8 MB。
- 公式与图谱库已内联（`--offline all` 构建），断网可用；单书伴侣约 3.5 MB，总入口约 1.9 MB。
- 深度片段只覆盖五个高难概念，其余概念页是常规精讲，不含长推导。
- `verify_handbook.py` 的首页断言写死了另一本书的标题，稳定报 1 项失败（32/33），属已知假阳性。
