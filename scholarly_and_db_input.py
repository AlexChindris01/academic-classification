from scholarly import scholarly, ProxyGenerator
import mariadb
import sys
# de la aceste functii se poate porni pentru a extrage date folosind scholarly,
# inlocuind afisarea cu scholarly.pprint cu o metoda de colectare a informatiei
# intr-o variabila pentru a fi returnata.

# pg = ProxyGenerator()
# pg.FreeProxies()
# scholarly.use_proxy(pg)
# aceste trei linii sunt optionale


def search_author_by_name(query):
    # exemplu de utilizare:
    # search_author_by_name('Steven A Cholewiak')
    search_query = scholarly.search_author(query)
    author = next(search_query, None)
    while author is not None:
        scholarly.pprint(author)  # sau, mai multe informatii: scholarly.pprint(scholarly.fill(author))
        author = next(search_query, None)


def search_author_by_id(query):
    # exemplu de utilizare:
    # search_author_by_id('Smr99uEAAAAJ')
    author = scholarly.search_author_id(query)
    scholarly.pprint(scholarly.fill(author))
    first_pub = scholarly.fill(author)['publications'][0]
    print(first_pub['bib']['citation'].split(",")[0])


def search_pub(query):
    # exemplu de utilizare:
    # search_pub('Perception of physical stability and center of mass of 3D objects')
    search_query = scholarly.search_pubs(query)
    pub = next(search_query, None)
    while pub is not None:
        scholarly.pprint(pub)  # sau, mai multe informatii: scholarly.pprint(scholarly.fill(pub))
        pub = next(search_query, None)


def citations(query):
    # exemplu de utilizare:
    # search_query = scholarly.search_pubs('Perception of physical stability and center of mass of 3D objects')
    # pub = next(search_query, None)
    # citations(pub)
    search_query = scholarly.citedby(query)
    pub = next(search_query, None)
    while pub is not None:
        scholarly.pprint(pub)  # sau, mai multe informatii: scholarly.pprint(scholarly.fill(pub))
        pub = next(search_query, None)


# search_author_by_id('Vqm7_msAAAAJ')
# handling data from scholarly in detail:
author = scholarly.search_author_id('Vqm7_msAAAAJ')
first_pub = scholarly.fill(author)['publications'][0]
journal1 = first_pub['bib']['citation'].split(",")[0]
title1 = first_pub['bib']['title']
try:
    conn = mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="academic-classification"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cursor = conn.cursor()
try:
    cursor.execute(
        "INSERT INTO gst_pub(title, journal) VALUES (?, ?)",
        (title1, journal1))
except mariadb.Error as e:
    print(f"Error: {e}")
conn.commit()
print(title1, journal1, sep="\n")
