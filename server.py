# HTTPException — специальное исключение,
# чтобы удобно возвращать HTTP‑ошибки (404, 400 и т.п.).
from fastapi import FastAPI, HTTPException
# BaseModel — базовый класс Pydantic для описания
# схем данных (валидация, сериализация в JSON).
from pydantic import BaseModel
# Dict, List, Optional — типы из typing:
# Dict[Ключ, Значение], List[Тип], Optional[Тип или None].
from typing import Dict, List, Optional
# Импортируем общее хранилище функций из модуля storage.
# В этом словаре сервер хранит все созданные функции.
from storage import functions



# Модель параметризованной функции.
# Содержит описание функции, её входных и выходных переменных, параметров и математического выражения.
class Function(BaseModel):
    name: str                    # имя функции
    inputs: List[str]            # список входных переменных
    outputs: List[str]           # список выходных переменных
    parameters: Dict[str, float] # параметры функции
    expression: str              # выражение функции в виде строки

# Модель запроса обновления функции.
# Позволяет изменить параметры и/или выражение функции.
# Все поля являются необязательными.
class UpdateRequest(BaseModel):
    parameters: Optional[Dict[str, float]] = None
    expression: Optional[str] = None

# Модель запроса вычисления функции.
# Содержит значения входных переменных, необходимых для вычисления выражения.
class ExecuteRequest(BaseModel):
    inputs: Dict[str, float]




# Создаём экземпляр FastAPI.
# Через него объявляются все HTTP-эндпоинты сервера.
app = FastAPI(title="Parameterized Function Server")#запуск fastApi



# Создание новой параметризованной функции.
# Принимает описание функции в формате JSON и сохраняет её в хранилище.
@app.post("/functions")
async def create_function(func: Function):#создаем функцию
    if func.name in functions:
        raise HTTPException(400, "Function already exists")
    functions[func.name] = func
    return {"status": "created"}


# Получение описания функции по её имени.
@app.get("/functions/{name}")
async def get_function(name: str):#получем параметры функции
    if name not in functions:
        raise HTTPException(404, "Function not found")
    return functions[name]


# Получение списка имён всех сохранённых функций.
@app.get("/functions")
async def list_functions():#список функций
    return list(functions.keys())


# Обновление параметров и/или выражения функции.
@app.put("/functions/{name}")
async def update_function(name: str, update: UpdateRequest):#обновляем функцию
    if name not in functions:
        raise HTTPException(404, "Function not found")
    func = functions[name]
    if update.parameters:
        func.parameters.update(update.parameters)
    if update.expression:
        func.expression = update.expression
    return {"status": "updated"}


# Удаление функции из хранилища.
@app.delete("/functions/{name}")
async def delete_function(name: str):#удаляем
    if name not in functions:
        raise HTTPException(404, "Function not found")
    del functions[name]
    return {"status": "deleted"}



# Вычисление значения функции.
# Выполняет вычисление выражения функции на основе её параметров и переданных входных данных.
@app.post("/functions/{name}/execute")
async def execute_function(name: str, req: ExecuteRequest):
    if name not in functions:
        raise HTTPException(404, "Function not found")
    func = functions[name]

    
    # Формируем контекст вычисления: объединяем параметры функции и входные значения
    context = {}
    context.update(func.parameters)
    context.update(req.inputs)

    try:
        # eval вычисляет строку выражения как Python‑код.
        # {"__builtins__": {}} отключает встроенные функции Python ради безопасности.
        # context — словарь переменных, доступных внутри выражения.
        result = eval(
            func.expression,
            {"__builtins__": {}},
            context
        )
    except Exception as e:
        raise HTTPException(400, str(e))
    # Возвращаем результат под первым именем из списка outputs,
    # например {"y": 42.0}, если outputs[0] == "y".
    return {func.outputs[0]: result}
