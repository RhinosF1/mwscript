#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
MWPATH = '/srv/mediawiki/w'


def getScripts(args):
    scripts = {}
    script = args[1]
    if len(script.split('/')) == 1:
        script = f'{MWPATH}/maintenance/{args[1]}'
    else:
        scriptsplit = script.split('/')
        if scriptsplit[2] == 'removePII.php':
            raise Exception("RemovePII can't be executed with mwscript")
        script = f'{MWPATH}/{scriptsplit[0]}/{scriptsplit[1]}/maintenance/{scriptsplit[2]}'
    wiki = args[2]
    if wiki in ('all', 'foreachwikiindblist'):
        command = f'sudo -u www-data /usr/local/bin/foreachwikiindblist /srv/mediawiki/cache/databases.json {script}'
    elif wiki in ('extension', 'skin'):
        extension = input('Type the ManageWiki name of the extension or skin: ')
        scripts['generate'] = f'php {MWPATH}/extensions/MirahezeMagic/maintenance/generateExtensionDatabaseList.php --wiki=loginwiki --extension={extension}'  # noqa: E501
        command = f'sudo -u www-data /usr/local/bin/foreachwikiindblist /home/{os.getlogin()}/{extension}.json {script}'
    else:
        command = f'sudo -u www-data php {script} --wiki={wiki}'
    if len(sys.argv) == 4:
        command = f'{command} {args[3]}'
    scripts['main'] = command
    return scripts


def getLogCommand(command, return_value, pos):
    return f'/usr/local/bin/logsalmsg "{command} ({pos} - exit={str(return_value)}"'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('Not Enough Parameters')
    scripts = getScripts(sys.argv)
    print('Will execute:')
    for cmdtype in scripts.keys():
        print(scripts[cmdtype]['command'])
    confirm = input("Type 'Y' to confirm: ")
    if confirm.upper() == 'Y':
        for cmdtype in scripts.keys():
            scripts[cmdtype]['return'] = os.system(scripts[cmdtype]['command'])
        logcommand = getLogCommand(scrips['main']['command'], scripts['main']['return'], 'END')
        print('Done!')
    else:
        print('Aborted!')
