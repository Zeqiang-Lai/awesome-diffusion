import json
from datetime import datetime
import re

def dmy_to_ymd(d):
    return datetime.strptime(d, '%d %b %Y').strftime('%Y-%m-%d')


with open('Resource.md', 'r') as f:
    lines = f.readlines()
    # remove empty line
    lines = [line for line in lines if line.strip()]
    # find index of line that start with #
    indexs = [i for i, line in enumerate(lines) if line.startswith('##') and not line.startswith('###')]

    db = {"resources": []}

    # split lines by index
    indexs += [len(lines)]
    for i, idx in enumerate(indexs[:-1]):
        field = lines[idx].strip('##').strip()
        print(field)
        content = lines[idx + 1:indexs[i + 1]]

        second_indexs = [i for i, line in enumerate(content) if line.startswith('###')]
        second_indexs += [len(content)]
        for i, idx in enumerate(second_indexs[:-1]):
            task = content[idx].strip('###').strip()
            second_content = content[idx + 1:second_indexs[i + 1]]
            print(task, len(second_content))

            for l in range(0, len(second_content), 4):
                item = second_content[l:l + 4]

                obj = {}
                obj['title'] = item[0][2:-5]
                obj['authors'] = item[1][1:-4]

                linkstr = item[2][:-1].strip()
                links = re.findall("\[\[([^\]]*)\]\(([^\)]+)\)\]", linkstr)
                links2 = {}
                for name, href in links:
                    links2[name] = href

                obj['links'] = links2

                obj['date'] = dmy_to_ymd(item[3].strip())
                obj['field'] = field
                obj['task'] = task

                db['resources'].append(obj)

    with open('resource.json', 'w') as fout:
        json.dump(db, fout)
