import os
import json
import pymysql


def process_i18n(i18n_path):
    data = os.listdir(i18n_path)
    data.remove('index.js')
    for d in data:
        res = parse_i18n_file(os.path.join(i18n_path, d))


def parse_i18n_file(path):
    data = js2json(path)
    res = []
    build_info(data, res, '')
    # print(res)
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


def process_page(project_name):
    page = 'src/page'
    page_path = os.path.join(project_name, page)
    if not os.path.exists(page_path):
        print(page_path, 'not exist')
        return
    data = []
    find_all_json(page_path, data)
    print(len(data), page_path.split('/')[0], data)
    data = [d for d in data if not 'pcas.json' in d]
    # init_group(project_name, data)
    for group in data:
        items = parse_page_file(group)
        # init_item(group, items)
        init_translate(group, items)


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
    return res


def build_info(data, res, base):
    for key, value in dict(data).items():
        full_key = key
        if base is not '':
            full_key = base + '--' + key
        if isinstance(value, str):
            res.append((full_key, value))
        else:
            build_info(data[key], res, full_key)


def init_project(projects):

    conn_params = {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3326,
        'db': 'i18n',
    }

    # db = pymysql.connect(host='192.168.33.206', user='dev', passwd='lvyue@123456', port=3326, db='i18n')

    db = pymysql.connect(**conn_params)

    cursor = db.cursor()

    select_sql = 'select name from i18n_project'

    cursor.execute(select_sql)

    project_names = set([row[0] for row in cursor.fetchall()])

    for project in projects:
        if project not in project_names:
            sql = "INSERT INTO i18n_project(name ,created_by) VALUES ('%s', '%s')" % (project, '1')
            print(sql)
            cursor.execute(sql)
    # db.commit()
    db.close()


def init_group(project_name, groups):
    """
    project_name -> id , insert group, project_id
    :param project_name:
    :param groups:
    :return:
    """

    conn_params = {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3326,
        'db': 'i18n',
    }

    # db = pymysql.connect(host='192.168.33.206', user='dev', passwd='lvyue@123456', port=3326, db='i18n')

    db = pymysql.connect(**conn_params)

    cursor = db.cursor()

    select_project_id = "select id from i18n_project where name = '%s'" % project_name

    cursor.execute(select_project_id)

    project_id = cursor.fetchone()[0]

    group_set = set([str(group).split('/')[-1].replace('.json', '') for group in groups])

    print(project_id, group_set)

    groups_sql = 'select name from i18n_group where project_id = %s' % project_id

    cursor.execute(groups_sql)

    old_group_set = set([row[0] for row in cursor.fetchall()])

    insert_group_set = group_set - old_group_set

    # print(insert_group_set, old_group_set, group_set)
    # print(groups_sql)

    for group_name in insert_group_set:
        sql = "INSERT INTO i18n_group(name ,parent_id, project_id) VALUES ('%s', '%s', '%s')" % (group_name, 0, project_id)
        print(sql)
        cursor.execute(sql)
    db.commit()
    db.close()


def init_item(group_name, items):
    """
    group_name -> group_id -> insert(group_id, item) into item table
    :param group_name:
    :param items:
    :return:
    """
    '''
    ui-web-rearservices/src/page/opinion/opinion.json 
    
    [('id--opinionUser', 'opinionUser'), 
    ('id--content', 'content'), 
    ('id--departmentName', 'departmentName'), 
    ('id--type', 'type'), 
    ('id--recordDate', 'recordDate'), 
    ('id--viewDetail', 'viewDetail'), 
    ('id--pictureUpload', 'pictureUpload'), 
    ('zhCn--opinionUser', '意见人'), 
    ('zhCn--content', '意见内容'), 
    ('zhCn--departmentName', '部门'), 
    ('zhCn--type', '所属分类'), 
    ('zhCn--recordDate', '提出时间'), 
    ('zhCn--viewDetail', '查看详细'), 
    ('zhCn--pictureUpload', '相关图片')]
    '''
    group_name = group_name.split('/')[-1].replace('.json', '')

    conn_params = {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3326,
        'db': 'i18n',
    }

    db = pymysql.connect(**conn_params)

    cursor = db.cursor()

    select_group = "select id from i18n_group where name = '%s'" % group_name

    cursor.execute(select_group)

    group_id = cursor.fetchone()[0]

    print('group_id', group_id)

    for item in items:
        info = str(item[0]).split('--')
        name = info[1]
        sql = "INSERT INTO i18n_item(name ,group_id) VALUES ('%s', '%s')" % (name, group_id)
        print('insert item sql : ', sql)
        cursor.execute(sql)

    db.commit()

    # for item in items:
    #     info = str(item[0]).split('--')
    #
    #     name = info[1]
    #     language = info[0]
    #     value = item[1]
    #     value = str(value).replace('）', '').replace('（', '').replace('/', '').replace('，', '').replace("'", '')
    #
    #     if language == 'id':
    #         language_id = 2
    #     else:
    #         language_id = 1
    #
    #     select_item = "select id from i18n_item where name = '%s'" % name
    #
    #     cursor.execute(select_item)
    #
    #     item_id = cursor.fetchone()[0]
    #
    #     translate_sql = "INSERT INTO i18n_translate(item_id ,language_id, value) VALUES ('%s', '%s', '%s')" % (item_id, language_id, value)
    #
    #     print(translate_sql)

        # cursor.execute(translate_sql)

    # db.commit()
    db.close()


