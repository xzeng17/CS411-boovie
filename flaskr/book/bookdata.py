from .. import sql  
import urllib.request, json, time 

# http://books.google.com/books/feeds/volumes?q=a&max_results=40&start_index=1     

def init(conn):
    i = 1
    idSet = set()
    while i <= 500:
        with urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q=science&max_results=40&start_index="+str(i)) as url:
            data = json.loads(url.read().decode())
            if 'items' in data:
                books = data["items"]
                for book in books:                    
                    if book['id'] in idSet:
                        continue
                    idSet.add(book['id'])
                    pageCount = 0
                    title = 'N/A'
                    description = 'N/A'
                    publisher = 'N/A'
                    authors = 'N/A'
                    publishedDate = 'N/A'
                    imgLink = 'https://casperblog.imgix.net/blog/wp-content/uploads/2020/10/books-1200x880-1.png?auto=format'
                    if 'imageLinks' in book['volumeInfo']:
                        if 'thumbnail' in book['volumeInfo']['imageLinks']:
                            imgLink = book['volumeInfo']['imageLinks']['thumbnail']
                    if 'pageCount' in book['volumeInfo']:
                        pageCount = book['volumeInfo']['pageCount']
                    if 'authors' in book['volumeInfo']:
                        authors = (";").join(book['volumeInfo']['authors']).replace('"', '').replace('\\','')
                    if 'description' in book['volumeInfo']:
                        description = book['volumeInfo']['description'].replace('"', '').replace('\\','')
                    if 'publisher' in book['volumeInfo']:
                        publisher = book['volumeInfo']['publisher'].replace('"', '').replace('\\','')
                    if 'publishedDate' in book['volumeInfo']:
                        publishedDate = book['volumeInfo']['publishedDate']
                    if 'title' in book['volumeInfo']:
                        title = book['volumeInfo']['title'].replace('"', '').replace('\\','')
                    if 'industryIdentifiers' not in book['volumeInfo']:
                        continue
                        # industryIdentifiers = str(book['volumeInfo']['industryIdentifiers'][0]['identifier'])
                    values = [
                        book['id'],
                        str(book['volumeInfo']['industryIdentifiers'][0]['identifier']),
                        title,
                        authors,
                        book['volumeInfo']['language'],
                        imgLink,
                        publishedDate,
                        pageCount,
                        description,
                        publisher,
                    ]
                    sql.insert_values(conn, "Book", values)  
                i = i + 40
                print(i)
    time.sleep(360)  
    i = 1 
    while i <= 500:
        with urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q=country&max_results=40&start_index="+str(i)) as url:
            data = json.loads(url.read().decode())
            if 'items' in data:
                books = data["items"]
                for book in books:                    
                    if book['id'] in idSet:
                        continue
                    idSet.add(book['id'])
                    pageCount = 0
                    description = 'N/A'
                    publisher = 'N/A'
                    authors = 'N/A'
                    publishedDate = 'N/A'
                    title = 'N/A'
                    imgLink = 'https://5b0988e595225.cdn.sohucs.com/images/20200104/a8327f8ae16e495e9dc0df75f3b88837.png'
                    # 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.scientificamerican.com%2Fsciam%2Fcache%2Ffile%2F1DDFE633-2B85-468D-B28D05ADAE7D1AD8_source.jpg%3Fw%3D590%26h%3D800%26D80F3D79-4382-49FA-BE4B4D0C62A5C3ED&imgrefurl=https%3A%2F%2Fwww.scientificamerican.com%2Fpodcast%2Fepisode%2Funread-books-at-home-still-spark-literacy-habits%2F&tbnid=79SOCMHf7w5ODM&vet=12ahUKEwjT5aeB_cfzAhVVBM0KHePdCBoQMygBegUIARDQAQ..i&docid=DUTn4ZoS2heroM&w=590&h=431&itg=1&q=book&ved=2ahUKEwjT5aeB_cfzAhVVBM0KHePdCBoQMygBegUIARDQAQ'
                    if 'imgLinks' in book['volumeInfo']:
                        if 'thumbnail' in book['volumeInfo']['imageLinks']:
                            imgLink = book['volumeInfo']['imageLinks']['thumbnail']
                        elif 'smallThumbnail' in book['volumeInfo']['imageLinks']:
                            imgLink = book['volumeInfo']['imageLinks']['smallThumbnail']
                    if 'pageCount' in book['volumeInfo']:
                        pageCount = book['volumeInfo']['pageCount']
                    if 'authors' in book['volumeInfo']:
                        authors = (";").join(book['volumeInfo']['authors']).replace('"', '').replace('\\','')
                    if 'description' in book['volumeInfo']:
                        description = book['volumeInfo']['description'].replace('"', '').replace('\\','')
                    if 'publisher' in book['volumeInfo']:
                        publisher = book['volumeInfo']['publisher'].replace('"', '').replace('\\','')
                    if 'publishedDate' in book['volumeInfo']:
                        publishedDate = book['volumeInfo']['publishedDate']
                    if 'industryIdentifiers' not in book['volumeInfo']:
                        continue
                        industryIdentifiers = str(book['volumeInfo']['industryIdentifiers'][0]['identifier'])
                    if 'title' in book['volumeInfo']:
                        title = book['volumeInfo']['title'].replace('"', '').replace('\\','')
                    values = [
                        book['id'],
                        str(book['volumeInfo']['industryIdentifiers'][0]['identifier']),
                        title,
                        authors,
                        book['volumeInfo']['language'],
                        imgLink,
                        publishedDate,
                        pageCount,
                        description,
                        publisher,
                    ]
                    sql.insert_values(conn, "Book", values)  
                i = i + 40
    i = 1 
    while i <= 50:
        with urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q=classic&max_results=40&start_index="+str(i)) as url:
            data = json.loads(url.read().decode())
            if 'items' in data:
                books = data["items"]
                for book in books:                    
                    if book['id'] in idSet:
                        continue
                    idSet.add(book['id'])
                    pageCount = 0
                    description = 'N/A'
                    publisher = 'N/A'
                    authors = 'N/A'
                    publishedDate = 'N/A'
                    title = 'N/A'
                    imgLink = 'https://5b0988e595225.cdn.sohucs.com/images/20200104/a8327f8ae16e495e9dc0df75f3b88837.png'
                    # 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.scientificamerican.com%2Fsciam%2Fcache%2Ffile%2F1DDFE633-2B85-468D-B28D05ADAE7D1AD8_source.jpg%3Fw%3D590%26h%3D800%26D80F3D79-4382-49FA-BE4B4D0C62A5C3ED&imgrefurl=https%3A%2F%2Fwww.scientificamerican.com%2Fpodcast%2Fepisode%2Funread-books-at-home-still-spark-literacy-habits%2F&tbnid=79SOCMHf7w5ODM&vet=12ahUKEwjT5aeB_cfzAhVVBM0KHePdCBoQMygBegUIARDQAQ..i&docid=DUTn4ZoS2heroM&w=590&h=431&itg=1&q=book&ved=2ahUKEwjT5aeB_cfzAhVVBM0KHePdCBoQMygBegUIARDQAQ'
                    if 'imgLinks' in book['volumeInfo']:
                        if 'thumbnail' in book['volumeInfo']['imageLinks']:
                            imgLink = book['volumeInfo']['imageLinks']['thumbnail']
                        elif 'smallThumbnail' in book['volumeInfo']['imageLinks']:
                            imgLink = book['volumeInfo']['imageLinks']['smallThumbnail']
                    if 'pageCount' in book['volumeInfo']:
                        pageCount = book['volumeInfo']['pageCount']
                    if 'authors' in book['volumeInfo']:
                        authors = (";").join(book['volumeInfo']['authors']).replace('"', '').replace('\\','')
                    if 'description' in book['volumeInfo']:
                        description = book['volumeInfo']['description'].replace('"', '').replace('\\','')
                    if 'publisher' in book['volumeInfo']:
                        publisher = book['volumeInfo']['publisher'].replace('"', '').replace('\\','')
                    if 'publishedDate' in book['volumeInfo']:
                        publishedDate = book['volumeInfo']['publishedDate']
                    if 'industryIdentifiers' not in book['volumeInfo']:
                        continue
                        industryIdentifiers = str(book['volumeInfo']['industryIdentifiers'][0]['identifier'])
                    if 'title' in book['volumeInfo']:
                        title = book['volumeInfo']['title'].replace('"', '').replace('\\','')
                    values = [
                        book['id'],
                        str(book['volumeInfo']['industryIdentifiers'][0]['identifier']),
                        title,
                        authors,
                        book['volumeInfo']['language'],
                        imgLink,
                        publishedDate,
                        pageCount,
                        description,
                        publisher,
                    ]
                    sql.insert_values(conn, "Book", values)  
                i = i + 40
                print(i)               
    return "123"
