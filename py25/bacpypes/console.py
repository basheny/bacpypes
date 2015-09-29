#!/usr/bin/env python

"""
Console Communications
"""

import sys
import asyncore

from .debugging import bacpypes_debugging, ModuleLogger

from .core import deferred
from .comm import PDU, Client, Server

# some debugging
_debug = 0
_log = ModuleLogger(globals())

#
#   asyncore.file_dispatcher is only available in Unix.  This is a hack that
#   allows the ConsoleClient and ConsoleServer to initialize on Windows.
#

try:
    asyncore.file_dispatcher
except:
    class _barf:
        def __init__(self, *args):
            pass
    asyncore.file_dispatcher = _barf


#
#   ConsoleClient
#

class ConsoleClient(asyncore.file_dispatcher, Client):

    def __init__(self, cid=None):
        ConsoleClient._debug("__init__ cid=%r", cid)
        asyncore.file_dispatcher.__init__(self, sys.stdin)
        Client.__init__(self, cid)

    def readable(self):
        return True     # We are always happy to read

    def writable(self):
        return False    # we don't have anything to write

    def handle_read(self):
        deferred(ConsoleClient._debug, "handle_read")
        data = sys.stdin.read()
        deferred(ConsoleClient._debug, "    - data: %r", data)
        deferred(self.request, PDU(data))

    def confirmation(self, pdu):
        deferred(ConsoleClient._debug, "confirmation %r", pdu)
        try:
            sys.stdout.write(pdu.pduData)
        except Exception, err:
            ConsoleClient._exception("Confirmation sys.stdout.write exception: %r", err)

bacpypes_debugging(ConsoleClient)

#
#   ConsoleServer
#

class ConsoleServer(asyncore.file_dispatcher, Server):

    def __init__(self, sid=None):
        ConsoleServer._debug("__init__ sid=%r", sid)
        asyncore.file_dispatcher.__init__(self, sys.stdin)
        Server.__init__(self, sid)

    def readable(self):
        return True     # We are always happy to read

    def writable(self):
        return False    # we don't have anything to write

    def handle_read(self):
        deferred(ConsoleServer._debug, "handle_read")
        data = sys.stdin.read()
        deferred(ConsoleServer._debug, "    - data: %r", data)
        deferred(self.response, PDU(data))

    def indication(self, pdu):
        deferred(ConsoleServer._debug, "Indication %r", pdu)
        try:
            sys.stdout.write(pdu.pduData)
        except Exception, err:
            ConsoleServer._exception("Indication sys.stdout.write exception: %r", err)

bacpypes_debugging(ConsoleServer)
