# Выполнение автотестов, разработанных для FTACommander

1. Создаем вирт. окружение
python -m venv .venv

.venv\Scripts\Activate.ps1

source .venv/bin/activate

pip install selenium --no-index --find-links d:\Ivanov\whl\
pip install typing_extensions --no-index --find-links d:\Ivanov\whl\
pip install webdriver-manager --no-index --find-links d:\Ivanov\whl\
pip install browsermob-proxy --no-index --find-links d:\Ivanov\whl\


1. Прогнать простой тест

https://stackoverflow.com/questions/48201944/how-to-use-browsermob-with-python-selenium
https://bmp.lightbody.net/

Download the browsermob-proxy binaries browsermob-proxy-2.1.4-bin form the following url :



---
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal