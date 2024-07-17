import json
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE
from mongoengine.errors import NotUniqueError

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}

class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField())  # Знімаємо обмеження на довжину тегів
    quote = StringField()
    meta = {"collection": "quotes"}

def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors = json.load(f)
        for author_data in authors:
            try:
                author = Author(
                    fullname=author_data['fullname'],
                    born_date=author_data['born_date'],
                    born_location=author_data['born_location'],
                    description=author_data['description']
                )
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує: {author_data['fullname']}")

def load_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes = json.load(f)
        for quote_data in quotes:
            try:
                author = Author.objects.get(fullname=quote_data['author'])
                quote = Quote(
                    author=author,
                    tags=quote_data['tags'],  # Зберігаємо теги без обрізання
                    quote=quote_data['quote']
                )
                quote.save()
            except Author.DoesNotExist:
                print(f"Автор не знайдено: {quote_data['author']}")

if __name__ == "__main__":
    connect(db="hw", host="mongodb://localhost:27017")

    load_authors()
    load_quotes()

    print("Data loaded into MongoDB")
