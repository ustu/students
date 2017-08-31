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

PATH_TO_GROUP: str = '../Группы/'


class Student(object):

    def __init__(
            self,
            name:     str,
            github:   str,
            path:     Path,
            subjects: Dict[str, Any]
    ) -> None:
        self.name:     str = name
        self.github:   str = github
        self.avatar:   str = getFromGitHub(github)
        self.path:     Path = path
        self.subjects: Dict[str, Any] = subjects

    def make(self) -> None:
        key: str
        values: Dict[str, Any]
        for key, values in self.subjects.items():
            course_path: Path = Path('..') / Path(key)
            if not os.path.exists(course_path):
                logging.warning(f'Course "{key}" doesn\'t exist')
                continue
            year: int = values.get('year')
            session: int = values.get('session')
            exam: str = 'exam' if values.get('exam') else 'noexam'
            template_name: str = f'{year}.{session}.{exam}.student.json'
            template_path: Path = course_path / '_templates' / template_name
            if not os.path.exists(template_path):
                logging.warning(f'Template "{template_path}" doesn\'t exist')
                continue
            dst_name: str = f'{year}.{session}.{key}.json'
            shutil.copy(template_path, self.path / dst_name)


def getFromGitHub(login: str) -> str:
    '''
    Return avatar if user exist
    '''
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", f"/users/{login}", headers={'User-Agent': 'USTU/IIT'})
    response = conn.getresponse()
    if response.status != 200:
        logging.error(response)  # type: ignore
        raise Exception(f'User {login} not found')
    info: Dict[str, Any] = json.load(response)  # type: ignore
    if info['type'] != 'User':
        raise Exception(f'Wrong user type {info["type"]}')
    return info['avatar_url']


def makeStudent(student: Student) -> None:
    print(student.name)
    student.make()


def makeGroup(file_name: str) -> None:
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
        student: Dict[str, Any]
        for student in students:
            name: str = student.get('name', '')
            if len(name.split()) < 2:
                raise Exception(f'Bad fullname {name}')
            stud_path = path / name
            stud_path.mkdir(exist_ok=True)

            github: str = student.get('github', '')
            makeStudent(Student(name, github, stud_path, subjects))


for pos_json in os.listdir(PATH_TO_GROUP):
    if pos_json.endswith('.json'):
        makeGroup(PATH_TO_GROUP + pos_json)
