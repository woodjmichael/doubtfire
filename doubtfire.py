'''
doubtfire.py checks up on your regular data harvesting tasks and send you an email if something
is missing
'''
__author__ = 'Michael Wood'
__email__ = 'michael.wood@mugrid.com'
__copyright__ = 'Copyright 2022, muGrid Analytics'
__version__ = '1.1'

import os
import csv
from configparser import ConfigParser
import datetime as dt
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class LogFile:
    '''
    Helpful with logging
    '''
    def __init__(self, logname):
        '''
        Check if logfile exists, create if not, then read logfile
        '''
        self.filename = logname
        if not os.path.isfile(logname):
            self.create_logfile()
        self.df = pd.read_csv(self.filename, index_col=0, parse_dates=True)

    def write(self, note):
        '''
        Add new line to log
        '''    
        self.df.loc[len(self.df)] = [dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M'), note]
        self.df = self.df.sort_index(ascending=False)

    def no_entry_today(self):
        '''
        Check if there is a log entry from today
        '''
        dt_last_log = dt.datetime.fromisoformat( self.df['Log datetime UTC'].iloc[0] )
        if dt_last_log.date() == dt.datetime.utcnow().date():
            return False
        return True

    def close(self, note = None):
        '''
        Save to logfile
        '''
        if note:
            self.write(note)       
        self.df.to_csv(self.filename)

    def create_logfile(self):
        '''
        Create new log if none
        '''
        with open(self.filename,'w',newline='',encoding='utf-8') as newfile:
            writer=csv.writer(newfile)
            writer.writerow(',Log datetime UTC,Note'.split(','))
            writer.writerow('0,2000-01-01 00:00,First note'.split(','))


def send_alert_email(dt_last_entry, cfg):
    '''
    Build and send the alert email
        Parmaeters: dt_last_entry (datetime): when the last log entry was
        Returns: status code of the api request
    '''
    emails = cfg['emails']['email_list'].split('\n') # returns a list
    
    # Build and send email
    message = Mail(
        from_email='michael.wood@mugrid.com',
        to_emails=emails,
        subject='Automated: Open Weather Forecast Failure',
        html_content=f'Last forecast was {dt_last_entry} for at least one file. <br><br><br><img src="https://i.imgflip.com/11fjj7.jpg"/>')
    try:
        api_key = os.getenv('SENDGRID_API_KEY')
        api = SendGridAPIClient(api_key)
        response = api.send(message)
        stat = f'{response.status_code}'
    except Exception as ex:
        stat = ex
    return stat


config = ConfigParser()
config.read('setup.cfg')
log = LogFile('open-weather.log')

files_out_of_date = []
if log.no_entry_today():
    for filename in config['open-weather']['files_to_check'].split('\n'):
        df = pd.read_csv(config['open-weather']['dir'] + filename,
                        index_col=0, parse_dates=True, usecols=[0,1])
        last_forecast_utc = dt.datetime.fromisoformat(df.iloc[-1, 0])
        diff = dt.datetime.utcnow() - last_forecast_utc
        diff = diff.total_seconds()/3600 # hours
        log.write(f'Daily check: {filename} last entry from {diff:.1f} hours ago')
        if diff > 24: # hours
            files_out_of_date.append(filename)
    if files_out_of_date:
        # Email only once, even if multiple files out of date
        status = send_alert_email(last_forecast_utc, config)
        log.write(f'Forecast data more than 1 day old for {files_out_of_date} - email status {status}')

log.close('doubtfire.py run to completion')
