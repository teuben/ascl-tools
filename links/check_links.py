from db import init_db
import datetime, urllib2, ssl

def store_result(id, code, msg, conn, sql):
	sql.execute("INSERT INTO checks(datetime, code, message, link) VALUES(?,?,?,?)", (datetime.datetime.now(), str(code), msg, int(id)))
	conn.commit()

class NotHTTPException(Exception):
	pass

def check_link(id, url):
	if url[:3] == 'ftp':
		raise NotHTTPException("FTP links are currently unsupported")
	if url[:4] != 'http':
		print(url)
		url = "http://" + url
	req = urllib2.Request(url)
	e = ''
	try:
		res = urllib2.urlopen(req)
		code = res.getcode()
	except urllib2.HTTPError as e:
		code = e.code
	except urllib2.URLError as e:
		code = -1
	except ssl.CertificateError as e:
		code = -2
	except urllib2.socket.error as e:
		code = -3
	except urllib2.httplib.BadStatusLine as e:
		code = -4
	except ValueError as e:
		code = -5
	return (id, code, str(e))

if __name__ == "__main__":
	conn, sql = init_db()
	links = conn.execute("SELECT id, url FROM links")
	for link in links:
		print(link)
		try:
			id, code, msg = check_link(link[0], link[1])
		except NotHTTPException as e:
			print("\t{0}".format(e.message))
			continue
		if code != 200:
			print("\t{0} {1}".format(code, msg))
		store_result(id, code, msg, conn, sql)
	conn.commit()
	conn.close()
