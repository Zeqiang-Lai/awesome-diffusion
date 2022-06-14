import json
from datetime import datetime


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

                source, links = item[2][:-2].strip().split('.', maxsplit=1)
                obj['source'] = source

                links = links.strip().split(' ')
                links = [link[1:-1] for link in links]
                links2 = {}
                for link in links:
                    name, url = link.split(']')
                    name = name[1:].strip()
                    url = url[1:-1].strip()
                    links2[name] = url
                obj['links'] = links2

                obj['date'] = dmy_to_ymd(item[3].strip())
                obj['field'] = field
                obj['task'] = task

                db['papers'].append(obj)

    with open('db.json', 'w') as fout:
        json.dump(db, fout)
