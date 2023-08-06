# -*- coding:utf-8 -*-
# @Time     :2023/2/8 9:44
# @Author   :CHNJX
# @File     :testcase.py
# @Desc     :
import pytest


class Testcase1:

    def test_01(self):
        assert 1 == 1


class Testcase2:
    pytestmark = [pytest.mark.demo]

    def test_01(self):
        assert 1 != 1
