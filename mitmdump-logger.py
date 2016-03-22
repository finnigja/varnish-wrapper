from libmproxy.script import concurrent
import sqlite3
import uuid

# logs requests passing through mitmproxy into sqlite; tag requests with
# x-mitm-uuid header, to allow correlation if recurring

def start(context, argv):
    context.position = argv[1]
    context.db_conn = sqlite3.connect(
        'flows.db',
        check_same_thread=False  # allow reuse across mitmproxy instances
    )
    c = context.db_conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flows (
                 position text, method text, scheme text, host text,
                 port text, path text, headers text, context text,
                 uuid text)'''
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
    t = (context.position, flow.request.method, flow.request.scheme,
         flow.request.host, flow.request.port, flow.request.path,
         str(flow.request.headers), flow.request.content, req_uuid)
    c.execute('INSERT INTO flows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', t)
    context.db_conn.commit()
    flow.request.headers.set_all('x-mitm-uuid', (req_uuid,))
