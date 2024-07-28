﻿# LLMui-clone

LLMui-clone - это веб-приложение для общения с ботом на основе модели языка GPT. В этом проекте используется Flask для создания серверной части и JavaScript для клиентской части. Также реализована возможность подсветки синтаксиса с помощью Prism.js.

## Функциональные возможности

- Создание новых чатов
- Удаление чатов
- Отправка и получение сообщений
- Подсветка синтаксиса в сообщениях с кодом

## Технологии

- Flask
- SQLAlchemy
- JavaScript
- Prism.js

## Установка упрощенная
1. Найдите кнопку "Code":
На странице репозитория найдите зеленую кнопку "Code" (обычно расположена в правом верхнем углу списка файлов репозитория).

2. Скачайте ZIP-архив:
Нажмите на кнопку "Code".
В выпадающем меню выберите опцию "Download ZIP".
Начнется загрузка ZIP-архива с содержимым репозитория.

3. Распакуйте ZIP-архив:
После завершения загрузки найдите скачанный ZIP-архив на своем компьютере.
Распакуйте архив с помощью любого архиватора, установленного на вашем компьютере (например, встроенного архиватора Windows, macOS, или стороннего архиватора, такого как WinRAR или 7-Zip).

4. Запустите файл chat_start.bat

## Установка

1. Клонируйте репозиторий на локальный компьютер:
    ```bash
    git clone https://github.com/username/chatgpt-clone.git
    cd chatgpt-clone
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте: venv\Scripts\activate
    ```

3. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Запустите приложение:
    ```bash
    python app.py
    ```

5. Откройте браузер и перейдите по адресу [http://localhost:5000](http://localhost:5000).

## Структура проекта

chatgpt-clone/
├── static/
│ ├── style.css
│ └── script.js
├── templates/
│ └── index.html
├── app.py
├── requirements.txt
└── README.md


## Конфигурация

- `app.py`: Основной файл приложения Flask.
- `static/style.css`: Файл стилей для приложения.
- `static/script.js`: Основной файл JavaScript для клиентской логики.
- `templates/index.html`: Основной HTML шаблон.

## Использование

### Создание нового чата

Для создания нового чата нажмите на кнопку "+" в панели истории чатов.

### Удаление текущего чата

Для удаления текущего чата нажмите на кнопку "🗑️" в панели истории чатов.

### Отправка сообщения

Для отправки сообщения введите текст в поле ввода в нижней части экрана и нажмите Enter.

### Подсветка синтаксиса

Для отображения сообщений с подсветкой синтаксиса используйте теги `<pre><code class="language-<язык>">...</code></pre>`. Например:

```html
<pre><code class="language-python">
# Пример кода на Python
def greet(name):
    print(f"Hello, {name}!")
   
greet("World")
</code></pre>
