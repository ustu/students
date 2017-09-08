#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Parse students
"""
# standard library
import os
import json
import shutil
import logging
import http.client
from typing import Any, Dict, List  # flake8: noqa
from pathlib import Path

# third-party
from mako.template import Template

PATH_TO_GROUP: str = '../Группы/'


class Course(object):
    '''
    Course
    '''
    def __init__(
            self,
            name:   str,
            values: Dict[str, Any]
    ) -> None:
        self.name = name
        self.year:    int = values.get('year')
        self.session: int = values.get('session')
        self.exam:    str = 'exam' if values.get('exam') else 'noexam'
        self.__course_path: Path = Path('..') / Path(name)
        self.template_name: \
            str = f'{self.year}.{self.session}.{self.exam}.student.json'

    @property
    def data(self) -> Dict[str, Any]:
        if (self.template_path.exists()):
            return json.load(self.template_path.open())
        return {}

    @property
    def checkpoints(self) -> List[str]:
        return [
            f'`{values.get("name", "")}'
            f' <{values.get("url", "./")}>`_'
            f' {values.get("date")}'
            for key, values in self.data.get('checkpoints', {}).items()
        ]

    @property
    def template_path(self) -> Path:
        path: Path = self.course_path / '_templates' / self.template_name
        if not path.exists():
            logging.warning(f'Template "{path}" doesn\'t exist')
            return Path('__NO_EXIST__')
        return path

    @property
    def course_path(self) -> Path:
        if not self.__course_path.exists():
            logging.warning(f'Course "{self.name}" doesn\'t exist')
            return Path('__NO_EXIST__')
        return self.__course_path

    def score_path(self, group) -> Path:
        return self.course_path / f'{self.year}.{self.session}.{group}.rst'


class Student(object):
    '''
    Student factory
    '''

    def __init__(
            self,
            name:     str,
            github:   str,
            path:     Path,
            subjects: Dict[str, Any]
    ) -> None:
        self.name:     str = name
        self.github:   str = github
        self.avatar:   str = get_from_github(github)
        self.path:     Path = path
        self.subjects: Dict[str, Any] = subjects

    def checkpoints(self, course: Course) -> List[Dict[str, str]]:
        return [
            items.get('total', {})
            for _, items in course.data.get('checkpoints', {}).items()
        ]

    def make(self) -> None:
        key: str
        values: Dict[str, Any]

        # Walk courses
        for key, values in self.subjects.items():
            course: Course = Course(key, values)
            course_template: Path = course.template_path
            if not course_template.exists():
                continue

            # Check file exist and update is it
            dst_path: Path = self.path / \
                f'{course.year}.{course.session}.{course.name}.json'
            if not dst_path.exists():
                shutil.copy(course_template, dst_path)
            else:
                merge_json_files(course_template, dst_path)


def merge_json_files(src_path: Path, dst_path: Path) -> None:
    '''
    Merge 2 JSON file
    '''
    src: Dict[str, Any] = json.load(src_path.open())
    dst: Dict[str, Any] = json.load(dst_path.open())
    src.update(dst)
    json.dump(dst, dst_path.open('w'), ensure_ascii=False, indent=2)


def get_from_github(login: str) -> str:
    '''
    Return avatar if user exist
    '''
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", f"/users/{login}", headers={'User-Agent': 'USTU/IIT'})
    response = conn.getresponse()
    if response.status == 403:
        conn = http.client.HTTPSConnection("github.com")
        conn.request(
            "GET", f"/{login}", headers={'User-Agent': 'USTU/IIT'}
        )
        response = conn.getresponse()
        if response.status == 200:
            return ''
        else:
            logging.error(response.status, response.read())  # type: ignore
            raise Exception(f'User {login} not found')
    elif response.status != 200:
        logging.error(response.status, response.read())  # type: ignore
        raise Exception(f'User {login} not found')
    info: Dict[str, Any] = json.load(response)  # type: ignore
    if info['type'] != 'User':
        raise Exception(f'Wrong user type {info["type"]}')
    return info['avatar_url']


def make_group(file_name: str) -> None:
    '''
    Create group folder and add students
    '''
    with open(file_name) as file:
        data:     Dict[str, Any] = json.load(file)
        group:    str = data.get("name", "")
        students: List[Dict] = data.get("students", "")
        subjects: Dict[str, Any] = data.get("subjects", {})

        # Make group dir
        if not all((group, students)):
            raise Exception(f'No group or students in {file_name}')
        path: Path = Path(PATH_TO_GROUP + group)
        path.mkdir(exist_ok=True)

        # Walk students
        students_obj: List[Student] = []
        student: Dict[str, Any]
        for student in students:
            name: str = student.get('name', '')
            if len(name.split()) < 2:
                raise Exception(f'Bad fullname {name}')
            stud_path = path / name
            stud_path.mkdir(exist_ok=True)

            github: str = student.get('github', '')
            _obj: Student = Student(name, github, stud_path, subjects)
            print(_obj.name)
            _obj.make()
            students_obj.append(_obj)

        # Rebuild score reports
        for key, values in subjects.items():
            course: Course = Course(key, values)
            score_path: Path = course.score_path(group)
            if not score_path.parent.exists():
                continue
            with open('./score.mako') as fo:
                score: str = Template(fo.read()).render(
                    course=course,
                    group_name=group,
                    students=students_obj
                )
            score_path.write_text(score)


# Walk groups
for pos_json in os.listdir(PATH_TO_GROUP):
    if pos_json.endswith('.json'):
        make_group(PATH_TO_GROUP + pos_json)
