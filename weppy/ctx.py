# -*- coding: utf-8 -*-
"""
    weppy.ctx
    ---------

    Provides the current object. Used by application to deal with
    request, response, session (if loaded with pipeline).

    :copyright: (c) 2014-2018 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

import contextvars
import pendulum

from datetime import datetime

from ._internal import ContextVarProxy
from .language import T


class Context(object):
    def __init__(self):
        self.language = None

    @property
    def now(self):
        return pendulum.instance(datetime.utcnow())


class Current(object):
    __slots__ = ('_ctx',)

    def __init__(self):
        object.__setattr__(self, '_ctx', contextvars.ContextVar('ctx'))
        self._ctx.set(Context())

    def _init_(self, ctx_cls, app, scope):
        return self._ctx.set(ctx_cls(app, scope))

    def _close_(self, token):
        self._ctx.reset(token)

    @property
    def ctx(self):
        return self._ctx.get()

    def __getattr__(self, name):
        return getattr(self.ctx, name)

    def __setattr__(self, name, value):
        setattr(self.ctx, name, value)

    def __delattr__(self, name):
        delattr(self.ctx, name)

    @property
    def T(self):
        return T


current = Current()
request = ContextVarProxy(current._ctx, 'request')
response = ContextVarProxy(current._ctx, 'response')
session = ContextVarProxy(current._ctx, 'session')


def now():
    return current.now
