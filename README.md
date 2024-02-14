# Проект парсинга pep
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Practicum.Yandex](https://img.shields.io/badge/-Practicum.Yandex-464646?style=flat&logo=Practicum.Yandex&logoColor=56C0C0&color=008080)](https://practicum.yandex.ru/)
# Парсер документации python и PEP
## Описание
Парсер информации о python с **https://docs.python.org/3/** и **https://peps.python.org/**
### Для использования
Клонируйте репозиторий:

```
git clone git@github.com:Iv-EN/bs4_parser_pep.git
```
В корневой папке создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate
```
Установите зависимости
```
pip install -r requirements.txt
```
### перейдите в директорию src
```
cd src/
```
### запустите файл main.py
```
python main.py [вариант парсера] [аргументы]
```
### варианты парсеров:
- whats-new   
Парсер выводящий спсок изменений в python.
```
python main.py whats-new [аргументы]
```
- latest_versions
Парсер выводящий список версий python и ссылки на их документацию.
```
python main.py latest-versions [аргументы]
```
- download   
Парсер скачивающий zip архив с документацией python в pdf формате.
```
python main.py download [аргументы]
```
- pep
Парсер выводящий список статусов документов pep
и количество документов в каждом статусе. 
```
python main.py pep [аргументы]
```
### Аргументы
Есть возможность указывать аргументы для изменения работы программы:   
- -h, --help
Общая информация о командах.
```
python main.py -h
```
- -c, --clear-cache
Очистка кеша перед выполнением парсинга.
```
python main.py [вариант парсера] -c
```
- -o {pretty,file}, --output {pretty,file}   
Дополнительные способы вывода данных   
pretty - выводит данные в командной строке в таблице   
file - сохраняет информацию в формате csv в папке ./results/
```
python main.py [вариант парсера] -o file
```
### Автор
- [Евгений Иванов](https://github.com/Iv-EN)