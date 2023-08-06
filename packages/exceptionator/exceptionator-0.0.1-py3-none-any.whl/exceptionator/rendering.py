"""
.. module:: rendering
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the exception rendering helper functions and meta data declarations.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import List

import inspect
import os
import traceback


MEMBER_TRACE_POLICY = "__traceback_format_policy__"


class TracebackFormatPolicy:
    Brief = "Brief"
    Full = "Full"
    Hide = "Hide"


VALID_MEMBER_TRACE_POLICY = ["Brief", "Full", "Hide"]


class TRACEBACK_CONFIG:
    TRACEBACK_POLICY_OVERRIDE = None
    TRACEBACK_MAX_FULL_DISPLAY = 10


def split_and_indent_lines(msg: str, level: int, indent: int=4, pre_strip_leading: bool=True) -> List[str]:
    """
        Takes a string and splits it into multiple lines, then indents each line
        to the specified level using 'indent' spaces for each level.

        :param msg: The text content to split into lines and then indent.
        :param level: The integer level number to indent to.
        :param indent: The number of spaces to indent for each level.
        :param pre_strip_leading: Strip any leading whitesspace before indenting the lines.

        :returns: The indenting lines
    """

    # Split msg into lines keeping the line endings
    msglines = msg.splitlines(False)

    prestrip_len = len(msg)
    if pre_strip_leading:
        for nxtline in msglines:
            stripped = nxtline.lstrip()
            striplen = len(nxtline) - len(stripped)
            if striplen < prestrip_len:
                prestrip_len = striplen

    pfx = " " * (level * indent)

    indented = None
    if pre_strip_leading and prestrip_len > 0:
        indented = [pfx + nxtline[prestrip_len:] for nxtline in msglines]
    else:
        indented = [pfx + nxtline for nxtline in msglines]

    return indented

def collect_stack_frames(calling_frame, ex_inst):

    max_full_display = TRACEBACK_CONFIG.TRACEBACK_MAX_FULL_DISPLAY

    last_items = None
    tb_code = None
    tb_lineno = None

    tb_frames = []

    for tb_frame, tb_lineno in traceback.walk_stack(calling_frame):
        tb_frames.insert(0, (tb_frame, tb_lineno))
        if tb_frame.f_code.co_name == '<module>':
            break 

    tb_frames.pop()

    for tb_frame, tb_lineno in traceback.walk_tb(ex_inst.__traceback__):
        tb_frames.append((tb_frame, tb_lineno))

    tb_frames.reverse()

    traceback_list = []

    for tb_frame, tb_lineno in tb_frames:
        tb_code = tb_frame.f_code
        co_filename: str = tb_code.co_filename
        co_name: str = tb_code.co_name
        co_arg_names = tb_code.co_varnames[:tb_code.co_argcount]
        co_argcount = tb_code.co_argcount
        co_locals = tb_frame.f_locals

        co_format_policy = TracebackFormatPolicy.Full

        if TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE is None:
            co_module = inspect.getmodule(tb_code)
            if co_module and hasattr(co_module, MEMBER_TRACE_POLICY):
                cand_format_policy = getattr(co_module, MEMBER_TRACE_POLICY)
                if cand_format_policy in VALID_MEMBER_TRACE_POLICY:
                    co_format_policy = cand_format_policy
        else:
            co_format_policy = TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE

        items = [co_filename, tb_lineno, co_name, "", None]
        if last_items is not None:
            code_args = []
            for argidx in range(0, co_argcount):
                argname = co_arg_names[argidx]
                argval = co_locals[argname]
                code_args.append("%s=%r" % (argname, argval))

            last_items[-2] = "%s(%s)" % (co_name, ", ".join(code_args)) # pylint: disable=unsupported-assignment-operation

        last_items = items

        traceback_list.append(items)
        last_items = items

        if max_full_display > 0 and co_format_policy == TracebackFormatPolicy.Full \
            and os.path.exists(co_filename) and co_filename.endswith(".py"):
            context_lines, context_startline = inspect.getsourcelines(tb_code)
            context_lines = [cline.rstrip() for cline in context_lines]
            clindex = (tb_lineno - context_startline)
            last_items[-2] = context_lines[clindex].strip()
            last_items[-1] = context_lines
            max_full_display -= 1

    return traceback_list


def format_exception(ex_inst: BaseException):

    etypename = type(ex_inst).__name__
    eargs = ex_inst.args

    exmsg_lines = [
        "%s: %s" % (etypename, repr(eargs).rstrip(",")),
        "TRACEBACK (most recent call last):"
    ]

    previous_frame = inspect.currentframe().f_back

    stack_frames = collect_stack_frames(previous_frame, ex_inst)
    stack_frames_len = len(stack_frames)

    for co_filename, co_lineno, co_name, co_code, co_context in stack_frames:

        exmsg_lines.extend([
            '  File "%s", line %d, in %s' % (co_filename, co_lineno, co_name),
            "    %s" % co_code
        ])

        if hasattr(ex_inst, "context") and co_name in ex_inst.context:
            cxtinfo = ex_inst.context[co_name]
            exmsg_lines.append('    %s:' % cxtinfo["label"])
            exmsg_lines.extend(split_and_indent_lines(cxtinfo["content"], 2, indent=3))

        if co_context is not None and len(co_context) > 0 and stack_frames_len > 1:
            exmsg_lines.append('    CODE:')
            firstline = co_context[0]
            lstrip_len = len(firstline) - len(firstline.lstrip())
            co_context = [cline[lstrip_len:] for cline in co_context]
            co_context = ["      %s" % cline for cline in co_context]
            exmsg_lines.extend(co_context)
        exmsg_lines.append('')

    return exmsg_lines

