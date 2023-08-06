# Exceptionator
The `exceptionator` module provides methods for enhancing ordinary python
exceptions with a context which allows for the addition of contextual
information about was was going on when an exception was thrown and what
the contextual state of the code on the stack was.

```{python}

def failing_function():
    raise TestError("This is a test error")

class TestEnhancer(unittest.TestCase):

    def test_enhance_exception(self):

        try:
            failing_function()
        except TestError as terr:
            exceptionator.enhance_exception(terr, "This is some extra content.", "BLAH")

            tblines = exceptionator.format_exception(terr)

            for line in tblines:
                print(line)

        return

```

The output of the code above shows an example of how the `enhance_exception` method is
used to add contextual information about the state in which an exception occured.

The `exceptionator` module also allows for control of code output in at different levels
of the stacktrace output.  Modules can add a declaration that instructs the `exceptionator`
code on how to output stack trace information for a given module.  The select of output policy
is accomplished by applying a policy declaration to each module like so.

```

__traceback_format_policy__ = "Brief"


```

The possible trackback policies are:

```
class TracebackFormatPolicy:
    Brief = "Brief"
    Full = "Full"
    Hide = "Hide"
```


