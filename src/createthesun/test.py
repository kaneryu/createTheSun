import dataclasses
import random
import string


@dataclasses.dataclass
class fizlike:
    outstring: str
    num: int


def game(num: int, fizlikes: list[fizlike]) -> None:
    def checker(num: int, fizlike_: fizlike) -> str:
        if num % fizlike_.num == 0:
            return fizlike_.outstring + " "
        return ""

    for i in range(1, num + 1):
        fizlike_out = ""
        for fizlike_ in fizlikes:
            fizlike_out += checker(i, fizlike_)
        print(fizlike_out or i)


def randomString(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def randomInt(length: int) -> int:
    return random.randint(2, 9)


fizzes = []
for i in range(5):
    fizzes.append(fizlike(randomString(randomInt(5)), randomInt(1)))

game(100, fizzes)
