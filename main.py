#!/usr/bin/python

import sys,os


class App:

    def __init__(self, stack):
        self.stack = stack
        self.rancherUrl = 'http://172.17.0.2:8080'
        self.initCmd = 'rancher --wait {0} {1} --type stack'
        self.upgradeCmd = 'rancher-compose --access-key {0} --secret-key {1} --url {2} -f {3}_docker.compose.yml'
        self.accessKey = 'B7050CC048EE53A2D4F3'
        self.privateKey = 'ScQezVwW18q2JwQ1hf6k3d39jXpJdyxD2M2tK4jV'
        self.healthState = 'rancher inspect --format {{.healthState}} --type stack '
        self.status = '{0} status is {1}'

    def start(self):
        command = self.initCmd.format('start', self.stack)
        state = self.checkhealthstate()
        if state == 'unhealthy':
            print 'Starting ', self.stack
            self.launch(command)

    def stop(self):
        command = self.initCmd.format('stop', self.stack)
        state = self.checkhealthstate()
        if state == 'healthy':
            print 'Stopping ', self.stack
            self.launch(command)

    def restart(self):
        command = self.initCmd.format('restart', self.stack)
        state = self.checkhealthstate()
        if state == 'healthy':
            print 'Restarting ', self.stack
            self.launch(command)

    def upgrade(self):
        command = self.upgradeCmd.format(self.accessKey, self.privateKey, self.rancherUrl, self.stack)
        self.launch(command)

    def checkhealthstate(self):
        return os.popen(self.healthState + self.stack).read().strip()

    def launch(self, command):
        output = os.popen(command).read().strip()


if __name__ == "__main__":
    stack = sys.argv[1]
    order = sys.argv[2]
    a = App(stack)
    if order == 'start':
        a.start()
    elif order == 'stop':
        a.stop()
    elif order == 'restart':
        a.restart()
    elif order == 'upgrade':
        a.upgrade()
    elif order == 'status':
        print a.status.format(stack, a.checkhealthstate())
