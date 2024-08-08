from typing import List,Tuple
from random import randint, uniform

from shapely import Polygon

from db.models import models

def gen_mock_cnpj(to_test_unique:List[str]) -> str:

    while True:
        cnpj = [randint(0,9) for _ in range(12)]
        first_sum = sum(
            (val*weight for (val,weight) in zip(
                cnpj[:12],[5,4,3,2,9,8,7,6,5,4,3,2]
            ) )
        )
        first_digit = 11 - (first_sum % 11)
        first_digit = first_digit if first_digit < 10 else 0
        second_sum = sum((val * weight for val, weight in zip(
            cnpj[:13], [6,5,4,3,2,9,8,7,6,5,4,3,2])))
        second_digit = 11 - (second_sum % 11)
        second_digit = second_digit if second_digit < 10 else 0
        cnpj.append(second_digit)       
        cnpj = ''.join([str(n) for n in cnpj])
        if cnpj not in to_test_unique: return cnpj

def gen_square_area(side_length:float) -> Tuple[Tuple]:

    top_left = (uniform(-180.0,180.0), uniform(-90.0,90.0))
    top_right = (top_left[0], top_left[1] + side_length)
    bottom_right = (top_left[0] - side_length, top_left[1] + side_length)
    bottom_left = (top_left[0] - side_length, top_left[1])
    return (top_left,top_right,bottom_right,bottom_left)

