from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

# Инициализация браузера
browser = webdriver.Firefox()

# Открытие главной страницы Википедии
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
assert 'Википедия' in browser.title
time.sleep(5)


# Поиск по запросу
search_box = browser.find_element(By.ID, 'searchInput')
search_query = input('Поиск: ')
search_box.send_keys(search_query)

# Найдем кнопку поиска и кликнем на неё
search_button = browser.find_element(By.ID, 'searchButton')
search_button.click()

time.sleep(5)

# Функция для вывода параграфов
def print_paragraphs():
    paragraphs = browser.find_elements(By.TAG_NAME, 'p')
    for paragraph in paragraphs:
        print(paragraph.text)
    input("Нажмите Enter для продолжения...")

# Функция для поиска связанных статей (hatnotes)
def find_hatnotes():
    hatnotes = []
    for element in browser.find_elements(By.CLASS_NAME, 'hatnote'):
        if 'navigation-not-searchable' in element.get_attribute('class'):
            hatnotes.append(element)
    return hatnotes

# Основной цикл программы
while True:
    print("\nЧто хотите сделать?")
    print("1. Листать параграфы текущей статьи")
    print("2. Перейти на одну из связанных страниц")
    print("3. Выход")

    try:
        answer = int(input("Выберите действие (1/2/3): "))
    except ValueError:
        print("Пожалуйста, введите 1, 2 или 3.")
        continue

    if answer == 1:
        # Вывести параграфы текущей статьи
        print_paragraphs()

    elif answer == 2:
        # Поиск hatnotes (связанных ссылок на другие статьи)
        hatnotes = find_hatnotes()
        if not hatnotes:
            print("Связанные страницы не найдены.")
            continue

        # Случайным образом выбираем hatnote
        hatnote = random.choice(hatnotes)

        # Поиск ссылки внутри hatnote и переход по ней
        try:
            link_element = hatnote.find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href")
            print(f"Переход по ссылке: {link}")
            browser.get(link)
            time.sleep(5)
        except Exception as e:
            print(f"Ошибка при переходе по ссылке: {e}")

    elif answer == 3:
        # Выход из программы
        print("Выход из программы.")
        break

    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

# Завершение работы браузера
browser.quit()
