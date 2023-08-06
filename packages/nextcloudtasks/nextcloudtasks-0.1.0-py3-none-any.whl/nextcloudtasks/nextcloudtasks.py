#!/usr/bin/env python3

import caldav
from prettytable import PrettyTable
import datetime
import uuid
import re


todo_skeleton = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//TODOcli Nextcloud tasks 0.1
BEGIN:VTODO
CREATED;X-VOBJ-FLOATINGTIME-ALLOWED=TRUE:{}
DTSTAMP;X-VOBJ-FLOATINGTIME-ALLOWED=TRUE:{}
LAST-MODIFIED;X-VOBJ-FLOATINGTIME-ALLOWED=TRUE:{}
SUMMARY:{}
UID:{}
PRIORITY:{}
PERCENT-COMPLETE:{}
STATUS: {}
END:VTODO
END:VCALENDAR"""


# Errors
class SummaryNotFound(Exception):
    "message..."
    pass

class TaskNotFound(Exception):
    def __init__(self, task):
        super().__init__("Task \"%s\" not found." % task)

class ListNotFound(Exception):
    def __init__(self, list):
        super().__init__("List \"%s\" not found." % list)

# Class to handle the TODOs of Nextcloud tasks
# RFC5545 (iCalendar)
class Todo:
    """
    Class that parse VTODO calendar component and convert it to an object.
    Mention that this is from a Nextcloud Tasks usage, RFC5545 contains more
    "Component Properties", but Nextcloud Tasks does not use all of them.
    """
    def __init__(self, todo):
        self.todo = todo
        self.summary = re.search('SUMMARY:(.*?)\n', todo, re.DOTALL).group(1)
        self.created = datetime.datetime.strptime(re.search('CREATED(?:;X-VOBJ-FLOATINGTIME-ALLOWED=TRUE|):(.*?)\n', todo, re.DOTALL).group(1), '%Y%m%dT%H%M%S')
        self.dtstamp = datetime.datetime.strptime(re.search('DTSTAMP(?:;X-VOBJ-FLOATINGTIME-ALLOWED=TRUE|):(.*?)\n', todo, re.DOTALL).group(1), '%Y%m%dT%H%M%S')
        self.last_modified = datetime.datetime.strptime(re.search('LAST-MODIFIED(?:;X-VOBJ-FLOATINGTIME-ALLOWED=TRUE|):(.*?)\n', todo, re.DOTALL).group(1), '%Y%m%dT%H%M%S')
        self.uid = re.search('UID:(.*?)\n', todo, re.DOTALL).group(1)
        # the following components could not be in the nextcloud task
        try:
            self.categories = re.search('CATEGORIES:(.*?)\n', todo, re.DOTALL).group(1)
        except:
            self.categories = None
        try:
            self.due = datetime.datetime.strptime(re.search('DUE:(.*?)\n', todo, re.DOTALL).group(1), '%Y%m%dT%H%M%S')
        except:
            self.due = None
        try:
            self.priority = re.search('PRIORITY:(.*?)\n', todo, re.DOTALL).group(1)
        except:
            self.priority = None
        try:
            self.percent_complete = int(re.search('PERCENT-COMPLETE:(.*?)\n', todo, re.DOTALL).group(1))
        except:
            self.percent_complete = None
        try:
            self.status = re.search('STATUS:(.*?)\n', todo, re.DOTALL).group(1) # NEEDS-ACTION, COMPLETED, IN-PROCESS
        except:
            self.status = None
        try:
            self.completed = datetime.datetime.strptime(re.search('COMPLETED:(.*?)\n', todo, re.DOTALL).group(1), '%Y%m%dT%H%M%S')
        except:
            self.completed = None
        try:
            self.dtstart = datetime.datetime.strptime(re.search('DTSTART:(.*?)\n', todo, re.DOTALL).group(1), '%Y%m%dT%H%M%S')
        except:
            self.dtstart = None
        try:
            # Notes in Nexctcloud tasks
            self.description = re.search('DESCRIPTION:(.*?)\n', todo, re.DOTALL).group(1)
        except:
            self.description = None
        try:
            # Subtasks in Nexctcloud tasks
            self.related_to = re.search('RELATED-TO:(.*?)\n', todo, re.DOTALL).group(1)
        except:
            self.related_to = None

    def getSummary(self):
        return self.summary

    def getCreated(self):
        return self.created# Component properties

    def getModified(self):
        return self.last_modified

    def getTodo(self):
        return self.todo

    def getUid(self):
        return self.uid

    def getSummary(self):
        return self.summary

    def getStatus(self):
        return self.status

    def getDtstart(self):
        return self.dtstart

    def getCompleted(self):
        return self.completed

    def getDescription(self):
        return self.description# Component properties

    def getNotes(self):
        """
        In Nextcloud use the Component property Description for notes
        """
        return self.description

    def raw(self):
        """
        Convert a Todo in an iCalendar
        """
        return self.todo

    def VTodo(self):
        """
        Return a VTodo object of caldav module
        """
        raw = todo_skeleton.format(datetime.datetime.now().strftime('%Y%m%dT%H%M%S'),
            datetime.datetime.now().strftime('%Y%m%dT%H%M%S'), datetime.datetime.now().strftime('%Y%m%dT%H%M%S'),
            self.summary, self.uid, str(self.priority), str(self.percent_complete), self.status)
        return caldav.objects.Todo(data=raw)

    def __str__(self):
        return "Todo(uid={}, summary={})".format(self.uid, self.summary)

class NextcloudTask:
    """
    Class responsible to handle the Nextcloud caldav connection, adding, deleting,
    modifying and printing the TODO lists.
    """
    def __init__(self, url, list):
        """
        Parameters:
        url: Nextcloud url
        list: Task list
        """
        self.url = url
        self.list = list
        self.connected = False
        self.sort = ("priority",)

    def connect(self, username, password):
        """
        Connect to nextcloud CALDAV using caldav python module
        """
        self.client = caldav.DAVClient("https://"+username+":"+password+"@"+self.url)
        try:
            self.calendar = self.client.principal().calendar(self.list)
        except caldav.error.NotFoundError:
            raise ListNotFound(self.list)
        self.todos = self.client.principal().calendar(self.list).todos()
        self.connected = True

    def isConnected(self):
        return self.connected

    def close(self):
        """
        Close the Nextcloud caldav connection
        """
        self.client.close()

    def setList(self, list):
        """
        Set a task list
        """
        self.list = list
        try:
            self.calendar = self.client.principal().calendar(self.list)
        except caldav.error.NotFoundError:
            raise ListNotFound(self.list)

    def updateTodos(self):
        """
        Update the task lists
        """
        self.todos = self.client.principal().calendar(self.list).todos()

    def setSort(self, keys=("priority",)):
        """
        Set the sort key(s)
        """
        self.sort = keys

    def addTodo(self, summary, priority=0, percent_complete=0):
        """ Add task only with summary """
        if percent_complete == 100:
            status = "COMPLETED"
        elif percent_complete == 0:
            status = "NEEDS-ACTION"
        else:
            status = "IN-PROCESS"
        todo = todo_skeleton.format(datetime.datetime.now().strftime('%Y%m%dT%H%M%S'),
            datetime.datetime.now().strftime('%Y%m%dT%H%M%S'), datetime.datetime.now().strftime('%Y%m%dT%H%M%S'),
            summary, str(uuid.uuid4()), str(priority), str(percent_complete), status)
        self.calendar.save_todo(todo)
        self.updateTodos()

    def updateTodo(self, uid, summary=None, start=None, due=None, note=None,
        priority=None, percent_complete=None, categories=None):
        """
        Update summary of a task

        Keyword arguments:
        uid -- string with the UID of the task
        summary -- string
        start -- datetime
        due -- datetime
        note -- string
        priority -- int
        percent_complete -- int
        categories -- dict of string
        """
        todo = self.getTodoByUid(uid)
        if summary is not None:
            todo.icalendar_component['SUMMARY'] = summary
        if note is not None:
            todo.icalendar_component['DECRIPTION'] = note
        if categories is not None:
            todo.icalendar_component['CATEGORIES'] = categories
        if start is not None:
            todo.icalendar_component['DTSTART'] = start.strftime('%Y%m%dT%H%M%S')
        if due is not None:
            todo.icalendar_component['DUE'] = due.strftime('%Y%m%dT%H%M%S')
        if priority is not None:
            todo.icalendar_component['PRIORITY'] = priority
        if percent_complete is not None:
            todo.icalendar_component['PERCENT-COMPLETE'] = percent_complete
            if percent_complete == 0:
                todo.icalendar_component['STATUS'] = "NEEDS-ACTION"
            elif percent_complete == 100:
                todo.icalendar_component['STATUS'] = "COMPLETED"
                todo.icalendar_component['COMPLETED'] = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
            else:
                todo.icalendar_component['STATUS'] = "IN-PROCESS"
        # Although Nextcloud will not update the last-modified, we want to update
        todo.icalendar_component['LAST-MODIFIED'] = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        todo.save()
        self.updateTodos()

    def getTodoByUid(self, uid):
        """
        Get task by UID
        """
        todo = self.client.principal().calendar(self.list).todo_by_uid(uid)
        return todo

    def getTodoBySummary(self, summary):
        """
        Get task by summary
        """
        uid = self.getUidbySummary(summary)
        todo = self.getTodoByUid(uid)
        return todo

    def getUidbySummary(self, summary):
        """ Get summary by uid """
        output = ""
        for todo in self.todos:
            if (todo.icalendar_component["SUMMARY"] == summary):
                output = todo.icalendar_component["UID"]
                break
        if output == "":
            raise SummaryNotFound
        else:
            return output

    def getSummarybyUid(self, uid):
        """ Get uid by summary """
        return self.calendar.todo_by_uid(uid).icalendar_component["SUMMARY"]

    def deleteByUid(self, uid):
        """ Delete a task by uid """
        try:
            self.calendar.todo_by_uid(uid).delete()
        except caldav.error.NotFoundError:
            raise TaskNotFound(uid)

    def deleteBySummary(self, summary):
        """ Delete a task by summary """
        uid = self.getUidbySummary(summary)
        self.deleteByUid(uid)

    def printTODO(self, uid):
        """ Print task by uid """
        todo = self.client.principal().calendar(self.list).todo_by_uid(uid)
        print(Todo(todo.data))

    def printTODOs(self, columns, include_completed=False):
        """
        Print tasks by selected columns
        Parameters:
        columns: Comma separated list of Component Properties of VTODO (without spaces)
        """
        table = PrettyTable()
        table.field_names = [column.upper().strip() for column in columns.split(",")]
        todos = self.client.principal().calendar(self.list).todos(sort_keys=self.sort, include_completed=include_completed)
        for t in todos:
            todo = Todo(t.data)
            row = []
            for i in table.field_names:
                if ("CREATED" == i.strip()):
                    row.append(todo.created)
                elif ("UID" == i.strip()):
                    row.append(todo.uid)
                elif ("SUMMARY" == i.strip()):
                    row.append(todo.summary)
                elif ("CATEGORIES" == i.strip()):
                    row.append(todo.categories)
                elif ("PRIORITY" == i.strip()):
                    row.append(todo.priority)
                elif ("PERCENT-COMPLETE" == i):
                    row.append(todo.percent_complete)
                elif ("STATUS" == i.strip()):
                    row.append(todo.status)
                elif ("RELATED-TO" == i.strip()):
                    # related-to is a UID, so use the summary of the main task
                    try:
                        row.append(self.getSummarybyUid(todo.related_to))
                    except caldav.error.NotFoundError:
                        row.append(todo.related_to)
                        pass
                else:
                    row.append(i.strip())
            table.add_row(row)
        print(table)
