# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polymer']

package_data = \
{'': ['*']}

install_requires = \
['loguru==0.6.0']

setup_kwargs = {
    'name': 'polymer',
    'version': '1.0.3',
    'description': 'Manage parallel tasks',
    'long_description': '\n# New Summary - Do not use this package\n\nIn many cases, this package can be replaced by Python3\'s [`concurrent.futures.ProcessPoolExecutor()`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor).  As of 2023, this package is vulnerable to process deadlocks, and in-general Python3 tripping all over itself. These problems are better solved in `concurrent.futures`.  At some point in the future, I may rewrite `polymer` as a wrapper around `concurrent.futures`.\n\n# Original Summary\n\nA simple framework to run tasks in parallel.  It\'s similar to [`multiprocessing.Pool`](https://docs.python.org/3/library/multiprocessing.html#using-a-pool-of-workers), but has a few enhancements over that.  For example, `mp.Pool` is only useful for multiprocessing functions (not objects).  You can wrap a function around the object, but it\'s nicer just to deal with task objects themselves.\n\n`polymer` is mostly useful for its Worker error logging and run-time statistics.  It also restarts crashed multiprocessing workers automatically (not true with multiprocessing.Pool).  When a worker crashes, `polymer` knows what the worker was doing and resubmits that task as well.  This definitely is not fool-proof; however, it\'s a helpful feature.\n\nOnce `TaskMgr().supervise()` finishes, a list of object instances is returned.  You can store per-task results as an attribute of each object instance.\n\n# Usage\n\n```python\nimport time\n\nfrom polymer.Polymer import ControllerQueue, TaskMgr\nfrom polymer.abc_task import BaseTask\n\nclass SimpleTask(BaseTask):\n    def __init__(self, text="", wait=0.0):\n        super(SimpleTask, self).__init__()\n        self.text = text\n        self.wait = wait\n\n    def run(self):\n        """run() is where all the work is done; this is called by TaskMgr()"""\n        ## WARNING... using try / except in run() could squash Polymer\'s\n        ##      internal error logging...\n        #time.sleep(float(self.wait/10))\n        print(self.text, self.wait/10.0)\n\n    def __eq__(self, other):\n        """Define how tasks are uniquely identified"""\n        if isinstance(other, SimpleTask) and (other.text==self.text):\n            return True\n        return False\n\n    def __repr__(self):\n        return """<{0}, wait: {1}>""".format(self.text, self.wait)\n\n    def __hash__(self):\n        return id(self)\n\ndef Controller():\n    """Controller() builds a list of tasks, and queues them to the TaskMgr\n    There is nothing special about the name Controller()... it\'s just some\n    code to build a list of SimpleTask() instances."""\n\n    tasks = list()\n\n    ## Build ten tasks... do *not* depend on execution order...\n    num_tasks = 10\n    for ii in range(0, num_tasks):\n        tasks.append(SimpleTask(text="Task {0}".format(ii), wait=ii))\n\n    targs = {\n        \'work_todo\': tasks,  # a list of SimpleTask() instances\n        \'hot_loop\': False,   # If True, continuously loop over the tasks\n        \'worker_count\': 3,           # Number of workers (default: 5)\n        \'resubmit_on_error\': False,  # Do not retry errored jobs...\n        \'queue\': ControllerQueue(),\n        \'worker_cycle_sleep\': 0.001, # Worker sleep time after a task\n        \'log_stdout\': False,         # Don\'t log to stdout (default: True)\n        \'log_path\':  "taskmgr.log",  # Log file name\n        \'log_level\': 0,              # Logging off is 0 (debugging=3)\n        \'log_interval\': 10,          # Statistics logging interval\n    }\n\n    ## task_mgr reads and executes the queued tasks\n    task_mgr = TaskMgr(**targs)\n\n    ## a set() of completed task objects are returned after supervise()\n    results = task_mgr.supervise()\n    return results\n\nif __name__==\'__main__\':\n    Controller()\n```\n\n\nLicense\n-------\n\nGPLv3\n',
    'author': 'Mike Pennington',
    'author_email': 'mike@pennington.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mpenning/polymer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
