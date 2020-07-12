# HTTP(S) Проски
###### Автор: hastyulia

### Описание
> Данное приложение является реализацией прокси-сервера
### Состав
##### Модули:
- proxy.py
- adblock.py
- asyn_proxy.py
- http_protocol.py
- https_protocol.py
- asyn_proxy_child.py

##### Тесты:  
- test_http.py
- test_https.py
- test_proxy.py
- test_adblock.py
- test_asyn_proxy.py
- test_asyn_proxy_child.py

##### Пример запуска в многопоточном режиме: 
> ~$ python3 main.py thread

##### Пример запуска в асинхронном режиме: 
> ~$ python3 main.py async

В модуле adblock реализован блокировщик рекламы.
В модуле http_protocol реализована обработка http запросов.
В модуле https_protocol реализована обработка https запросов.
В модуле asyn_proxy реализован асинхронная обработка запросов.
В модуле proxy реализована обработка запросов и их содержимого.
В модуле asyn_proxy_child описан протокол HTTP, основанный на asyncio.BaseProtocol.

На модули (http_protocol.py, https_protocol.py, proxy.py, adblock.py, asyn_proxy.py, asyn_proxy_child.py) написаны тесты, их можно найти в папке test/.

##### Покрытие
Покрытие по строкам составляет около 87%:

    proxy.py                        85% lines covered
    adblock.py                      95% lines covered
    asyn_proxy.py	                84% lines covered
    http_protocol.py                100% lines covered
    https_protocol.py               82% lines covered
    asyn_proxy_child.py       87% lines covered
    
