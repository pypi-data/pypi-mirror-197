#!/usr/bin/env python3

from nextcloudtasks import *
import cmd
import getpass
import configparser
import os
import re
import datetime

"""
Example of CLI program to manage tasks

Example of .nc-tasks.rc file:
[DEFAULT]
url=your.nextclouddomain.foo:443/remote.php/dav/calendars/youruser/
user=youruser
password=yourpassword
list=yourlist

"""
class TasksShell(cmd.Cmd):
    intro = 'Welcome to Nextcloud tasks CLI. Type help or ? to list commands.\n'
    prompt = '(Nextcloud Tasks) '
    url = None
    list = None
    nextcloud = None

    # Commands
    def do_load(self, arg):
        'load configuration file; ".nc-tasks.rc" by default; If not, use <file>'
        config = configparser.ConfigParser()
        if len(arg) > 0:
            filename = arg.split()
        else:
            filename = os.path.expanduser("~") + '/.nc-tasks.rc'
        config.read(filename)
        self.nextcloud = NextcloudTask(config['DEFAULT']['url'], config['DEFAULT']['list'])
        self.nextcloud.connect(config['DEFAULT']['user'], config['DEFAULT']['password'])
        self.print = config['DEFAULT']['print']

    def do_nextcloud(self, arg):
        'Create the NextcloudTask object with <url> <list>'
        self.nextcloud = NextcloudTask(arg.split()[0], arg.split()[1])

    def do_connect(self, arg):
        'Connect <user>'
        user = arg.split()[0]
        passwd = getpass.getpass()
        self.nextcloud.connect(user, passwd)

    def changeOrder(self, arg):
        'Change order of print tasks'
        self.nextcloud.setSort((arg.split()[0],))

    def do_print(self, arg):
        'Print tasks by priority order; in nextcloud "None" is No priority, so it is the first.'
        if len(arg) == 0:
            if (self.print is not None):
                self.nextcloud.printTODOs(self.print)
            else:
                self.nextcloud.printTODOs("summary")
        else:
            self.nextcloud.printTODOs(arg.split()[0])

    def do_print_all(self, arg):
        'Print all tasks (complete included) by priority order; in nextcloud "None" is No priority, so it is the first.'
        if len(arg) == 0:
            if (self.print is not None):
                self.nextcloud.printTODOs(self.print, include_completed=True)
            else:
                self.nextcloud.printTODOs("summary", include_completed=True)
        else:
            self.nextcloud.printTODOs(arg.split()[0], include_completed=True)

    def do_add(self, arg):
        'Add task; add <summary>'
        priority = int(input("Enter priority [default=0]: ") or "0")
        percent_complete = int(input("Enter percent-complete [default=0]: ") or "0")
        self.nextcloud.addTodo(arg, priority, percent_complete)

    def do_list(self, arg):
        'Change list'
        self.nextcloud.setList(arg)

    def do_delete(self, arg):
        'Delete task by uid/summmary'
        if len(arg.split()) >= 1:
            try:
                if (re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$",arg)):
                    # Delete by uid (uuid in Nextcloud)
                    self.nextcloud.deleteByUid(arg)
                else:
                    # Delety by summary
                    self.nextcloud.deleteBySummary(arg)
            except TaskNotFound:
                print("Task %s not found" % arg)
        else:
            print("Need the <uid/summary>")
        
    def do_edit(self, arg):
        'Edit task'
        if len(arg.split()) == 1:
            try:
                if (re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$",arg)):
                    # Update by uid (uuid in Nextcloud)
                    todo = self.nextcloud.getTodoByUid(arg)
                    summary = input("Enter summary [default=%s]: "%todo.icalendar_component['SUMMARY'])
                    priority = int(input("Enter priority [default=%s]: "%todo.icalendar_component['PRIORITY']) or int(todo.icalendar_component['PRIORITY']))
                    percent_complete = int(input("Enter percent-complete [default=%s]: "%todo.icalendar_component['PERCENT-COMPLETE']) or int(todo.icalendar_component['PERCENT-COMPLETE'])) 
                    try:
                        dtstart = input("Enter dtstart (YmdTHS) [default=%s]: "%str(todo.icalendar_component['DTSTART']))
                    except KeyError:
                        dtstart = input("Enter dtstart (YmdTHS) [default=None]: ")
                    try:
                        due = input("Enter due YmdTHMS [default=%s]: "%str(todo.icalendar_component['DUE']))
                    except KeyError:
                        due = input("Enter due YmdTHMS [default=None]: ")
                    if summary == '':
                        summary = None
                    if dtstart == '':
                        dtstart = None
                    else:
                        dtstart = datetime.strptime(dtstart, "%Y%m%dT%H%M%S")
                    if due == '':
                        due = None
                    else:
                        due = datetime.strptime(due, "%Y%m%dT%H%M%S")
                    self.nextcloud.updateTodo(arg, summary=summary, start=dtstart, due=due, priority=priority, percent_complete=percent_complete)
                else:
                    print("Error: UID bad format")  
            except TaskNotFound:
                print("Task %s not found" % arg)
        else:
            print("Need the <uid>")        

    def do_complete(self, arg):
        'Set a task as completed'
        if len(arg.split()) >= 1:
            try:
                if (re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$",arg)):
                    self.nextcloud.updateTodo(arg, percent_complete=100)
                else:
                    uid = self.nextcloud.getUidbySummary(arg)
                    self.nextcloud.updateTodo(uid, percent_complete=100)
            except TaskNotFound:
                print("Task %s not found" % arg)
        else:
            print("Need the <uid/summary>")

    def do_close(self, arg):
        ' Close nextcloud connection'
        self.nextcloud.close()
        return True
    
    def do_exit(self, arg):
        'Close Nextcloud tasks CLI'
        return True

if __name__ == '__main__':
    TasksShell().cmdloop()
