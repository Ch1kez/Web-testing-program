from re import sub
from socket import gethostname


class TestResponse:
    def __init__(self, request, test_class, test_serializer_class, func_get_par, response_class, rest_status, target,
                 target_serializer):
        """
        :param request: query_param (полученный запрос от клиента)
        :param test_class: class (класс модели тестов)
        :param test_serializer_class: class (сериализация полей класса тестов)
        :param func_get_par: func (функция получения параметров запрошеного теста)
        :param response_class: class (класс ответа на запрос клиента)
        :param rest_status: module rest_framework.status (модуль из DRF для статус кода запроса)
        :param target: class (класс модели таргетов)
        :param target_serializer:(сериализация полей класса таргетов)
        :param tfa_dbg: bool
        """
        self.req = request
        self.func_get_par = func_get_par
        self.rest_status = rest_status

        self.target = target
        self.test_class = test_class
        self.response_class = response_class
        self.test_serializer_class = test_serializer_class
        self.target_serializer = target_serializer

        self.tfa_dbg = gethostname() == 'sts-tf_tfa'  # type: bool

    def get_test_165(self):
        """
        :return: Resonse (json-ответ или исключение, что страница с тестом не найдена )
        """
        tst_num = self.req.query_params.get('tst_num')
        trg = self.req.query_params.get('trg')
        save_log = self.req.query_params.get('save_log')

        # Получение данных из базы
        try:
            test_data = self.test_class.objects.get(id=tst_num)

            serializer = self.test_serializer_class(test_data)
            print('TEST_DATA', serializer.data)

            t_info = {"t_info": {"tsts": "СЭП 240",
                                 "tadr": "http://10.17.10.31:8080/pts/login",
                                 "tst_par": self.func_get_par(serializer.data.get('test_text'), trg, serializer),
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
                      "tst_arr": serializer.data
                      # Используем сериализованные данные
                      }
            return self.response_class(t_info)
        except self.test_class.DoesNotExist as ex:
            return self.response_class({"error": f"Test does not exist{ex}"},
                                       status=self.rest_status.HTTP_404_NOT_FOUND)

    def get_par_test(self, t_array, trgp, serializer_test):

        retv = {'tsts': 'СЭП ' + trgp, 'dbg': self.tfa_dbg}
        tst_start = ''
        eotts_macros = ["@ЗакрЭОТТС", "@ИнфЭОТТС", "@ПоискЭОТТС", "@РазворотЭОТТС", "@СвязиЭОТТС", "@СелекторЭОТТС",
                        "@ТаблЭОТТС", "@ПлюсЭОТТС", "@Прил2Настр_ЭОТТС", "@Прил2Зап_ЭОТТС", "@Прил2Разд_ЭОТТС",
                        "@Прил4_ЭОТТС", "@МинусЭОТТС", "@НастрЭОТТС", "@VIN_ЭОТТС", "@ЧекбоксЭОТТС"]

        # Ищем макросы ЭОТТС и определяем адрес площадки
        for cmd in t_array:
            if 'get' in cmd and tst_start == '':
                tst_start = cmd['get']
            if 'fnd' in cmd and cmd['fnd'] in eotts_macros:
                retv['tsts'] = 'ЭОТТС ' + trgp
        print('DADR', serializer_test.data.get('dadr'))
        target_data = self.target.objects.get(tname=retv['tsts'])
        serializer_target = self.target_serializer(target_data)
        int_ip = serializer_target.data.get('dadr') if retv['dbg'] else serializer_target.data.get('madr')
        print('saaaaaaaaaaaaaaa', int_ip)

        retv['tadr'] = int_ip + sub('(?i)^http.+?\.\d{1,3}(:8080)?/', '/', tst_start)

        return retv
