#!/usr/bin/env python
# -*- coding:utf-8 -*-
from mitmproxy import ctx

def request(flow):
    request = flow.request
    ctx.log.info(request.url)
    ctx.log.info(request.host)
    # ctx.log.info(str(request.headers))
    flow.request.method = "GET"
    flow.request.url = ""

    return