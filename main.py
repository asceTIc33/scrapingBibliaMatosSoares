import sqlite3
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

booksChapters = {
    "genesis": 50,
    "exodo": 40,
    "levitico": 27,
    "numeros": 36,
    "deuteronomio": 34,
    "josue": 24,
    "juizes": 21,
    "rute": 4,
    "i-samuel": 31,
    "ii-samuel": 24,
    "i-reis": 22,
    "ii-reis": 25,
    "i-cronicas": 29,
    "ii-cronicas": 36,
    "esdras": 10,
    "neemias": 13,
    "tobias": 14,
    "judite": 16,
    "ester": 16,
    "jo": 42,
    "salmos": 150,
    "i-macabeus": 16,
    "ii-macabeus": 15,
    "proverbios": 31,
    "eclesiastes": 12,
    "cantico-dos-canticos": 8,
    "sabedoria": 19,
    "eclesiastico": 51,
    "isaias": 66,
    "jeremias": 52,
    "lamentacoes": 5,
    "baruc": 6,
    "ezequiel": 48,
    "daniel": 14,
    "oseias": 14,
    "joel": 3,
    "amos": 9,
    "abdias": 1,
    "jonas": 4,
    "miqueias": 7,
    "naum": 3,
    "habacuc": 3,
    "sofonias": 3,
    "ageu": 2,
    "zacarias": 14,
    "malaquias": 4,
    "sao-mateus": 28,
    "sao-marcos": 16,
    "sao-lucas": 24,
    "sao-joao": 21,
    "atos-dos-apostolos": 28,
    "romanos": 16,
    "i-corintios": 16,
    "ii-corintios": 13,
    "galatas": 6,
    "efesios": 6,
    "filipenses": 4,
    "colossenses": 4,
    "i-tessalonicenses": 5,
    "ii-tessalonicenses": 3,
    "i-timoteo": 6,
    "ii-timoteo": 4,
    "tito": 3,
    "filemon": 1,
    "hebreus": 13,
    "sao-tiago": 5,
    "i-sao-pedro": 5,
    "ii-sao-pedro": 3,
    "i-sao-joao": 5,
    "ii-sao-joao": 1,
    "iii-sao-joao": 1,
    "sao-judas": 1,
    "apocalipse": 22
}


def createDatabase():
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Verses (
        id INTEGER PRIMARY KEY,
        book TEXT,
        chapter INTEGER,
        verse INTEGER,
        text TEXT
    )
    ''')
    conn.commit()
    conn.close()


def saveVerse(book, chapter, verse, text):
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Verses (book, chapter, verse, text)
    VALUES (?, ?, ?, ?)
    ''', (book, chapter, verse, text))
    conn.commit()
    conn.close()


def scrapeChapter(browser, book, chapter):
    url = f'https://www.bibliacatolica.com.br/biblia-matos-soares-1956/{book}/{chapter}/'
    browser.get(url)
    sleep(2)

    verses = browser.find_elements(By.XPATH, "//section/article/section/p")
    for verse in verses:
        try:
            verseNumberElement = verse.find_element(By.TAG_NAME, "strong")
            verseNumber = verseNumberElement.text.strip().replace('.', '')
            verseText = verse.text[len(verseNumber):].strip()
            verseText = re.sub(r'^[\.\¶]+', '', verseText).strip()

            saveVerse(book, chapter, int(verseNumber), verseText)
        except Exception as e:
            print(f"Pulando parágrafo: {e}")
            continue


def main():
    createDatabase()
    browser = webdriver.Firefox()

    for book, chapters in booksChapters.items():
        for chapter in range(1, chapters + 1):
            print(f'Raspando {book} capítulo {chapter}')
            scrapeChapter(browser, book, chapter)

    browser.quit()


if __name__ == "__main__":
    main()