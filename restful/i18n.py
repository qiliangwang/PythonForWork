import os
import json


def main():
    project_info = {'rearservices': 'C:/Users/Administrator/Desktop/TODO/GIT/ui-web-rearservices'}
    i18n = 'src\i18n'
    page = 'src\page'
    for key, value in project_info.items():
        i18n_path = os.path.join(value, i18n)
        page_path = os.path.join(value, page)
        process_i18n(i18n_path)
        process_page(page_path)


def process_i18n(i18n_path):
    data = os.listdir(i18n_path)
    data.remove('index.js')
    for d in data:
        res = parse_i18n_file(os.path.join(i18n_path, d))


def parse_i18n_file(path):
    data = js2json(path)
    res = []
    build_info(data, res, '')
    print(res)
    return data


def js2json(path):
    with open(path, encoding='utf-8') as f:
        print('------ start parse', path, '------')
        lines = f.readlines()
        lines = [line for line in lines if not line.strip(' ').startswith('//')]
        data = ''.join(lines)
        data = data.replace(':', '":').replace("'", '"')
        data = list(data.strip('export default '))
        data.reverse()
        colon = False
        braces = False
        for i in range(len(data)):
            c = data[i]
            if c is ':':
                colon = True
            if colon and c is ' ':
                data[i] = '"'
                colon = False

            if c is '}':
                braces = True
            if braces:
                if c is '"':
                    braces = False
                if c is ',':
                    braces = False
                    data[i] = ""
                if c is ' ' or '\n' or '}':
                    continue
                else:
                    braces = False

        data.reverse()
        json_str = ''.join(data)
        return json.loads(json_str)


def process_page(page_path):
    data = []
    find_all_json(page_path, data)
    for d in data:
        parse_page_file(d)


def find_all_json(base_path, results):
    for path in os.listdir(base_path):
        path = os.path.join(base_path, path)
        if os.path.isdir(path):
            find_all_json(path, results)
        elif path.endswith('.json'):
            results.append(path)


def parse_page_file(path):
    with open(path, encoding='utf-8') as f:
        print('------ start parse', path, '------')
        data = json.load(f)
    res = []
    build_info(data, res, '')
    print(res)
    return data


def build_info(data, res, base):
    for key, value in dict(data).items():
        full_key = key
        if base is not '':
            full_key = base + '--' + key
        if isinstance(value, str):
            res.append((full_key, value))
        else:
            build_info(data[key], res, full_key)
    pass


if __name__ == '__main__':
    main()
