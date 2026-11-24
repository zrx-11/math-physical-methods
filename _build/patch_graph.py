# -*- coding: utf-8 -*-
"""给 build_handbook 1.9.0 生成的 index.html 补上“知识图谱”路由与渲染。

总入口脚本只注册了 path/cards/glossary/patterns/cheatsheet/diagnosis，
单书伴侣里的 __graph__ 页虽然被抽取进 rendered，却没有 pid 映射与 initGraph 调用。
本补丁只改产物，不改 Skill 源脚本。可重复执行（已打过就跳过）。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
VIS = "/home/user/.doubao/agent_mode/workspace/.user_skills/zhishu/assets/vendor/vis-network.min.js"

with open(INDEX, encoding="utf-8") as f:
    html = f.read()

if "/* zs-graph-patch */" in html:
    print("已打过补丁，跳过")
    sys.exit(0)

# 1) pid 映射
old = "  if(page==='diagnosis') return '__diagnosis__';"
new = old + "\n  if(page==='graph') return '__graph__';"
assert old in html
html = html.replace(old, new, 1)

# 2) 渲染时初始化
old = "  if(cur.page==='diagnosis') initDiagnosis();"
new = old + "\n  if(cur.page==='graph') initGraph();"
assert old in html
html = html.replace(old, new, 1)

# 3) 侧栏入口
old = "  add('🩺 诊断测试','#/book/'+cur.book+'/diagnosis', cur.page==='diagnosis'?'active':'');"
new = old + "\n  add('🕸 知识图谱','#/book/'+cur.book+'/graph', cur.page==='graph'?'active':'');"
assert old in html
html = html.replace(old, new, 1)

# 4) 内联 vis-network + initGraph
with open(VIS, encoding="utf-8") as f:
    vis = f.read()

graph_js = r"""
/* zs-graph-patch */
function initGraph(){
  const container=document.getElementById('graph-container');
  if(!container) return;
  if(typeof vis==='undefined'){ container.innerHTML='<p class="empty">图谱库未加载</p>'; return; }
  if(container.dataset.done==='1') return;
  container.dataset.done='1';
  const B=BOOKS[cur.book]||{}, mf=B.manifest||{};
  const nodes=[], edges=[];
  (mf.concepts||[]).forEach(c=>{
    nodes.push({id:'c_'+c.id,label:c.title||c.id,title:c.title||c.id,shape:'dot',size:13,
                color:'#5c7cff',font:{size:12,color:'#e6edf7'}});
  });
  (mf.chapters||[]).forEach(ch=>{
    nodes.push({id:'ch_'+ch.id,label:ch.title||ch.id,title:ch.title||ch.id,shape:'box',
                color:'#16c7d9',font:{size:12,color:'#06121f'}});
  });
  const addEdge=(from,to,ptype)=>{
    const p=typeof ptype==='string'?ptype:(ptype&&ptype.type)||'hard';
    edges.push({from:from,to:to,arrows:'to',
      color:{color:p==='hard'?'#dc2626':p==='soft'?'#9ca3af':'#3b82f6'},
      width:p==='hard'?2:1,dashes:p!=='hard'});
  };
  (mf.concepts||[]).forEach(c=>{
    (c.prerequisites||[]).forEach(p=>{
      const pid=typeof p==='string'?p:(p&&p.id);
      if(pid&&nodes.find(n=>n.id==='c_'+pid)) addEdge('c_'+pid,'c_'+c.id,p);
    });
  });
  (mf.chapters||[]).forEach(ch=>{
    (ch.prerequisites||[]).forEach(p=>{
      const pid=typeof p==='string'?p:(p&&p.id);
      if(pid&&nodes.find(n=>n.id==='ch_'+pid)) addEdge('ch_'+pid,'ch_'+ch.id,p);
    });
  });
  const data={nodes:new vis.DataSet(nodes),edges:new vis.DataSet(edges)};
  const options={height:'560px',physics:{stabilization:true,barnesHut:{gravitationalConstant:-3000}},
                 interaction:{hover:true,tooltipDelay:200}};
  const net=new vis.Network(container,data,options);
  net.on('click',params=>{
    if(!params.nodes.length) return;
    const nid=params.nodes[0];
    if(nid.indexOf('c_')===0) location.hash='#/book/'+cur.book+'/concept/'+nid.slice(2);
    else if(nid.indexOf('ch_')===0) location.hash='#/book/'+cur.book+'/chapter/'+nid.slice(3);
  });
}
"""

blob = "<script>\n/* vis-network.min.js inlined */\n" + vis + "\n</script>\n<script>\n" + graph_js + "\n</script>\n"

assert "</body>" in html
html = html.replace("</body>", blob + "</body>", 1)

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print("补丁完成：", INDEX, f"{os.path.getsize(INDEX)/1024:.0f} KB")
