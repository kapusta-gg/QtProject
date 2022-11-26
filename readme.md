# QtPLayer
____
## Проект представляет собой простенький плеер для Windows на PyQt.
#### Реализованы функции:
1) Добавления трека в коллекцию
2) Просмотр всех треков в папке проекта
3) Возможность переключать треки и менять громкость

#### Все библиотеки нужные для запуска проекта представлены в файле requirement.txt.

#### Для запуска проекта нужно иметь:
1) Windows(т.к. используется библиотека для работы именно с этой OS)
2) Python3.9 и выше

#### Порядок действий для запуска проекта:
1) Открыть командную строку
2) Распаковать zip-файл куда вам будет удобно
3) Перейти с помощью командной строки в папку проекта
   1) Для перемещения по папкам используйте
   ```cd *Путь до папки*```
   2) Для перемещения по дискам используйте
   ```*Название диска*:```
4) Использовать команду для создания окружения:  
``` python -m venv venv ```  
Если после этого не появилась папка __venv__ в проекте, то вручную указывайте путь до python.exe и путь до проекта  
```*путь до python.exe* -m venv *путь до проекта* ```   
_Например:_  
```C:\Users\bogda\AppData\Local\Programs\Python\Python39\python -m venv D:\QtProject-master\venv```
5) После используйте команду для активации среды:  
```venv\Scripts\activate.bat ```  
Если все прошло успешно, то у вас должно было появиться напротив пути проекта слово __venv__. Как пример:  
```(venv) D:\QtProject-master> ```
6) Установите все нужные библиотеки с помощью команды ниже:  
```pip install -r requirements.txt```
7) для запуска проекта просто напишете название главного файла. В нашем случае это файл ```main.py``` 

Для повторного запуска проекта, если вы вышли из командной строки, повторите шаги 3, 5, 7