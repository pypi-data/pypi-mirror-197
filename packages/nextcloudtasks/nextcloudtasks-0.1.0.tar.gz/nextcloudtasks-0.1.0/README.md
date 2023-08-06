# Nextcloud Tasks API

[![Python package](https://github.com/Sinkmanu/nextcloud-tasks/actions/workflows/test-todo.yml/badge.svg?branch=main)](https://github.com/Sinkmanu/nextcloud-tasks/actions/workflows/test-todo.yml)

A [Nextcloud Tasks](https://github.com/nextcloud/tasks) API wrapper with some useful examples for CLI

```py
from nextcloudtasks import *

nextcloud = NextcloudTask("foo.bar.org:443/remote.php/dav/calendars/foobar/", "myList")
nextcloud.connect("username", "password")
nextcloud.printTODOs("summary,categories,created,priority")
nextcloud.close()
```

It is a custom API wrapper that is not developed nor maitained by Nextcloud. 

## Installation

```sh
pip install nextcloudtasks
```

## Examples

The following example is a tool that manages the a Nextcloud TODO list from the command line. It can be found in [examples](/examples)

.nc-tasks.rc
```
[DEFAULT]
url=your.nextclouddomain.foo:443/remote.php/dav/calendars/youruser/
user=youruser
password=yourpassword
list=yourlist
```

nc-tasks.py:
```
Welcome to Nextcloud tasks CLI.   Type help or ? to list commands.
(Nextcloud Tasks) ?

Documented commands (type help <topic>):
========================================
add    complete  delete  exit  list  nextcloud  print_all
close  connect   edit    help  load  print    

(Nextcloud Tasks) load
(Nextcloud Tasks) print
+---------+--------------------------------------+------------+----------+
| SUMMARY |                 UID                  | RELATED-TO | PRIORITY |
+---------+--------------------------------------+------------+----------+
|  Task 2 | d4910d0e-e82f-474c-8b96-39d51a078820 |    None    |    0     |
|  Task 3 | e823277e-08da-4e38-a98e-67f6e0301eb3 |    None    |    0     |
|  Task 1 | de92dbda-afba-4bf3-b924-57b4db08f3f2 |    None    |    3     |
+---------+--------------------------------------+------------+----------+
```

## Hacking

Pull requests are welcome. 

## License

[GPL](https://www.gnu.org/licenses/gpl-3.0.txt)
