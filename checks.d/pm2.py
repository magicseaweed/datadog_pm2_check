#  PYTHONPATH=.:/usr/share/datadog/agent/ python checks.d/pm2.py
import subprocess
import json
import time

from checks import AgentCheck

class Pm2(AgentCheck):

    def load_json(self, command):
        p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.communicate()
        self.log.info('Raw data from: %s' % command)
        self.log.info(out)
        return json.loads(out[0])

    def check(self, instance):

        for proc in self.load_json(instance['command']):
            tags = [
                "node_id:%s" % proc['pm2_env']['NODE_APP_INSTANCE'],
                'name:%s' % proc['name'],
                'pm_id:%s' % proc['pm_id']
            ]

            # cpu, memory, errors, processes, restart
            self.gauge('pm2.processes.cpu', proc['monit']['cpu'], tags=tags)
            self.gauge('pm2.processes.memory', proc['monit']['memory'], tags=tags)
            self.gauge('pm2.processes.restart', proc['pm2_env']['restart_time'], tags=tags)
            self.gauge('pm2.processes.processes', proc['pm2_env']['instances'], tags=tags)

if __name__ == '__main__':
    check, instances = Pm2.from_yaml('conf.d/pm2.yaml')
    for instance in instances:
        print "\nRunning on %s" % instance['command']
        check.check(instance)
        if check.has_events():
            print "Events: %s" % check.get_events()
        print
        for m in check.get_metrics():
            print m

