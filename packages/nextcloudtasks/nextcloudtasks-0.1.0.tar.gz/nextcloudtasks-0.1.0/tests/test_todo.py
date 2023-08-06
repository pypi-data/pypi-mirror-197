#!/usr/bin/env python

import unittest
import datetime
from nextcloudtasks import *

class TestTodo(unittest.TestCase):
    def test_parse_summary(self):
        f = open('tests/assets/vcalendar-vtodo1.ics', 'r')
        test = f.read()
        todo = Todo(test)
        self.assertEqual('Calendar 1 - Task 1', todo.summary)
        f.close()

    def test_parse_created(self):
        f = open('tests/assets/vcalendar-vtodo2.ics', 'r')
        test = f.read()
        todo = Todo(test)
        self.assertEqual(datetime.datetime.strptime('20181119T183919', '%Y%m%dT%H%M%S'), todo.created)
        f.close()

    def test_parse_dtstamp(self):
        f = open('tests/assets/vcalendar-vtodo3_1_1.ics', 'r')
        test = f.read()
        todo = Todo(test)
        self.assertEqual(datetime.datetime.strptime('20190918T095816', '%Y%m%dT%H%M%S'), todo.dtstamp)
        f.close()

    def test_parse_last_modified(self):
        f = open('tests/assets/vcalendar-vtodo3_1.ics', 'r')
        test = f.read()
        todo = Todo(test)
        self.assertEqual(datetime.datetime.strptime('20190918T095816', '%Y%m%dT%H%M%S'), todo.last_modified)
        f.close()

    def test_uid(self):
        f = open('tests/assets/vcalendar-vtodo3.ics', 'r')
        test = f.read()
        todo = Todo(test)
        self.assertEqual('pwen4kz20g', todo.uid)
        f.close()

    def test_str(self):
        f = open('tests/assets/vcalendar-vtodo7.ics', 'r')
        test = f.read()
        todo = Todo(test)
        self.assertEqual('Todo(uid=pwen9kz48g, summary=Calendar 1 - Task 7)', str(todo))
        f.close()

    def test_return_todo1(self):
        f = open('tests/assets/vcalendar-vtodo1.ics', 'r')
        test = f.read()
        f.close()
        todo = Todo(test)
        raw = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Nextcloud Tasks 0.11.3\nBEGIN:VTODO\nCREATED:20181119T183919\nDTSTAMP:20190918T095816\nLAST-MODIFIED:20190918T095816\nUID:pwen4kz18g\nSUMMARY:Calendar 1 - Task 1\nPRIORITY:1\nDUE:20190101T123400\nEND:VTODO\nEND:VCALENDAR\n"
        t_todo = todo.todo
        self.assertEqual(t_todo, raw)

if __name__ == '__main__':
    unittest.main()
