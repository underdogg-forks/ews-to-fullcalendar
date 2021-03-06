# pylint: skip-file
# FIXME: Reenable pylint when updated to 2.0
# Flask(__name__) breaks pylint 1.6 on python 3.6

from flask import Flask, request

from ews_to_fullcalendar import (get_all_cached_fc_events,
	get_cached_fc_events_between, get_saved_ical)

from exchangelib import EWSTimeZone

import json, os, tzlocal

TIMEZONE = os.environ.get('EWS_TIMEZONE', tzlocal.get_localzone().zone)
ALLOWED_ORIGIN = os.environ.get('EWS_ALLOWED_ORIGIN', '*')

app = Flask(__name__)

tz = EWSTimeZone.timezone(TIMEZONE)

@app.route('/fullcalendar')
def fullcalendar():
	start = request.args.get('start', None)
	end = request.args.get('end', None)

	if start and end:
		events = get_cached_fc_events_between(start, end)
	else:
		events = get_all_cached_fc_events()

	return (
		json.dumps([event.to_dict() for event in events], indent='\t'),
		{
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': ALLOWED_ORIGIN
		}
	)

@app.route('/ical.ics')
def ical():
	return (
		get_saved_ical(),
		{
			'Content-Type': 'text/calendar',
			'Access-Control-Allow-Origin': ALLOWED_ORIGIN
		}
	)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
