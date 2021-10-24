#!/usr/bin/env python3

from . import *

app = Quart(__name__)
app.config.from_object('config')
am = AuthManager(app)

from . import main

# by InfantemTeam, 2021
# infantemteam@sdore.me
