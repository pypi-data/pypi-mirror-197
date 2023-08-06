# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_books_api_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['certifi==2022.12.7',
 'charset-normalizer==3.0.1',
 'idna==3.4',
 'requests==2.28.2',
 'urllib3==1.26.14']

setup_kwargs = {
    'name': 'google-books-api-wrapper',
    'version': '1.0.0',
    'description': 'A simple and easy to use wrapper around the Google Books Web API.',
    'long_description': '# Google Books API Wrapper for Python\n\nThis package wraps the [Google Books API](https://developers.google.com/books) in an easy to use Python interface. Use it to find comprehensive data on all books that peak your interest.\n\nBegin by installing the package:\n\n```bash\npip install google-books-api-wrapper\n```\n\nthen import the required configuration object,\n\n```python\nfrom google_books_api_wrapper.api import GoogleBooksAPI\n```\n\nYou can now use this object to **search** and **retreive** books,\n\n```python\n>>> client = GoogleBooksAPI()\n\n>>> client.get_book_by_title("IT")\nBook(title=It, authors=[\'Stephen King\'])\n\n>>> client.get_book_by_isbn13("9780670813025")\nBook(title=It, authors=[\'Stephen King\'])\n\n>>> client.get_book_by_isbn10("0670813028")\nBook(title=It, authors=[\'Stephen King\'])\n\n>>> simon_schuster_books = client.get_books_by_publisher("Simon & Schuster")\n>>> simon_schuster_books.get_all_results()[:3]\n[Book(title=Simon & Schuster\'s Guide to Dogs, authors=[\'Gino Pugnetti\']), Book(title=Frankenstein, authors=[\'Mary Shelley\']), Book(title=Why We Buy, authors=[\'Paco Underhill\'])]\n\n>>> fiction_books = client.get_books_by_subject("Fiction")\n>>> fiction_books.get_all_results()[:3]\n[Book(title=Lord of the Flies, authors=[\'William Golding\']), Book(title=Amish Snow White, authors=[\'Rachel Stoltzfus\']), Book(title=The Odyssey of Homer, authors=[\'Richmond Lattimore\'])]\n\n>>> stephen_king_books = client.get_books_by_author("Stephen King")\n>>> stephen_king_books.total_results #Read Below about book return limit\n40\n\n>>> stephen_king_books.get_all_results()[:3]\n[Book(title=It, authors=[\'Stephen King\']), Book(title=1922, authors=[\'Stephen King\']), Book(title=Elevation, authors=[\'Stephen King\'])]\n```\n',
    'author': 'dankrzeminski32',
    'author_email': 'dankrzeminski32@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://dankrzeminski32.github.io/google-books-api-wrapper/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
