import random
import pytest
import data.manuscripts.query as mqry


def gen_random_not_valid_str() -> str:
    BIG_NUM = 500_00_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)


def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_not_valid_state():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_state(gen_random_not_valid_str())


