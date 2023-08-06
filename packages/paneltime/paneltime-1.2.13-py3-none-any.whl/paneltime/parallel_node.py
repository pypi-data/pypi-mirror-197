#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import parallel
from . import parallel_slave

parallel_slave.run(parallel.Transact(sys.stdin,sys.stdout), True)