def init_translate(group_name, items):
    """
    -> select item_id -> insert(translate_id, value) into translate table
    :param group_name:
    :param items:
    :return:
    """
    '''
    ui-web-rearservices/src/page/opinion/opinion.json 

    [('id--opinionUser', 'opinionUser'), 
    ('id--content', 'content'), 
    ('id--departmentName', 'departmentName'), 
    ('id--type', 'type'), 
    ('id--recordDate', 'recordDate'), 
    ('id--viewDetail', 'viewDetail'), 
    ('id--pictureUpload', 'pictureUpload'), 
    ('zhCn--opinionUser', '意见人'), 
    ('zhCn--content', '意见内容'), 
    ('zhCn--departmentName', '部门'), 
    ('zhCn--type', '所属分类'), 
    ('zhCn--recordDate', '提出时间'), 
    ('zhCn--viewDetail', '查看详细'), 
    ('zhCn--pictureUpload', '相关图片')]
    '''

    conn_params = {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3326,
        'db': 'i18n',
    }

    db = pymysql.connect(**conn_params)

    cursor = db.cursor()

    group_name = group_name.split('/')[-1].replace('.json', '')

    select_group = "select id from i18n_group where name = '%s'" % group_name

    cursor.execute(select_group)

    group_id = cursor.fetchone()[0]

    print('group_id', group_id)

    for item in items:
        info = str(item[0]).split('--')

        name = info[1]
        language = info[0]
        value = item[1]
        value = str(value).replace('）', '').replace('（', '').replace('/', '').replace('，', '').replace("'", '')

        if language == 'id':
            language_id = 2
        else:
            language_id = 1

        select_item = "select id from i18n_item where name = '%s' and group_id = '%s' " % (name, group_id)

        print(select_item)

        cursor.execute(select_item)

        item_row = cursor.fetchone()

        if item_row is not None:

            item_id = item_row[0]

            print(name, 'id is', item_id)

            translate_sql = "INSERT INTO i18n_translate(item_id ,language_id, value) VALUES ('%s', '%s', '%s')" % ( item_id, language_id, value)

            print(translate_sql)

            cursor.execute(translate_sql)

    db.commit()

    db.close()


def main():

    project_info = {
        'shared-account-ui': 'shared-account-ui',
        'ui-web-account': 'ui-web-account',
        'ui-web-customer': 'ui-web-customer',
        'ui-web-distribution': 'ui-web-distribution',
        'ui-web-ime': 'ui-web-ime',
        'ui-web-operators': 'ui-web-operators',
        'ui-web-order': 'ui-web-order',
        'ui-web-performance': 'ui-web-performance',
        'ui-web-product': 'ui-web-product',
        'ui-web-rearservices': 'ui-web-rearservices',
        'ui-web-tool': 'ui-web-tool',
    }

    i18n = 'src/i18n'
    init_project(project_info.keys())
    for key, value in project_info.items():
        # i18n_path = os.path.join(value, i18n)
        # process_i18n(i18n_path)
        process_page(value)


def test():
    set_a = {'a', 'b', 'c', 'd', 'e', 'f'}

    set_b = {'a', 'b', 'c'}

    print(set_a - set_b)
    pass


if __name__ == '__main__':
    # test()
    main()
