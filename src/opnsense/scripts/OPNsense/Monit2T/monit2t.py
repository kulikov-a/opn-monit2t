#!/usr/bin/env python3

# send monit alert to telegram bot
# using HTML markup https://core.telegram.org/bots/api#formatting-options

import sys
import os
import re
import syslog
import requests
from configparser import ConfigParser


def t_send(token, chat_id, message_thread_id, message):
    t_url = f'https://api.telegram.org/bot{token}/sendMessage'
    syslog.openlog('monit')
    try:
        # restore multiline (if any) message and send to endpoint
        if message_thread_id:
            resp = requests.post(t_url, json={'chat_id': chat_id, 'message_thread_id': message_thread_id, 'text': message.replace(r'\n', '\n'), 'parse_mode': 'HTML'})
        else:
            resp = requests.post(t_url, json={'chat_id': chat_id, 'text': message.replace(r'\n', '\n'), 'parse_mode': 'HTML'})
    except requests.exceptions.Timeout:
        syslog.syslog(syslog.LOG_ERR, 'Telegram API endpoint request timeout')
        sys.exit('Telegram API endpoint request timeout')
    except requests.exceptions.TooManyRedirects:
        syslog.syslog(syslog.LOG_ERR, 'Telegram API endpoint returned error: ' + resp.text)
        sys.exit(resp.text)
    except requests.exceptions.RequestException as e:
        syslog.syslog(syslog.LOG_ERR, 'Telegram API endpoint returned error: ' + resp.text)
        sys.exit(resp.text)
    if resp.status_code == 200:
        syslog.syslog(syslog.LOG_NOTICE, 'Telegram message sent.')
        return resp.text
    else:
        syslog.syslog(syslog.LOG_ERR, 'Telegram API endpoint returned error: ' + resp.text)
        sys.exit(resp.text)
    
t_conf = '/usr/local/opnsense/scripts/OPNsense/Monit2T/monit2t.conf'
if os.path.exists(t_conf):
    cnf = ConfigParser()
    cnf.read(t_conf)
    token = str(cnf['api_settings']['token'])
    chat_id = str(cnf['api_settings']['chat_id'])
    message_thread_id = str(cnf['api_settings']['message_thread_id'])
    message = str(cnf['alert_settings']['message'])
    if len(sys.argv) == 1:
        msg_vars = re.findall(r"{([^{]*?)}", message)
        env_vars={}
        for msg_var in msg_vars:
            env_vars[msg_var] = os.getenv(msg_var, "null").replace('<','&lt').replace('>','&gt')
        t_send(token, chat_id, message_thread_id, message.format(**env_vars))
    else:
        message = 'This is a test telegram message\nAlerts will be sent in the following format: \n\n' + message
        t_send(token, chat_id, message_thread_id, message)
