# swml_statements.py

from typing import List, Optional, Dict, Any, Union
from base_swml import BaseSWML


class Transfer(BaseSWML):
    def __init__(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 meta: Optional[Dict[str, Any]] = None):
        self.dest = dest
        self.params = params
        self.meta = meta


class Execute(BaseSWML):
    def __init__(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 on_return: Optional[Dict[str, Any]] = None):
        self.dest = dest
        self.params = params
        self.on_return = on_return


class Return(BaseSWML):
    def __init__(self,
                 return_value: Optional[Any] = None):
        self.return_value = return_value


class Request(BaseSWML):
    def __init__(self, url: str,
                 method: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: Optional[Union[str, Dict[str, Any]]] = None,
                 timeout: Optional[float] = 5.0,
                 connect_timeout: Optional[float] = 5.0,
                 save_variables: Optional[bool] = False):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.save_variables = save_variables


class Switch(BaseSWML):
    def __init__(self,
                 variable: str,
                 case: Optional[Dict[str, List[Any]]] = None,
                 default: Optional[List[Any]] = None):
        self.variable = variable
        self.case = case
        self.default = default


class Cond(BaseSWML):
    def __init__(self,
                 when: str,
                 then: List[Any],
                 else_: List[Any]):
        self.when = when
        self.then = then
        self.else_ = else_


class Set(BaseSWML):
    def __init__(self,
                 variables: Dict[str, Any]):
        self.variables = variables


class Unset(BaseSWML):
    def __init__(self,
                 vars: Union[str, List[str]]):
        self.vars = vars
