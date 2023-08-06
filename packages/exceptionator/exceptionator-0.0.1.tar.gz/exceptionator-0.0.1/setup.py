# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['exceptionator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'exceptionator',
    'version': '0.0.1',
    'description': 'The Exceptionator Package',
    'long_description': '# Exceptionator\nThe `exceptionator` module provides methods for enhancing ordinary python\nexceptions with a context which allows for the addition of contextual\ninformation about was was going on when an exception was thrown and what\nthe contextual state of the code on the stack was.\n\n```{python}\n\ndef failing_function():\n    raise TestError("This is a test error")\n\nclass TestEnhancer(unittest.TestCase):\n\n    def test_enhance_exception(self):\n\n        try:\n            failing_function()\n        except TestError as terr:\n            exceptionator.enhance_exception(terr, "This is some extra content.", "BLAH")\n\n            tblines = exceptionator.format_exception(terr)\n\n            for line in tblines:\n                print(line)\n\n        return\n\n```\n\nThe output of the code above shows an example of how the `enhance_exception` method is\nused to add contextual information about the state in which an exception occured.\n\nThe `exceptionator` module also allows for control of code output in at different levels\nof the stacktrace output.  Modules can add a declaration that instructs the `exceptionator`\ncode on how to output stack trace information for a given module.  The select of output policy\nis accomplished by applying a policy declaration to each module like so.\n\n```\n\n__traceback_format_policy__ = "Brief"\n\n\n```\n\nThe possible trackback policies are:\n\n```\nclass TracebackFormatPolicy:\n    Brief = "Brief"\n    Full = "Full"\n    Hide = "Hide"\n```\n\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
