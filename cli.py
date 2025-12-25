# argparse — стандартная библиотека Python
# используется для создания интерфейса командной строки (CLI).
import argparse
# requests — библиотека для отправки HTTP-запросов к серверу.
import requests


# Базовый URL сервера.
# CLI будет отправлять запросы именно по этому адресу.
BASE_URL = "http://localhost:8000"


# Создаём основной парсер аргументов командной строки.
parser = argparse.ArgumentParser(description="Function Server CLI")
# Добавляем поддержку подкоманд (list, get, exec, create).
sub = parser.add_subparsers(dest="cmd")



# Команда list — получение списка всех функций
sub.add_parser("list")

# Команда get — получение описания функции по имени
get_p = sub.add_parser("get")
get_p.add_argument("name", help="Имя функции")

# Команда exec — вычисление значения функции
exec_p = sub.add_parser("exec")
exec_p.add_argument("name", help="Имя функции")
exec_p.add_argument("--x", type=float, required=True, help="Значение переменной x")

# Команда create — создание новой функции
create_p = sub.add_parser("create")
create_p.add_argument("name", help="Имя функции")
create_p.add_argument("--inputs", nargs="+", required=True, help="Список входных переменных")
create_p.add_argument("--outputs", nargs="+", required=True, help="Список выходных переменных")
create_p.add_argument("--params", nargs="+", required=True, help="Параметры в формате a=2 b=1")
create_p.add_argument("--expr", required=True, help="Выражение функции, например: a*x+b")

# Разбираем аргументы командной строки
args = parser.parse_args()






# Преобразует список параметров вида: ["a=2", "b=1"]
# в словарь: {"a": 2.0, "b": 1.0}
def parse_params(params_list):
    params = {}
    for p in params_list:
        if "=" in p:
            key, value = p.split("=")
            params[key] = float(value)
    return params



# Команда list — получить список всех функций
if args.cmd == "list":
    resp = requests.get(f"{BASE_URL}/functions")
    print(resp.json())

# Команда get — получить описание функции
elif args.cmd == "get":
    resp = requests.get(f"{BASE_URL}/functions/{args.name}")
    print(resp.json())

# Команда exec — вычислить значение функции
elif args.cmd == "exec":
    resp = requests.post(
        f"{BASE_URL}/functions/{args.name}/execute",
        json={"inputs": {"x": args.x}}
    )
    print(resp.json())

# Команда create — создать новую функцию
elif args.cmd == "create":
    payload = {
        "name": args.name,
        "inputs": args.inputs,
        "outputs": args.outputs,
        "parameters": parse_params(args.params),
        "expression": args.expr
    }
    resp = requests.post(f"{BASE_URL}/functions", json=payload)
    print(resp.json())
