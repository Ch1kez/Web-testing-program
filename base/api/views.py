from re import sub
from socket import gethostname

from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Mail, Target, Tuser, WebsiteTable
from .models import Test
from .serializers import (
    MailSerializer, TargetSerializer, TuserSerializer, WebsiteTableSerializer
)
from .serializers import TestSerializer


@api_view(['GET'])
def custom_response(request):
    print(request.query_params)
    tst_num = request.query_params.get('tst_num')
    trg = request.query_params.get('trg')
    save_log = request.query_params.get('save_log')

    # Получение данных из базы
    try:
        test_data = Test.objects.get(id=tst_num)

        serializer = TestSerializer(test_data)
        print('TEST_DATA', serializer.data)

        t_info = {
            "t_info": {
                "tsts": "СЭП 240",
                "tadr": "http://10.17.10.31:8080/pts/login",
                "tst_par": get_par_test(serializer.data.get('test_text'), trg, serializer),
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
            "tst_arr": serializer.data  # Используем сериализованные данные
        }
        return Response(t_info)
    except Test.DoesNotExist as ex:
        return Response({"error": f"Test does not exist{ex}"}, status=status.HTTP_404_NOT_FOUND)


def tfa_dbg():
    return gethostname() == 'sts-tf_tfa'


def get_par_test(t_array, trgp, serializer_test):
    retv = {'tsts': 'СЭП ' + trgp, 'dbg': tfa_dbg()}
    tst_start = ''
    eotts_macros = ["@ЗакрЭОТТС", "@ИнфЭОТТС", "@ПоискЭОТТС", "@РазворотЭОТТС", "@СвязиЭОТТС",
                    "@СелекторЭОТТС", "@ТаблЭОТТС", "@ПлюсЭОТТС", "@Прил2Настр_ЭОТТС", "@Прил2Зап_ЭОТТС",
                    "@Прил2Разд_ЭОТТС", "@Прил4_ЭОТТС", "@МинусЭОТТС", "@НастрЭОТТС", "@VIN_ЭОТТС", "@ЧекбоксЭОТТС"]

    # Ищем макросы ЭОТТС и определяем адрес площадки
    for cmd in t_array:
        if 'get' in cmd and tst_start == '':
            tst_start = cmd['get']
        if 'fnd' in cmd and cmd['fnd'] in eotts_macros:
            retv['tsts'] = 'ЭОТТС ' + trgp
    print('DADR', serializer_test.data.get('dadr'))
    target_data = Target.objects.get(tname=retv['tsts'])
    serializer_target = TargetSerializer(target_data)
    int_ip = serializer_target.data.get('dadr') if retv['dbg'] else serializer_target.data.get('madr')
    print('saaaaaaaaaaaaaaa', int_ip)

    retv['tadr'] = int_ip + sub('(?i)^http.+?\.\d{1,3}(:8080)?/', '/', tst_start)

    return retv


def api_home(request):
    # Ваша логика представления для страницы API
    return render(request, 'api_home.html')


def api_tables(request):
    # Ваша логика представления для страницы API
    return render(request, 'api_tabels.html')


# Представление для модели Mail
class MailListCreateView(generics.ListCreateAPIView):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer


class MailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer


# Представление для модели Target
class TargetListCreateView(generics.ListCreateAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class TargetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


# Представление для модели Test
class TestListCreateView(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


# Представление для модели Tuser
class TuserListCreateView(generics.ListCreateAPIView):
    queryset = Tuser.objects.all()
    serializer_class = TuserSerializer


class TuserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tuser.objects.all()
    serializer_class = TuserSerializer


# Представление для модели WebsiteTable
class WebsiteTableListCreateView(generics.ListCreateAPIView):
    queryset = WebsiteTable.objects.all()
    serializer_class = WebsiteTableSerializer


class WebsiteTableDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WebsiteTable.objects.all()
    serializer_class = WebsiteTableSerializer

if __name__ == '__main__':
    pass
