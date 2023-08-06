from dataclasses import dataclass, field
from logging import getLogger
from devgoldyutils import DictDataclass

@dataclass
class Test(DictDataclass):
    data:dict
    bruh:str = field(init=False)

    logger = getLogger("bruhhhh")

    def __post_init__(self):
        self.bruh = self.get("ow")

test = Test({
    "owo": {
        "bruh": "omg"
    }
})

print(test.bruh)