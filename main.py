from jinja2 import Template
import json


class Link:
    def __init__(self, name, href):
        self.name = name
        self.href = href


class Paper:
    def __init__(self, data):
        self.title = data['title']
        self.authors = data['authors']
        self.source = data['source']
        self.date = data['date']
        self.links = [Link(k, v) for k, v in data['links'].items()]
        self.field = data['field']
        self.task = data['task']


class Field:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = [Task(k, v) for k, v in tasks.items()]

    @property
    def total(self):
        return sum([len(task.papers) for task in self.tasks])

class Task:
    def __init__(self, name, papers):
        self.name = name
        self.papers = papers

    @property
    def url_name(self):
        return self.name.lower().replace(' ', '_')


def find_all_fields(papers):
    fields = {}
    for paper in papers:
        if paper.field not in fields:
            fields[paper.field] = {}
        if paper.task not in fields[paper.field]:
            fields[paper.field][paper.task] = set()
        fields[paper.field][paper.task].add(paper)

    field_objs = []
    for k, v in fields.items():
        obj = Field(k, v)
        field_objs.append(obj)

    return field_objs


def main():
    with open('db.json', 'r') as f:
        db = json.load(f)

    papers = [Paper(paper) for paper in db['papers']]

    fields = find_all_fields(papers)

    with open('docs/template.html', 'r') as fin:
        template = Template(fin.read(), lstrip_blocks=True, trim_blocks=True)

        first = True
        for field in fields:
            for task in field.tasks:
                out = template.render(fields=fields, papers=task.papers, highlight_task=task)
                with open(f'docs/{task.url_name}.html', 'w') as fout:
                    fout.write(out)
                if first:
                    with open(f'docs/index.html', 'w') as fout:
                        fout.write(out)
                    first = False


if __name__ == '__main__':
    main()
