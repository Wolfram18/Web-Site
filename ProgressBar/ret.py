import cgi
storage = cgi.FieldStorage()
data = storage.getvalue('number')
print('Status: 200 OK')
print('Content-Type: text/plain')
print('')
print(data)
