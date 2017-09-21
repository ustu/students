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
import operator
import collections
import http.client
import urllib.parse
from typing import Any, Dict, List  # flake8: noqa
from pathlib import Path
from functools import reduce

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
            group:  str,
            values: Dict[str, Any]
    ) -> None:
        self.name:    str = name
        self.group:   str = group
        self.year:    int = values.get('year')
        self.session: int = values.get('session')
        self.exam:    str = 'exam' if values.get('exam') else 'noexam'
        self.__course_path: Path = Path('..') / Path(name)
        self.template_name: \
            str = f'{self.year}.{self.session}.{self.exam}.student.json'

    def _data(self, path: Path) -> Dict[str, Any]:
        if (path.exists()):
            return json.load(path.open())
        return {}

    @property
    def data(self) -> Dict[str, Any]:
        return self._data(self.template_path)

    @property
    def data_group(self) -> Dict[str, Any]:
        return self._data(self.template_group_path)

    @property
    def checkpoints(self) -> List[Dict[str, Any]]:
        return self._checkpoints(self.template_path)

    @property
    def checkpoints_group(self) -> List[Dict[str, Any]]:
        return self._checkpoints(self.template_group_path)

    def _checkpoints(self, path: Path) -> List[Dict[str, Any]]:
        data: Dict[str, Any] = self._data(path)
        return data.get('checkpoints', {}).items()

    def _template_path(self, common_path: Path) -> Path:
        path: Path = common_path / '_templates' / self.template_name
        if not path.exists():
            logging.warning(f'Template "{path}" doesn\'t exist')
            return Path('__NO_EXIST__')
        return path

    @property
    def template_path(self) -> Path:
        return self._template_path(self.course_path)

    @property
    def template_group_path(self) -> Path:
        # Make group templates for subjects
        path: Path = Path(PATH_TO_GROUP) / self.group / '_common' / self.name
        path.mkdir(exist_ok=True)

        # Copy if not exist
        try:
            shutil.copytree(f'../{self.name}/_templates', path)
        except FileExistsError as e:
            pass

        # Return template path
        return self._template_path(path)

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
            group:    str,
            github:   str,
            path:     Path,
            subjects: Dict[str, Any]
    ) -> None:
        self.name:     str = name
        self.group:    str = group
        self.github:   str = github
        self.path:     Path = path
        self.subjects: Dict[str, Any] = subjects

    def set_github(self, course: Course) -> None:

        if self.github:
            return None

        dst: Dict[str, Any] = json.load(self._dst_path(course).open())
        github_nickname: str = dst.get('github_nickname', None)
        if not github_nickname:
            return None

        self.github = github_nickname

        path: Path = Path(PATH_TO_GROUP) / f'{self.group}.json'
        data: Dict[str, Any] = json.load(path.open())
        for item in data.get('students'):
            if item.get('name') == self.name:
                item['github'] = github_nickname

        json.dump(data, path.open('w'), ensure_ascii=False, indent=2)

    def checkpoints(self, course: Course) -> List[Dict[str, Any]]:
        data: Dict[str, Any] = json.load(self._dst_path(course).open())
        return [
            {
                **items.get('total', {}),
                **{
                    'score': items.get('score', 0)
                    if items.get('score', 0) > 0
                    else ''
                }
            }
            for _, items in data.get('checkpoints', {}).items()
        ]

    def _dst_path(self, course: Course) -> Path:
        return self.path / f'{course.year}.{course.session}.{course.name}.json'

    def make(self) -> None:
        key: str
        values: Dict[str, Any]

        # Walk courses
        for key, values in self.subjects.items():
            course: Course = Course(key, self.group, values)
            course_template: Path = course.template_group_path
            if not course_template.exists():
                continue

            # Check file exist and update is it
            dst_path: Path = self._dst_path(course)
            if not dst_path.exists():
                get_from_github(self.github)
                shutil.copy(course.template_group_path, dst_path)
            else:
                self.set_github(course)
                merge_json_files(
                    course.template_group_path,
                    dst_path,
                    {
                        **(
                            {
                                'github_nickname': self.github,
                            } if self.github else {}
                        ),
                        **{'checkpoints/Контрольная работа': None}
                    }
                    # [
                    #     'checkpoints',
                    # ]
                )


def merge_json_files(
        src_path: Path,
        dst_path: Path,
        overwrite: Dict[str, Any] = {},
        merge_subkeys: List[str] = []
) -> None:
    '''
    Merge 2 JSON file
    '''
    src: Dict[str, Any] = json.load(src_path.open())
    dst: Dict[str, Any] = json.load(dst_path.open())

    def setValue(keys: List[str], data: Dict, value) -> None:
        getValue(keys[:-1], data)[keys[-1]] = value

    def getValue(keys: List[str], data: Dict):
        return reduce(operator.getitem, keys, data)

    # merge subkeys
    for key in merge_subkeys:
        dst[key] = {**src[key], **dst[key]}

    # Owerwrite
    for _keys, value in overwrite.items():
        keys = _keys.split('/')
        _value = value if value else getValue(keys, src)
        print(_value)
        setValue(keys, dst, _value)

    src.update(dst)
    json.dump(dst, dst_path.open('w'), ensure_ascii=False, indent=2)


def get_from_github(login: str) -> str:
    '''
    Return avatar if user exist
    '''
    if not login.strip():
        return ''
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
            try:
                _obj: Student = Student(
                    name,
                    group,
                    github,
                    stud_path,
                    subjects
                )
            except Exception as e:
                logging.error(str(e))
                continue
            print(_obj.name)
            _obj.make()
            students_obj.append(_obj)

        # Rebuild score reports
        for key, values in subjects.items():
            course: Course = Course(key, group, values)
            score_path: Path = course.score_path(group)
            if not score_path.parent.exists():
                continue
            with open('./score.mako') as fo:
                score: str = Template(fo.read()).render(
                    course=course,
                    group_name=group,
                    students=students_obj,
                    collections=collections,
                    quote=lambda url: urllib.parse.quote(
                        url.replace(' ', '%20'),
                        safe="%/:=&?~#+!$,;'@()*[]"
                    )
                    # quote=lambda url: urllib.parse.quote_plus(
                    #     url, safe=":,/"
                    # )
                )
            score_path.write_text(score)


# Walk groups
for pos_json in os.listdir(PATH_TO_GROUP):
    if pos_json.endswith('.json'):
        make_group(PATH_TO_GROUP + pos_json)
