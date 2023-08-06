import os
from os.path import join, dirname

from service_driver.project_generator import ProjectGenerator
from service_driver.swagger_generate import SwaggerGenerator


class TestProjectGenerator:
    def test_start_project(self):
        ProjectGenerator().project_generate('new_project')
        assert os.path.isdir(os.path.join('new_project', "api_object"))
        assert os.path.isdir(os.path.join('new_project', "testcase"))

    def test_swagger_generate(self):
        SwaggerGenerator().generate(join(join(dirname(__file__), '..'), 'test/swagger/swagger.yaml'),
                                    join(join(dirname(__file__), '..'), 'test/api_object'))
        assert os.path.exists(os.path.join(os.path.dirname(__file__) + "/api_object", "users.py"))
