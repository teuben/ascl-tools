from db import init_db
import sys, codecs, pyPdf

def find_pdf_links(filename):
	pdf_file = open(filename)
	pdf = pyPdf.PdfFileReader(pdf_file)
	pdf_links = []
	pdf_pages = pdf.getNumPages()
	for i in range(pdf_pages):
		page = pdf.getPage(i).getObject()
		if page.has_key('/Annots'):
			for k in page['/Annots']:
				annot = k.getObject()
				if annot.has_key('/A') and annot['/A'].has_key('/URI'):
					pdf_links.append(annot['/A']['/URI'])
	return pdf_links

def filter_links(links):
	to_filter = ["http://www.aanda.org", "http://www.edpsciences.org",\
				 "http://dexter.edpsciences.org", "http://dx.doi.org",\
				 "http://linker.aanda.org", "http://arxiv.org",\
				 "http://adsabs.harvard.edu", "http://ui.adsabs.harvard.edu",\
				 "doi:", "DOI:", "mailto:", 'email:', "http://ascl.net", "ascl.net"]
	to_filter = zip(to_filter, [len(u) for u in to_filter])
	return [l for l in links if (not any([l[0:v] == u for u, v in to_filter])) and (l.find('@') == -1)]

def add_link(link, filename, paper_id, conn, sql):
	sql.execute("SELECT url FROM links WHERE url = ?", (link,))
	foo = sql.fetchone()
	if not foo:
		sql.execute("INSERT INTO links(url) VALUES (?)", (link,))
		conn.commit()
		link_id = sql.lastrowid
	else:
		sql.execute("SELECT id FROM links WHERE url = ?", (link,))
		link_id = sql.fetchone()[0]
	sql.execute("INSERT INTO links_papers(link_id, paper_id) VALUES (?, ?)", (link_id, paper_id))

def unpathify(filename):
	return filename.split('/')[-1].split('.')[0]

def process_papers(filenames):
	conn, sql = init_db()
	processed_files = 0
	added_links = 0
	errored_files = []
	for filename in filenames:
		print("Reading file {0}".format(filename))
		try:
			links = filter_links(find_pdf_links(filename))
		except pyPdf.utils.PdfReadError:
			print("Couldn't read file")
			errored_files.append(filename)
			continue
		filename_without_path = unpathify(filename)
		sql.execute("SELECT filename FROM papers WHERE papers.filename = ?", (filename_without_path,))
		if sql.fetchone():
			continue
		sql.execute("INSERT INTO papers(filename) VALUES (?)", (filename_without_path,))
		conn.commit()
		paper_id = sql.lastrowid
		for link in links:
			print("\tAdding link {0}".format(link))
			add_link(link, filename, paper_id, conn, sql)
		processed_files += 1
		added_links += len(links)
	conn.commit()
	conn.close()
	print("--- Complete! ---")
	print("Processed {0} files, added {1} links".format(processed_files, added_links))
	if len(errored_files) == 0:
		print("No file read errors!")
	elif len(errored_files) == 1:
		print("1 file read error:\n\t{0}".format(errored_files[0]))
	else:
		print("{0} file read errors:".format(len(errored_files)))
		for f in errored_files:
			print("\t" + f)

if __name__ == "__main__":
	process_papers(sys.argv[1:])
