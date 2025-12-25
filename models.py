# BaseModel — базовый класс Pydantic для описания
# схем данных (валидация, сериализация в JSON).
from pydantic import BaseModel
# Dict, List, Optional — типы из typing:
# Dict[Ключ, Значение], List[Тип], Optional[Тип или None].
from typing import Dict, List, Optional


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