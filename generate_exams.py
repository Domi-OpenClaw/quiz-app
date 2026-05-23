#!/usr/bin/env python3
"""生成20套固定试卷，覆盖全部755题，不重复
单选649 判断50 填空47 连线9 = 755
分配: 单选32~33/套 + 判断2~3/套 + 填空2~3/套 + 连线0~1/套
"""
import json, random
random.seed(42)

d = json.load(open('questions.json'))

single = []
for q in d['单选']: single.append({**q, 'type': 'single'})
for cat in ['情境综合', '模块综合']:
    for q in d.get(cat, []):
        if q.get('type') == 'single': single.append(q)
judge = []
for cat in ['情境综合', '模块综合']:
    for q in d.get(cat, []):
        if q.get('type') == 'judge': judge.append(q)
fill = []
for cat in ['情境综合', '模块综合']:
    for q in d.get(cat, []):
        if q.get('type') == 'fill': fill.append(q)
match = []
for q in d.get('情境综合', []):
    if q.get('type') == 'match': match.append(q)

print(f"题库: 单选{len(single)} 判断{len(judge)} 填空{len(fill)} 连线{len(match)} = {len(single)+len(judge)+len(fill)+len(match)}")

random.shuffle(single); random.shuffle(judge); random.shuffle(fill); random.shuffle(match)

# 分配: 649=11×32+9×33, 50=10×3+10×2, 47=7×3+13×2, 9=9×1+11×0
sc = [32]*11 + [33]*9   # 649
jc = [3]*10 + [2]*10    # 50
fc = [3]*7 + [2]*13     # 47
mc = [1]*9 + [0]*11     # 9

si=ji=fi=mi=0; exams={}
for s in range(1, 21):
    qs=[]
    for _ in range(sc[s-1]):
        if si<len(single): qs.append(single[si]); si+=1
    for _ in range(jc[s-1]):
        if ji<len(judge): qs.append(judge[ji]); ji+=1
    for _ in range(fc[s-1]):
        if fi<len(fill): qs.append(fill[fi]); fi+=1
    for _ in range(mc[s-1]):
        if mi<len(match): qs.append(match[mi]); mi+=1
    random.shuffle(qs)
    types={}
    for q in qs:
        t=q.get('type','single'); types[t]=types.get(t,0)+1
    exams[str(s)]=qs
    print(f"  试卷{s}: {len(qs)}题 → {types}")

# 验证无重复
used = set()
for s in exams:
    for q in exams[s]:
        key = (q.get('image',''), q.get('question','')[:50])
        assert key not in used, f"重复: {key}"
        used.add(key)
print(f"\n✅ 无重复，覆盖 {len(used)}/{len(single)+len(judge)+len(fill)+len(match)} 题")

with open('exams.json','w',encoding='utf-8') as f:
    json.dump(exams, f, ensure_ascii=False)

import os; print(f"exams.json: {os.path.getsize('exams.json')} bytes")
