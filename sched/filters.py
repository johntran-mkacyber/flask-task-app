from __future__ import division
import math

def do_datetime(dt, format=None):
    '''Jinja template filter to format a datetime object'''
    if dt is None:
        # By default, render an empty string
        return ''
    if format is None:
        # No format is given in the template call, so use a default format
        # 
        # Format time in its own strftime call in order to:
        # 1. Left-strip leading 0 in hour display
        # 2. Use 'am'/'pm' (lower case) instead of 'AM'/'PM'
        formatted_date = dt.strftime('%m/%d/%Y - %A')
        formatted_time = dt.strftime('%I:%M%p').lstrip('0').lower()
        formatted = '%s at %s' % (formatted_date, formatted_time)
    else:
        formatted = dt.strftime(format)
    return formatted

def do_duration(dur):
    '''Jinja template filter to format duration in seconds'''
    if not dur:
        return '00:00:00'
    secs = float(dur)
    if secs < 0.0:
        neg = "-"
        secs = secs*-1.0
    else:
        neg = ""
    if 0.0 <= secs < 60.0:
        hrs = 0.0
        mins = 0.0
        secs = math.floor(secs)
    elif 60.0 <= secs < 3600.0:
        hrs = 0.0
        mins = math.floor(secs/60.0)
        secs = math.floor(secs-(mins*60.0))
    else:
        hrs = math.floor(secs/3600.0)
        mins = math.floor((secs-(hrs*3600.0))/60.0)
        secs = math.floor(secs-(hrs*3600.0+mins*60.0))
    hrs, mins, secs = map(int, (hrs, mins, secs))
    return '{}{:0>2}:{:0>2}:{:0>2}'.format(neg, hrs, mins, secs)

def init_app(app):
    '''Initialize a Flask application with custom filters'''
    app.jinja_env.filters['datetime'] = do_datetime
    app.jinja_env.filters['duration'] = do_duration

