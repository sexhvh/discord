from sys import stdout
from random import choice
from requests import Session
from os import path, system, _exit
from threading import Thread, Lock
from colors import green, blue, reset
from time import strftime, gmtime, sleep

system('title [Lunar Spammer Beta]')
lock = Lock()
session = Session()
session.trust_env = False

class Main:
    def __init__(self):
        self.variables = {
            'tokens': [],
            'joined_tokens': [],
            'proxies': [],
            'num': 0,
            'proxy_num': 0,
            'completed': 0,
            'sent': 0,
            'joined': 0,
            'retries': 0
        }

        print("""%s 
                                      ██▓     █    ██  ███▄    █  ▄▄▄       ██▀███  
                                     ▓██▒     ██  ▓██▒ ██ ▀█   █ ▒████▄    ▓██ ▒ ██▒
                                     ▒██░    ▓██  ▒██░▓██  ▀█ ██▒▒██  ▀█▄  ▓██ ░▄█ ▒
                                     ▒██░    ▓▓█  ░██░▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██▀▀█▄  
                                     ░██████▒▒▒█████▓ ▒██░   ▓██░ ▓█   ▓██▒░██▓ ▒██▒
                                     ░ ▒░▓  ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░
                                     ░ ░ ▒  ░░░▒░ ░ ░ ░ ░░   ░ ▒░  ▒   ▒▒ ░  ░▒ ░ ▒░
                                       ░ ░    ░░░ ░ ░    ░   ░ ░   ░   ▒     ░░   ░ 
                                         ░  ░   ░              ░       ░  ░   ░     
                                                \n\n                                                %s\n\n""" % (blue(), reset()))
        Thread(target=self.grab_proxies).start()

    def start(self):
        if path.exists('Tokens.txt'):
            with open('Tokens.txt', 'r', encoding='UTF-8', errors='replace') as f:
                for line in f.read().splitlines():
                    if line != '':
                        self.variables['tokens'].append(line)
            if len(self.variables['tokens']) == 0:
                self.error_import(False)
        else:
            self.error_import(True)

        print(' %s[%s1%s] Join Server\n [%s2%s] Spam Server\n\n%s> %sSelect an option%s: ' % (blue(), reset(), blue(), reset(), blue(), reset(), blue(), reset()), end='')
        self.option = str(input())

        if self.option.upper() in ['1', 'Server Joiner']:
            print('%s> %sInvite%s: https://discord.gg/' % (reset(), blue(), reset()), end='')
            server = str(input())

            Thread(target=self.join_title).start()
            print()

            while self.variables['num'] < len(self.variables['tokens']):
                while True:
                    try:
                        Thread(target=self.join, args=(self.variables['tokens'][self.variables['num']], server, self.variables['proxies'][self.variables['proxy_num']],)).start()
                    except:
                        continue
                    else:
                        self.variables['num'] += 1
                        self.variables['proxy_num'] += 1
                        if self.variables['proxy_num'] >= len(self.variables['proxies']):
                            self.variables['proxy_num'] = 0
                        break
            
            while self.variables['completed'] < len(self.variables['tokens']):
                continue
            self.variables['num'] = 0
            self.variables['retries'] = 0
            print('\n%s> %s%s%s Accounts Joined%s!' % (reset(), green(), self.variables['joined'], blue(), reset()))
            self.spam_option()

        elif self.option.upper() in ['2', 'SPAM SERVER']:
            self.spam_option()

        else:
            print('%s> %sInvalid option%s.' % (reset(), blue(), reset()))
            system('title [Lunar Spammer Beta] Exiting..')
            sleep(3)
            _exit(0)

    def error_import(self, create):
        if create:
            open('Tokens.txt', 'a').close()
        print('%s> %sPut your tokens in Tokens.txt please...%s!' % (reset(), blue(), reset()))
        system('title [Lunar Spammer Beta] Exiting..')
        sleep(3)
        _exit(0)

    def spam_option(self):
        print('%s> %sMessage to Spam%s: ' % (reset(), blue(), reset()), end='')
        message = str(input())

        print('%s> %sChannel ID%s: ' % (reset(), blue(), reset()), end='')
        channel = str(input())
        
        print()

        if self.option.upper() in ['1', 'JOIN SERVER']:
            tokens = self.variables['joined_tokens']
        else:
            tokens = self.variables['tokens']

        Thread(target=self.spam_title).start()
        while True:
            try:
                Thread(target=self.spam, args=(tokens[self.variables['num']], message, channel, self.variables['proxies'][self.variables['proxy_num']],)).start()
            except IndexError:
                self.variables['num'] = 0
            else:
                self.variables['num'] += 1
                self.variables['proxy_num'] += 1
                if self.variables['proxy_num'] >= len(self.variables['proxies']):
                    self.variables['proxy_num'] = 0

    def grab_proxies(self):
        while True:
            try:
                all_proxies = session.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all&ssl=all&anonymity=all').text
            except:
                print('%s> %sPlease change your IP address%s.' % (reset(), blue(), reset()))
                system('title [Lunar Spammer Beta] Exiting..')
                sleep(3)
                _exit(0)
            else:
                for proxy in all_proxies.splitlines():
                    self.variables['proxies'].append(proxy)
                sleep(600)
                self.variables['proxies'].clear()

    def join_title(self):
        while self.variables['completed'] < len(self.variables['tokens']):
            system('title [Lunar Spammer Beta] Token..: %s/%s (%s%%) ^| Retries: %s' % (self.variables['completed'], len(self.variables['tokens']), round(((self.variables['completed'] / len(self.variables['tokens'])) * 100), 3), self.variables['retries']))
            sleep(0.4)
        system('title [Lunar Spammer Beta] Token..: %s/%s (%s%%) ^| Retries: %s' % (self.variables['completed'], len(self.variables['tokens']), round(((self.variables['completed'] / len(self.variables['tokens'])) * 100), 3), self.variables['retries']))

    def spam_title(self):
        while True:
            system('title [Lunar Spammer Beta] Sent..: %s ^| Retries: %s' % (self.variables['sent'], self.variables['retries']))
            sleep(0.4)

    def write(self, arg):
        lock.acquire()

        # Decrease printing bugs on Windows
        stdout.flush()
        stdout.write('%s\n'.encode('ascii', 'replace').decode() % (arg))

        lock.release()

    def join(self, token, server, proxy):
        headers = {'Authorization': token, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Accept': '*/*',}

        try:
            join_server = session.post('https://discord.com/api/v6/invites/%s' % (server), headers=headers, proxies={'https': 'http://%s' % (proxy)}, timeout=4).text

            if 'You need to verify your account' in join_server:
                self.variables['completed'] += 1
                self.write('%s[%s%s%s] Your token is not authenticated%s.' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset()))

            elif 'Unauthorized' in join_server:
                self.variables['completed'] += 1
                self.write('%s[%s%s%s] Malfunctioning token%s.' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset()))

            elif 'banned from this guild' in join_server:
                self.variables['completed'] += 1
                self.write('%s[%s%s%s] Token is being blocked on this server%s.' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset()))

            elif 'Maximum number of guilds reached' in join_server:
                self.variables['completed'] += 1
                self.write('%s[%s%s%s] User already in 100 servers%s.' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset()))

            elif '"vanity_url_code"' in join_server:
                self.write('%s[%s%s%s] %sToken was successfully connected%s: %s' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), green(), reset(), server))
                self.variables['joined_tokens'].append(token)
                self.variables['joined'] += 1
                self.variables['completed'] += 1

            elif 'Access denied' in join_server:
                self.variables['retries'] += 1
                self.join(token, server, choice(self.variables['proxies']))

            else:
                self.variables['completed'] += 1
                self.write('%s[%s%s%s] Error %s| %s%s' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset(), blue(), join_server))
        except:
            self.variables['retries'] += 1
            self.join(token, server, choice(self.variables['proxies']))

    def spam(self, token, message, channel, proxy):
        headers = {'Authorization': token, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Accept': '*/*',}

        try:
            send_message = session.post('https://discordapp.com/api/v6/channels/%s/messages' % (channel), json={'content': message}, headers=headers, proxies={'https': 'http://%s' % (proxy)}, timeout=4).text

            if '"content":' in send_message:
                self.variables['sent'] += 1
                self.write('%s[%s%s%s] %sSent Message%s: %s' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), green(), reset(), message))

            elif 'You need to verify your account' in send_message:
                self.write('%s[%s%s%s] Your token is not authenticated%s.' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset()))

            elif 'Unauthorized' in send_message:
                self.write('%s[%s%s%s] Malfunctioning token%s.' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset()))

            elif 'You are being rate limited.' in send_message:
                pass

            elif 'Missing Access' in send_message:
                self.write('%s[%s%s%s] You have no rights%s.' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset()))

            elif 'Access denied' in send_message:
                self.variables['retries'] += 1
                self.spam(token, message, channel, choice(self.variables['proxies']))
                
            else:
                self.write('%s[%s%s%s] Error %s| %s%s' % (blue(), reset(), strftime('%H:%M:%S', gmtime()), blue(), reset(), blue(), send_message))
        except:
            self.variables['retries'] += 1
            self.spam(token, message, channel, choice(self.variables['proxies']))

if __name__ == '__main__':
    spammer = Main()
    spammer.start()
