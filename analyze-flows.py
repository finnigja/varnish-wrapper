#!/usr/bin/env python

import sqlite3
import difflib

positions = ['precache', 'postcache']
types = [('request', '=>'), ('response', '<=')]

db_conn = sqlite3.connect('flows.db', check_same_thread=False)
db_conn.row_factory = sqlite3.Row


def diff_http_elements(headers1, content1, headers2, content2):
    return {
        'headers': difflib.SequenceMatcher(None, headers1, headers2).ratio(),
        'content': difflib.SequenceMatcher(None, content1, content2).ratio()
    }


def diff_text(position1, text1, position2, text2):
    return (
        difflib.unified_diff(
            str(text1).splitlines(),
            str(text2).splitlines(),
            lineterm='',
            fromfile=position1,
            tofile=position2
        )
    )


c1 = db_conn.cursor()
for i, row in enumerate(
    c1.execute('''SELECT * FROM request GROUP BY uuid ORDER BY time''')
):
    uuid = row['uuid']
    req_str = "{0} {1}://{2}:{3}{4}".format(
        row['method'], row['scheme'], row['host'], row['port'], row['path']
    )
    print("[-- {0} : {1} --]".format(i, req_str))
    c2 = db_conn.cursor()
    positions = ['source',]
    results = []
    for (type_text, type_arrow) in types:
        baseline = None
        for row in c2.execute(
            '''SELECT * FROM {0} WHERE uuid = ?'''.format(type_text), (uuid,)
        ):
            positions.append(row['position'])
            status_code = row['status_code'] if 'status_code' in row.keys() else ''
            if status_code != '':
                positions[-1] = '{0} ({1})'.format(positions[-1], status_code)
            if baseline is None:
                baseline = row
            else:
                diff_ratios = diff_http_elements(
                    baseline['headers'], baseline['content'],
                    row['headers'], row['content']
                )
                results.append("{0} {1}: headers {2}, content {3} ({4})".format(
                    type_arrow,
                    row['position'],
                    "{0:.2f}".format(diff_ratios['headers']),
                    "{0:.2f}".format(diff_ratios['content']),
                    status_code
                ))
                for http_element in ['headers', 'content']:
                    if diff_ratios[http_element] != 1.0:
                        results.append(''.join(['\t{0}\n'.format(line) for line in (
                            diff_text(
                                baseline['position'], baseline[http_element],
                                row['position'], row[http_element]
                            )
                        )]))
        positions.append('origin') if type_text == 'request' else positions.append('source')
    print(' => '.join(positions))
    for r in results:
        print(r)

if db_conn is not None:
    db_conn.close()
