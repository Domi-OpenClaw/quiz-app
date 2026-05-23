#!/usr/bin/env python3
"""修复连线题数据：统一answer格式为完整文本"""
import json

d = json.load(open('exams.json'))

fixed = 0
for s in d:
    for q in d[s]:
        if q.get('type') == 'match':
            ans = q.get('answer', '')
            opts = q.get('options', {})
            parts = ans.split(',')
            new_parts = []
            changed = False
            for p in parts:
                if '——' in p:
                    new_parts.append(p)
                elif '→' in p:
                    left, right = p.split('→', 1)
                    # 如果right是单个字母，查options替换
                    if len(right) == 1 and right in opts:
                        new_parts.append(f"{left}——{opts[right]}")
                        changed = True
                    else:
                        new_parts.append(p)
                else:
                    new_parts.append(p)
            if changed:
                q['answer'] = ','.join(new_parts)
                fixed += 1
                print(f"  试卷{s}: {ans[:40]}... → {q['answer'][:50]}...")

with open('exams.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False)

print(f"\n✅ 修复 {fixed} 题")
