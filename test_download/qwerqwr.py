from rest_framework.response import Response
from base.api.models import *

class Get_response():
    def __int__(self, req):
        self.request = req

    def request_to_db(self, request):
        tst_num = request.query_params.get('tst_num')
        trg = request.query_params.get('trg')
        save_log = request.query_params.get('save_log')

        # Вытащить данных после распарса словаря !!
        t_array = Test.from_db().filter(id=tst_num).values()

        # Далее ваша логика обработки параметров запроса и формирование данных в формате JSON
        # Пример:
        t_info = {
            "t_info": {
                "tsts": "СЭП 240",
                "tadr": "http://10.17.10.31:8080/pts/login",
                "tst_par": self.get_par_test(t_array, trg),
                "dbg": True,
                "headless": False,
                "var_arr": {},
                "cur_step": 0,
                "cur_cmd": "",
                "drv": None,
                "prx": None,
                "log_arr": {},
                "log_ajax": {}
            },
            "tst_arr": self.open_test_bd(tst_num)}

        return Response(t_info)

    def open_test_bd(test_id):
        # Ваша логика извлечения данных из базы данных
        pass

    def get_par_test(t_array, trgp):
        # Ваша логика обработки данных для формирования JSON
        pass
