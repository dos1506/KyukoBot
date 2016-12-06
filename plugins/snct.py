from plugins.kyuko import fetchKyukoInfo
from rtmbot.core import Plugin
import re

class kyukoPlugin(Plugin):

    status_map = {'henko': '変更', 'kyuko': '休講'}

    def process_message(self, data):
        channel = data['channel']
        text = data['text']

        if channel.startswith('D'):

            if text.startswith('kyuko'):

                match = re.match('kyuko (.*)', text)

                if match:
                    department = match.group(1)
                else:
                    department = None

                kyuko_all = fetchKyukoInfo()

                kyuko = list()
                for record in kyuko_all:

                    if (not department) or (record.department == department):
                        kyuko.append(self.record_formatting(record))

                if not kyuko:
                    self.outputs.append([channel, 'Nothing'])
                else:
                    self.outputs.append([channel, '\n'.join(kyuko)])


    def record_formatting(self, record):
        return '{month}月{day}日({date}) {department} {time} {subject} {teacher} [{status}]'\
               .format(month=record.date[0], day=record.date[1], date=record.date[2],\
                       department=record.department, time=record.time, subject=record.subject,\
                       teacher=record.teacher, status=self.status_map[record.status])

