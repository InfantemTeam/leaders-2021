#!/usr/bin/env python3

from .app import app


def main():
	app.env = 'development'
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run('unix', '///tmp/leaders.sock', debug=False, autoreload=True)

if (__name__ == '__main__'): exit(main())


# by InfantemTeam, 2021
# infantemteam@sdore.me
