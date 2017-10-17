import sqlite3

def init_db():
	sqlite_db_path = './links.sqlite'
	conn = sqlite3.connect(sqlite_db_path)
	sql = conn.cursor()
	sql.execute('CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, url VARCHAR(255) UNIQUE NOT NULL)')
	sql.execute('CREATE TABLE IF NOT EXISTS papers (id INTEGER PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL)')
	sql.execute('CREATE TABLE IF NOT EXISTS links_papers (id INTEGER PRIMARY KEY, link_id INTEGER NOT NULL, paper_id INTEGER NOT NULL, FOREIGN KEY(link_id) REFERENCES links(id), FOREIGN KEY(paper_id) REFERENCES papers(id))')
	sql.execute('CREATE TABLE IF NOT EXISTS checks (id INTEGER PRIMARY KEY, datetime DATETIME NOT NULL, code INTEGER NOT NULL, message VARCHAR(255), link INTEGER NOT NULL, FOREIGN KEY(link) REFERENCES links(id))')
	return (conn, sql)

if __name__ == '__main__':
	conn, sql = init_db()
	conn.commit()
	conn.close()
