#!/usr/bin/python

from cmd import Cmd
import sys
import os
import json
import TemplateHost
from TemplateHost import TemplateHost

class VCTool(Cmd):
    prompt = 'vctool > '
    intro = "[ VCENTER-TOOL ]\nType help for options.\nType exit or q to quit."
    hosts = []
    # I have NO CLUE how vulnerabilities/services are made
    vulns = []
    templates = []

    ## Pull relevant host information from JSON file
    def get_templates_info(self):
            templates = []
            with open('templates/info.json') as f:
                data = json.load(f)
                for host in data['templates']:
                    new_temp = TemplateHost(
                        host['file'],
                        host['hostname'],
                        host['description'],
                        host['os'])
                    templates.append(new_temp)
            self.templates = templates
    
    ## Get host information only once
    def preloop(self):
        self.get_templates_info()

    def precmd(self, line):
        self.get_templates_info()
        return line

    ## List of commands
    def do_help(self, inp):
        print("1) host []\n   host add [host] [name] \n   host list \n   host current \n   host rm [name]")
        print("3) add vuln [host] [vuln] \n4) generate \n5) load [script] \n6) list vuln [host]")

    ## All host related actions: add host, list hosts available, list current hosts, and remove host
    def do_host(self, inp):
        options = inp.split()
        if len(options) > 0:
            # vuln or host
            if options[0] == 'add':
                if len(options) > 2:
                    hostname, name = options[1:3]

                    host = None
                    for temp in self.templates:
                        if temp.hostname == hostname:
                            host = temp
                            break

                    if host is not None:
                        self.hosts.append((host, name))
                    else:
                        print("Incorrect host.")
                else:
                    print("usage: host add [host] [name]")

            elif options[0] == 'list':
                for t in self.templates:
                    print(f"\nHost: {t.hostname}\nDesc: {t.description}\nOS: {t.os}")
                    print("--------------------------------------------------")

            elif options[0] == 'current':
                print("[name: host]")
                for x in self.hosts:
                    print(f"{x[1]}: {x[0].hostname}")

            elif options[0] == 'rm':
                if len(options) > 1:
                    name = options[1]
                    rm_host = None
                    if len(self.hosts) > 0:
                        for host in self.hosts:
                            if host[1] == name:
                                rm_host = host
                                break
                        if rm_host is not None:
                            self.hosts.remove(rm_host)
                    else:
                        print("No hosts to remove.")
                else:
                    print("usage: host rm [name]")
            else:
                print("Type help for options.")
        else:
            print("usage: \n   add [host] [name] \n   host list \n   host current \n   host rm [name]")

    def do_add(self, inp):
        options = inp.split()
        if len(options) > 0:
            if options[0] == 'vuln':
                if len(options) > 2:
                    host, vuln = options[1:3]
                    # [Insert relevant actions with this information]
                else:
                    print("List of vulnerabilities:")
                    # Relevant list                
        else:
            print("usage: add vuln [host] [vuln]")

    def do_list(self, inp):
        options = inp.split()
        if len(options) > 0:
            if options[0] == 'vuln':
                if len(options) > 1:
                    host = options[1]
                    # [Insert relevant actions with this information]
                else:
                    print("list vuln [host]")              
        else:
            print("usage: list vuln [host]")

    ## Generate laforge script
    def do_generate(self, inp):
        print("Hosts:")
        if len(self.hosts) > 0:
            for x in self.hosts:
                print(f"{x[1]}: {x[0].hostname}")
        else:
            print("No hosts.")
        print("Services:") # Vulnerabilities??
        if_gen = input("Would you like to generate a script with this information? (y/n): ")
        if if_gen.lower() == 'n' or if_gen.lower() != 'y':
            print("Not generating a script.")
        else:
            scr_name = input("Script name: ")
            print(f"Generating script {scr_name}...")

            self.create_hosts()

    ## Load laforge script (and deploy?)
    def do_load(self, inp):
        options = inp.split()
        if len(options) < 1:
            print("usage: load [script]")
        else:
            script = options[0]
            print("Loading script", script)
            # [Insert relevant actions with this information]    
    
    def do_exit(self, inp):
        print("Bye.")
        return True

    def default(self, inp):
        if inp == 'q':
            return self.do_exit(inp)

    do_EOF = do_exit

    ## Create necessary host files from user information
    def create_hosts(self):
        for h in self.hosts:
            template_file = h[0].file
            with open(f'templates/{template_file}', 'r') as tf:
                data = tf.readlines()
            data[2] = f'  hostname = \"{h[1]}\"\n'
            with open(f'createdhosts/{h[1]}.laforge.tmpl', 'w') as f:
                f.writelines(data)

if len(sys.argv) > 1:
    VCTool().onecmd(' '.join(sys.argv[1:]))
else:
    VCTool().cmdloop()