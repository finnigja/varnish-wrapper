from libmproxy.script import concurrent
import sqlite3
import uuid

# logs requests passing through mitmproxy into sqlite; tag requests with
# x-mitm-uuid header, to allow correlation if recurring

def start(context, argv):
    context.position = argv[1]
    context.content_limit = -1  # can use this to limit content stored
    context.db_conn = sqlite3.connect(
        'flows.db',
        check_same_thread=False  # allow reuse across mitmproxy instances
    )
    c = context.db_conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS request (
                 position text, method text, scheme text, host text,
                 port text, path text, headers blob, content blob,
                 uuid text, time text)'''
             )
    c.execute('''CREATE TABLE IF NOT EXISTS response (position text,
                 http_version text, status_code text, reason text,
                 headers blob, content blob, uuid text, time text)'''
             )
    context.db_conn.commit()
    context.log('{0} initialized ({1})'.format(argv[0], argv[1]))

def done(context):
    if context.db_conn is not None:
        context.db_conn.close()

@concurrent
def request(context, flow):
    c = context.db_conn.cursor()
    req_uuid = flow.request.headers.pop('x-mitm-uuid', str(uuid.uuid4()))
    req_time = flow.request.headers.pop('x-mitm-time', str(flow.request.timestamp_start))
    t = (context.position, flow.request.method, flow.request.scheme,
         flow.request.host, flow.request.port, flow.request.path,
         sqlite3.Binary(unicode(flow.request.headers)),
         sqlite3.Binary(flow.request.get_decoded_content()), req_uuid, req_time)
    c.execute('INSERT INTO request VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', t)
    context.db_conn.commit()
    flow.request.headers.set_all('x-mitm-uuid', (req_uuid,))
    flow.request.headers.set_all('x-mitm-time', (req_time,))

@concurrent
def response(context, flow):
    c = context.db_conn.cursor()
    req_uuid = flow.request.headers.pop('x-mitm-uuid')
    req_time = flow.request.headers.pop('x-mitm-time')
    t = (context.position, flow.response.http_version,
         flow.response.status_code, flow.response.reason,
         sqlite3.Binary(unicode(flow.response.headers)),
         sqlite3.Binary(flow.response.get_decoded_content()[0:context.content_limit]), req_uuid, req_time)
    c.execute(u'INSERT INTO response VALUES (?, ?, ?, ?, ?, ?, ?, ?)', t)
    context.db_conn.commit()
