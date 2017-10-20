#!/usr/bin/python

import sys,os


class Main:

    def __init__(self, stack):
        self.stack = stack
        #VARIABLES DE ACCESO A RANCHER
        self.rancherUrl = 'http://172.17.0.2:8080'
        self.accessKey = 'B7050CC048EE53A2D4F3'
        self.privateKey = 'ScQezVwW18q2JwQ1hf6k3d39jXpJdyxD2M2tK4jV'
        #COMANDOS DE EJECUCION EN RANCHER
        self.initCmd = 'rancher --wait {0} {1} --type stack'
        self.healthState = 'rancher inspect --format {{.healthState}} --type stack '
        self.status = '{0} status is {1}'

    def start(self):
        command = self.initCmd.format('start', self.stack)
        state = self.checkhealthstate()
        output  = ''
        if state == 'unhealthy':
            print 'Starting ', self.stack
            output = self.launch(command)
        return output

    def stop(self):
        command = self.initCmd.format('stop', self.stack)
        state = self.checkhealthstate()
        output = ''
        if state == 'healthy':
            print 'Stopping ', self.stack
            output = self.launch(command)
        return output

    def restart(self):
        command = self.initCmd.format('restart', self.stack)
        state = self.checkhealthstate()
        output = ''
        if state == 'healthy':
            print 'Restarting ', self.stack
            output = self.launch(command)
        return output

    def checkhealthstate(self):
        return os.popen(self.healthState + self.stack).read().strip()

    def launch(self, command):
        output = os.popen(command).read().strip()
        return output


if __name__ == "__main__":
    stack = sys.argv[1]
    order = sys.argv[2]
    main = Main(stack)
    output = ''
    if order == 'start':
        output = main.start()
    elif order == 'stop':
        output = main.stop()
    elif order == 'restart':
        output = main.restart()
    elif order == 'status':
        print main.status.format(stack, main.checkhealthstate())
    sys.exit(0)