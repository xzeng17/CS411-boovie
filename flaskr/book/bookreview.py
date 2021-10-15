from .. import sql  
from essential_generators import DocumentGenerator
import urllib.request, json, time

def init(conn):
    gen = DocumentGenerator()
    i = 1
    while i <= 1000:
        id = gen.guid()
        content = gen.paragraph()
        isbn = gen.small_int()
        email = gen.email()
        template = [
            id,
            content.replace('"', '').replace('\\',''),
            isbn,
            email
        ]
        # gen.set_template(template)
        # documents = gen.documents(1)
        print(template)
        sql.insert_values(conn, "BookReview", template)
        i = i + 1
    return "123"