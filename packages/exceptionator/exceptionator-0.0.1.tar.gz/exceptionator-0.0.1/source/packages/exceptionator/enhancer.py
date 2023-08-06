
import inspect

class EnhancedErrorMixIn:
    def __init__(self, *args, **kwargs):
        self._context = {}
        return

    @property
    def context(self):
        return self._context

    def add_context(self, content, label="CONTEXT"):
        """
            Adds context to an exception and associates it with the function context
            on the stack.
        """
        caller_stack = inspect.stack()[2]
        caller_func_name = caller_stack.frame.f_code.co_name

        self._context[caller_func_name] = {
            "label": label,
            "content": content
        }

        return

def enhance_exception(xcpt: BaseException, content, label="CONTEXT"):
    """
        Allows for the enhancing of exceptions.
    """

    # EnhancedErrorMixIn just uses Duck typing so it should be safe to dynamically
    # append any exception that does not already inherit include EnhancedErrorMixIn
    # in its base clases list.
    xcpt_type = type(xcpt)

    if EnhancedErrorMixIn not in xcpt_type.__bases__:
        xcpt_type.__bases__ += (EnhancedErrorMixIn,)
        xcpt._context = {}

    xcpt.add_context(content, label=label)

    return