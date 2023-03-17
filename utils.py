import urllib.request
import json


# function to return the auth key
def return_auth_key(s):
    url = 'https://openlibrary.org/search/authors.json?q=' + \
        ('+'.join(s.split(' ')))

    response = urllib.request.urlopen(url)
    data = response.read()
    dict_auth = json.loads(data)
    auth_key = dict_auth['docs'][0]['key']
    return auth_key


# function to return the auth bio
def return_auth_bio(auth_key):
    url = f'https://openlibrary.org/authors/{auth_key}.json'
    response = urllib.request.urlopen(url)
    data = response.read()
    auth_bio = json.loads(data)
    return auth_bio

# function to return the works


def return_auth_works(auth_key):
    url = f'https://openlibrary.org/authors/{auth_key}/works.json'
    response = urllib.request.urlopen(url)
    data = response.read()
    auth_works = json.loads(data)
    return auth_works


def return_all_isbn(author_books):
    dict_isbn = {}
    for bk in author_books:
        for book in bk['books']:
            # print(book['isbn'])
            dict_isbn[book['title']] = '0' + \
                book['isbn'] if len(book['isbn']) < 10 else book['isbn']
    return dict_isbn


def return_amazon_links(dict_isbn):
    amazon_id = {}

    for title, isbn in dict_isbn.items():
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"

        try:
            response = urllib.request.urlopen(url)
            data = response.read()
            dict_book = json.loads(data)
            key1 = list(dict_book.keys())[0]
            iden = dict_book[key1]['identifiers']['amazon'][-1]
            # print(iden)
            if iden != '':
                amazon_id[title] = (iden)
        except:
            # print('no data')
            pass

    return amazon_id


def return_amazon_works(rowling_books):
    work_title_keys = {}
    for bk in rowling_books:
        works = (bk['works']['entries'])
        for work in works:
            work_title_keys[work['title']] = work['key']

    work_title_links = {}
    for title, work_id in work_title_keys.items():
        url = f'https://openlibrary.org{work_id}/editions.json'
        response = urllib.request.urlopen(url)
        data = response.read()
        dict_editions_info = json.loads(data)
        editions = dict_editions_info['entries']

        print(title)
        for edition in editions:
            try:
                for link in edition['source_records']:
                    if(link[:7] == 'amazon:'):
                        print(link[7:])
                        work_title_links[title] = link[7:]
                        break

            except:
                print('no data')

            else:
                break

    return work_title_links
