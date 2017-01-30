def save_hashtag(hashtag, connection):
    hashtag_entry = [(hashtag.word, hashtag.filename, hashtag.phrase)]
    connection.executemany('INSERT INTO hashtags VALUES (?, ?, ?)', hashtag_entry)


def print_contents_of_table(connection):
    connection.execute('SELECT * FROM hashtags ORDER BY word')
    results = connection.fetchall()
    for result in results:
        print(result)
