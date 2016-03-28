#!/usr/bin/env python

import sqlite3
import difflib
from collections import OrderedDict

positions = ['precache', 'postcache']
types = [('request', '->'), ('response', '<-')]

db_conn = sqlite3.connect('flows.db', check_same_thread=False)
db_conn.row_factory = sqlite3.Row


def diff_http(headers1, content1, headers2, content2):
    return (
        "{0:.2f}".format(
            difflib.SequenceMatcher(None, headers1, headers2).ratio()
        ),
        "{0:.2f}".format(
            difflib.SequenceMatcher(None, content1, content2).ratio()
        )
    )


def diff_text(text1, text2):
    return (
        difflib.unified_diff(str(text1).splitlines(), str(text2).splitlines())
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
    for (type_text, type_arrow) in types:
        baseline = None
        for row in c2.execute(
            '''SELECT * FROM {0} WHERE uuid = ?'''.format(type_text), (uuid,)
        ):
            position = row['position']
            if baseline is None:
                baseline = row
            else:
                diff_ratios = diff_http(
                    baseline['headers'], baseline['content'],
                    row['headers'], row['content']
                )
                print(" {0} {1}: headers {2}, content {3}".format(
                    type_arrow,
                    position,
                    diff_ratios[0],
                    diff_ratios[1]
                ))
                if diff_ratios[0] != 2:
                    print('\n\t'.join(
                        diff_text(baseline['headers'], row['headers'])
                    ))
                if diff_ratios[1] != 2:
                    print('\n\t'.join(
                        diff_text(baseline['content'], row['content'])
                    ))

if db_conn is not None:
    db_conn.close()
