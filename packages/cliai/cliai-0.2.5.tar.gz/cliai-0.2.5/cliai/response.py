#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygments.lexer import RegexLexer
from pygments.token import Comment, Generic, Text

# Test: python -m pygments -x -l response.py:ResponseLexer text.txt


class ResponseLexer(RegexLexer):
    name = 'ResponseLexer'
    tokens = {
        'root': [
            (r'^As\ an\ AI\ language\ model.*?\.', Generic.Deleted),
            (r'[ ^]`(.*?)`', Comment.Preproc),
            (r'^```(.*?$\n)?(.*?\n)+?^```$', Comment.Preproc),
            (r'.+?', Text),
        ]
    }

class InputLexer(RegexLexer):
    pass
