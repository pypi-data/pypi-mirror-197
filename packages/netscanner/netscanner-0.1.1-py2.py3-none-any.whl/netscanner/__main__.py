"""
NetScanner - A comprehensive network reconnaissance tool

Copyright (C) Adam Dawood <add0242@my.londonmet.ac.uk>
"""

# Imports
import time
import os
import subprocess
import re
import os.path
import datetime
import timeit
import argparse
import sys

# Start timer
Start = timeit.default_timer()

# Install external utilities
subprocess.run(["sudo apt install nmap aircrack-ng net-tools wireless-tools ethtool"],
               shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Add flags + options
parser = argparse.ArgumentParser()
parser._action_groups.pop()
Modes = parser.add_argument_group('Modes')
Options = parser.add_argument_group('Options')
Modes.add_argument('-nP',
                   action='store_true',
                   help='This flag will execute Mode 2, NO PORT SCAN, which will '
                        'execute the Host Discovery and 802.11 WLAN Discovery '
                        'processes.')
Modes.add_argument('-w',
                   action='store_true',
                   help='This flag will execute Mode 3, WIRELESS ONLY, which will '
                        'execute the 802.11 WLAN Discovery process exclusively. ')
Modes.add_argument('-l',
                   action='store_true',
                   help='This flag will execute Mode 4, LOCAL SCAN ONLY, which will '
                        'execute the Host Discovery and Port Scan processes')
Modes.add_argument('-hD',
                   action='store_true',
                   help='This flag will execute Mode 5, HOST DISCOVERY ONLY, which '
                        'will execute the Host Discovery Process exclusively.')
Options.add_argument('--wP',
                     action='store',
                     dest='WLANScanPeriod',
                     default=60,
                     type=int,
                     metavar='<integer value in seconds>',
                     help='This option allows you to specify a scan period for the 802.11 WLAN Discovery process. '
                          'The default is 60. This value is ignored if the mode of operation is not Mode 1, '
                          '2 or 3. Large values will result in longer scan times but greater verbosity.')
Options.add_argument('--pP',
                     action='store',
                     dest='PortScanPeriod',
                     default=60,
                     type=int,
                     metavar='<integer value in seconds>',
                     help='This option allows you to specify a scan period for the Port Scan process. '
                          'The default is 60. This value is ignored if the mode of operation is not Mode 1 or 4. '
                          'Large values will result in longer scan times but greater verbosity.')
Options.add_argument('--pR',
                     action='store',
                     dest='PortRange',
                     default='-F',
                     type=str,
                     metavar='<first port-last port>',
                     help='This option allows you to specify a port range for the Port Scan process.'
                          'The default is the 100 most common ports determined by Nmap (-F). '
                          'Large values will result in longer scan times but greater verbosity. '
                          'It is useful to combine this option with the --pP option to avoid scan timeouts '
                          'when scanning large ranges.')
args = parser.parse_args()

# Add -p flag for custom port range
PortRange = ''
if args.PortRange != '-F':
    if bool(re.match('^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])[-]'
                     '([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$',
                     args.PortRange)):
        PortRange = str('-p ' + args.PortRange)
    else:
        print("\nError: '" + args.PortRange + "' is not a valid port range. \
        \n\nPlease follow the Port Range conventions: <first port-last port>. Example: 1-100.")
        sys.exit()
else:
    PortRange = '-F'

# Execute Mode 1
def MAIN():
# Print header
    print("\nStarting NETSCANNER at " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')))
    time.sleep(1)
    print("\nDo not kill the program during this process, it may disable your network connection.")

# Create temp directory
    username = os.getlogin()
    tempDir = '/home/' + username + '/Documents/NetScanner/Temp'
    os.chdir(".")
    if os.path.isdir(tempDir):
        pass
    else:
        os.makedirs(tempDir)

# Get most active interface
    # Disables loopback interface
    subprocess.run(["sudo -S ifconfig lo down"],
                   shell=True, stderr=subprocess.DEVNULL)

    # Run ifconfig
    ifconf = (subprocess.check_output('ifconfig', shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))

    # Run ifconfig to gather interface names
    ifaces = (subprocess.check_output(r"ifconfig | sed 's/[ \t].*//;/^$/d'",
                                      shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    Interfaces = []
    Received = []
    Transmit = []

    # Stores interface names into list
    for line in ifaces.splitlines():
        Interfaces.append(line)

    # Stores RX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("RX packets"):
            RX = line.strip().split(" ")[2]
            Received.append(int(RX))

    # Stores TX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("TX packets"):
            TX = line.strip().split(" ")[2]
            Transmit.append(int(TX))

    # Calculates index of most active interface
    getRXmax = max(Received)
    getTXmax = max(Transmit)
    maxRXindex = Received.index(getRXmax)
    maxTXindex = Transmit.index(getTXmax)
    if maxRXindex == maxTXindex:
        MAI = str(Interfaces[maxRXindex]).replace(':', '')
    else:
        print('Error: The most active interface cannot be determined.')
        sys.exit()

    # Re-enables loopback interface
    subprocess.run(["sudo -S ifconfig lo up"], shell=True, stderr=subprocess.DEVNULL)

# Get local interface info + append to list
    LANInfo = []

    # Get MAI MAC
    MAC = (subprocess.check_output(["ifconfig " + MAI + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    MAC = MAC.upper()
    LANInfo.append(MAC.strip())

    # Get MAI NIC Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    try:
        HostMAC = MacLookup().lookup(MAC.strip())
    except (InvalidMacError, VendorNotFoundError):
        HostMAC = "Unknown"

    # Get MAI IP
    IP = (subprocess.check_output(["ifconfig " + MAI + r" | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(IP.strip())

    # Get MAI subnet mask
    SubMask = (subprocess.check_output(["ifconfig " + MAI + " | grep -w inet | awk '{print $4}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(SubMask.strip())

    # Get data exchanged in MB
    RXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'RX packets' | awk '{printf $6}{print $7}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXMB = re.sub("[()]","", RXMB)
    LANInfo.append(RXMB.strip())
    TXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'TX packets' | awk '{printf $6}{print $7}'"],
                                shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TXMB = re.sub("[()]","", TXMB)
    LANInfo.append(TXMB.strip())

    # Calculate CIDR
    if SubMask == '128.0.0.0':
        CIDR = '/1'
        UsableHosts = '2,147,483,646'
    elif LANInfo[2] == '192.0.0.0':
        CIDR = '/2'
        UsableHosts = '1,073,741,822'
    elif LANInfo[2] == '224.0.0.0':
        CIDR = '/3'
        UsableHosts = '536,870,910'
    elif LANInfo[2] == '240.0.0.0':
        CIDR = '/4'
        UsableHosts = '268,435,454'
    elif LANInfo[2] == '248.0.0.0':
        CIDR = '/5'
        UsableHosts = '134,217,726'
    elif LANInfo[2] == '252.0.0.0':
        CIDR = '/6'
        UsableHosts = '67,108,862'
    elif LANInfo[2] == '254.0.0.0':
        CIDR = '/7'
        UsableHosts = '33,554,430'
    elif LANInfo[2] == '255.0.0.0':
        CIDR = '/8'
        UsableHosts = '16,777,214'
    elif LANInfo[2] == '255.128.0.0':
        CIDR = '/9'
        UsableHosts = '8,388,606'
    elif LANInfo[2] == '255.192.0.0':
        CIDR = '/10'
        UsableHosts = '4,194,302'
    elif LANInfo[2] == '255.224.0.0':
        CIDR = '/11'
        UsableHosts = '2,097,150'
    elif LANInfo[2] == '255.240.0.0':
        CIDR = '/12'
        UsableHosts = '1,048,574'
    elif LANInfo[2] == '255.248.0.0':
        CIDR = '/13'
        UsableHosts = '524,286'
    elif LANInfo[2] == '255.252.0.0':
        CIDR = '/14'
        UsableHosts = '262,142'
    elif LANInfo[2] == '255.254.0.0':
        CIDR = '/15'
        UsableHosts = '131,070'
    elif LANInfo[2] == '255.255.0.0':
        CIDR = '/16'
        UsableHosts = '65,534'
    elif LANInfo[2] == '255.255.128.0':
        CIDR = '/17'
        UsableHosts = '32,766'
    elif LANInfo[2] == '255.255.192.0':
        CIDR = '/18'
        UsableHosts = '16,382'
    elif LANInfo[2] == '255.255.224.0':
        CIDR = '/19'
        UsableHosts = '8,190'
    elif LANInfo[2] == '255.255.240.0':
        CIDR = '/20'
        UsableHosts = '4,094'
    elif LANInfo[2] == '255.255.248.0':
        CIDR = '/21'
        UsableHosts = '2,046'
    elif LANInfo[2] == '255.255.252.0':
        CIDR = '/22'
        UsableHosts = '1,022'
    elif LANInfo[2] == '255.255.254.0':
        CIDR = '/23'
        UsableHosts = '510'
    elif LANInfo[2] == '255.255.255.0':
        CIDR = '/24'
        UsableHosts = '254'
    elif LANInfo[2] == '255.255.255.128':
        CIDR = '/25'
        UsableHosts = '126'
    elif LANInfo[2] == '255.255.255.192':
        CIDR = '/26'
        UsableHosts = '62'
    elif LANInfo[2] == '255.255.255.224':
        CIDR = '/27'
        UsableHosts = '30'
    elif LANInfo[2] == '255.255.255.240':
        CIDR = '/28'
        UsableHosts = '14'
    elif LANInfo[2] == '255.255.255.248':
        CIDR = '/29'
        UsableHosts = '6'
    elif LANInfo[2] == '255.255.255.252':
        CIDR = '/30'
        UsableHosts = '2'
    elif LANInfo[2] == '255.255.255.254':
        CIDR = '/31'
        UsableHosts = '0'
    elif LANInfo[2] == '255.255.255.255':
        CIDR = '/32'
        UsableHosts = '0'
    else:
        print("\nError: This program requires a valid network connection to operate. Please check your settings and "
              "try again.")
        sys.exit()
    LANInfo.append(CIDR.strip())

# Calculate network address
    # Convert subnet mask to binary
    BinNetAddr = []
    BinMask = '.'.join([bin(int(x)+256)[3:] for x in SubMask.split('.')])

    # Convert device ip to binary
    BinIP = '.'.join([bin(int(x)+256)[3:] for x in IP.split('.')])

    # Calculate network address in binary
    for i in range(len(BinMask)):
        if BinMask[i] == BinIP[i]:
            BinNetAddr.append(BinMask[i])
        else:
            BinNetAddr.append('0')

    # Convert binary network address to decimal
    BinNetAddr = ''.join(BinNetAddr)
    BinNetAddr = BinNetAddr.replace('.', '')
    FirstOctet = BinNetAddr[:8]
    SecondOctet = BinNetAddr[8:16]
    ThirdOctet = BinNetAddr[16:24]
    FourthOctet = BinNetAddr[24:32]
    FirstOctet = int(FirstOctet, 2)
    SecondOctet = int(SecondOctet, 2)
    ThirdOctet = int(ThirdOctet, 2)
    FourthOctet = int(FourthOctet, 2)

    # Arrange into dotted format.
    NetAddr = []
    NetAddr.append(str(FirstOctet))
    NetAddr.append(str(SecondOctet))
    NetAddr.append(str(ThirdOctet))
    NetAddr.append(str(FourthOctet))
    NetAddr = '.'.join(NetAddr)

    # Append network address to list
    LANInfo.append(NetAddr.strip())

    # Get link speeds
    TXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'txrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'rxrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    if TXLinkSp != '':
        TXLinkSp = float(TXLinkSp) / 1000000
        TXLinkSp = int(TXLinkSp)
        LANInfo.append(TXLinkSp)
    else:
        TXLinkSp = 'Unknown '
        LANInfo.append(TXLinkSp)

    if RXLinkSp != '':
        RXLinkSp = float(RXLinkSp) / 1000000
        RXLinkSp = int(RXLinkSp)
        LANInfo.append(RXLinkSp)
    else:
        RXLinkSp = 'Unknown '
        LANInfo.append(RXLinkSp)

    # Get WLAN info
    try:
        iwconf = (subprocess.check_output(["iwconfig " + MAI],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        # Get 802.11 protocol
        IEEEProt = (subprocess.check_output(["iwconfig " + MAI + " | grep 'IEEE' | awk '{printf $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(IEEEProt.strip())

        # Get associated ESSID
        ESSID = (subprocess.check_output(["iwconfig " + MAI + r" | grep ESSID | awk -F: '{print $2}' | sed 's/\"//g'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(ESSID.strip())

        # Get associated AP BSSID
        APMAC = (subprocess.check_output(["iwconfig " + MAI + " | grep 'Access Point' | awk '{print $6}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(APMAC.strip())

        # Get associated AP vendor
        from mac_vendor_lookup import MacLookup
        from mac_vendor_lookup import InvalidMacError
        from mac_vendor_lookup import VendorNotFoundError
        try:
            HostAPVendor = MacLookup().lookup(APMAC.strip())
            LANInfo.append(HostAPVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            HostAPVendor = "Unknown"
            LANInfo.append(HostAPVendor.strip())

        # Get operating frequency
        Freq = (subprocess.check_output(["iwconfig " + MAI + " | grep -o 'Frequency:.*GHz' | sed -e 's/[^0-9.]//g'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(Freq.strip())

        # Get operating channel
        Channel = (subprocess.check_output(["iwlist " + MAI + " channel | grep 'Current Frequency' | awk '{printf $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(')', '')
        if Channel == '':
            Channel = "Channel not identified"
        else:
            pass
        LANInfo.append(Channel.strip())

        # Get link quality
        LinkQual = (subprocess.check_output(["iwconfig " + MAI + "| grep 'Signal level=' | awk '{print $4}' |  sed -e "
                                                                 "'s/level=//'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(LinkQual.strip())
        if int(LinkQual) <= -80:
            Strength = "Poor"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= -55:
            Strength = "Good"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= 0:
            Strength = "Excellent"
            LANInfo.append(str(Strength).strip())
    except subprocess.CalledProcessError:
        IEEEProt = "No wireless connection"
        LANInfo.append(IEEEProt.strip())
        ESSID = "N/A"
        LANInfo.append(ESSID.strip())
        APMAC = "N/A"
        LANInfo.append(APMAC.strip())
        APMACVendor = "N/A"
        LANInfo.append(APMACVendor.strip())
        Channel = "N/A"
        LANInfo.append(Channel.strip())
        Freq = "N/A "
        LANInfo.append(Freq.strip())
        LinkQual = "N/A "
        LANInfo.append(LinkQual.strip())
        Strength = " "
        LANInfo.append(Strength.strip())
    LANInfo.append(UsableHosts)
    LANInfo.append(HostMAC)

# Execute host discovery techniques
    # Execute Nmap ARP ping scan
    subprocess.run(["sudo -S nmap -PR -sn -T4 -n -oN /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Execute Nmap rDNS lookup scan
    subprocess.run(["sudo -S nmap -R -PR -sn -T5 -oN /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Retrieve required data from output
    # Retrieve total hosts
    ActiveIPs = []
    TotalUpHosts = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'Nmap done at' | awk '{print $14}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalUpHosts = TotalUpHosts.replace('(', '')
    TotalUpHosts = TotalUpHosts.replace('\n', ' ')

    # Retrieve host IP addresses from ARP Scan
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        IPAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        IPAddrs = IPAddrs.replace('\n', '')
        ActiveIPs.append(IPAddrs)

    # Retrieve hostnames from rDNS lookup
    ActiveHostnames = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Hostname = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt "
                                             + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Hostname = Hostname.strip()
        Hostname = Hostname.replace('\n', '')
        try:
            IsChar = Hostname[0]
        except IndexError:
            IsChar = '1'
        if IsChar.isdigit() == True:
            Hostname = 'Unknown Hostname'
            ActiveHostnames.append(Hostname)
        elif IsChar.isdigit() == False:
            ActiveHostnames.append(Hostname)

    # Retrieve ARP reply latency from ARP Scan
    ResLatency = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Latency = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Host is up' | awk 'NR==" + str(i) + "{print $4}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Latency = Latency.replace('(', '')
        Latency = Latency.replace('\n', '')
        ResLatency.append(Latency)

    # Retrieve host MAC address from ARP Scan
    ActiveMACAddr = []
    MACVendors = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        MACAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'MAC Address: ' | awk 'NR==" + str(i) + "{print $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        MACAddrs = MACAddrs.replace('(', '')
        MACAddrs = MACAddrs.replace('\n', '')
        if MACAddrs == '':
            MACAddrs = 'Unknown'
            ActiveMACAddr.append(MACAddrs)
        else:
            ActiveMACAddr.append(MACAddrs)

    # Determine host NIC vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    Range = int(TotalUpHosts)
    for i in range(0, Range):
        try:
            MACVendor = MacLookup().lookup(ActiveMACAddr[i].strip())
            MACVendors.append(MACVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            MACVendor = "Unknown"
            MACVendors.append(MACVendor.strip())

# Execute port scans
    # Execute Nmap TCP Half Open and UDP port scan on all hosts
    # This can be resource intensive
    Range = int(TotalUpHosts) - 1
    PortScanCmds = []
    for i in range(0, Range, 9):
        try:
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i]
                                + ".txt " + ActiveIPs[i] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+1]
                                + ".txt " + ActiveIPs[i+1] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+2]
                                + ".txt " + ActiveIPs[i+2] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+3]
                                + ".txt " + ActiveIPs[i+3] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+4]
                                + ".txt " + ActiveIPs[i+4] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+5]
                                + ".txt " + ActiveIPs[i+5] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+6]
                                + ".txt " + ActiveIPs[i+6] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+7]
                                + ".txt " + ActiveIPs[i+7] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+8]
                                + ".txt " + ActiveIPs[i+8] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+9]
                                + ".txt " + ActiveIPs[i+9] + "/32")
        except IndexError:
            pass
    from subprocess import Popen
    processes = [Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) for cmd in PortScanCmds]
    time.sleep(args.PortScanPeriod)

    # Execute airodump-ng capture
    subprocess.run(["sudo -S airmon-ng start " + MAI],
                   shell=True, stdout=subprocess.DEVNULL)
    airodump = subprocess.Popen(["sudo -S airodump-ng " + MAI + "mon --band abg -w /home/" + username
                                 + "/Documents/NetScanner/Temp/airodump-ng --output-format csv"],
                                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(args.WLANScanPeriod)
    subprocess.run(["sudo kill -9 " + str(airodump.pid)], shell=True)
    subprocess.run(["sudo -S airmon-ng stop " + MAI + "mon"], shell=True, stdout=subprocess.DEVNULL)

    # Retrieve AP information from airodump-ng scan
    TotalAPs = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| wc -l"], shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalAPs = int(TotalAPs)

    # Get ESSIDs
    ESSIDs = []
    for i in range(1, TotalAPs):
        ESSID = (subprocess.check_output(["cat /home/" + username +
                                          "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                          "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                          "| awk '(NR==" + str(i) + "){print $18,$19}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        ESSID = ESSID.replace(',', '')
        ESSID = ESSID.replace('\n', '')
        ESSID = ESSID.replace('\r', '')
        IsESSID = any(str.isdigit(i) for i in ESSID)
        if IsESSID == True:
            ESSID = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                              "| awk '(NR==" + str(i) + "){print $19,$20}'"],
                                             shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
            ESSID = ESSID.replace(',', '')
            ESSID = ESSID.replace('\n', '')
            ESSID = ESSID.replace('\r', '')
            if ESSID == ' ':
                ESSIDs.append('Hidden')
            else:
                ESSID = ESSID.rstrip()
                ESSIDs.append(ESSID)
        else:
            if ESSID == ' ':
                ESSIDs.append('Hidden')
            else:
                ESSID = ESSID.rstrip()
                ESSIDs.append(ESSID)

    # Get BSSIDs and AP Vendors
    BSSIDs = []
    APVendors = []
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    for i in range(1, TotalAPs):
        BSSID = (subprocess.check_output(["cat /home/" + username +
                                          "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                          "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                          "| awk '(NR==" + str(i) + "){print $1}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        BSSID = BSSID.replace(',', '')
        BSSID = BSSID.replace('\n', '')
        BSSID = BSSID.replace('\r', '')
        BSSIDs.append(BSSID)
        try:
            APVendor = MacLookup().lookup(BSSID)
            APVendors.append(APVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            APVendor = "Unknown"
            APVendors.append(APVendor.strip())

    # Get AP channels
    Channels = []
    for i in range(1, TotalAPs):
        Channel = (subprocess.check_output(["cat /home/" + username +
                                            "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                            "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                            "| awk '(NR==" + str(i) + "){print $6}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(',', '')
        Channel = Channel.replace('\n', '')
        Channel = Channel.replace('\r', '')
        Channels.append(Channel)

    # Get throughput rates
    Throughputs = []
    for i in range(1, TotalAPs):
        Throughput = (subprocess.check_output(["cat /home/" + username +
                                               "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                               "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                               "| awk '(NR==" + str(i) + "){print $7}'"],
                                              shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Throughput = Throughput.replace(',', '')
        Throughput = Throughput.replace('\n', '')
        Throughput = Throughput.replace('\r', '')
        if Throughput == '-1':
            Throughput = ' ?'
            Throughputs.append(Throughput)
        else:
            Throughputs.append(Throughput)

    # Get RSSIs
    RSSIs = []
    for i in range(1, TotalAPs):
        RSSI = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $11}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        RSSI = RSSI.replace(',', '')
        RSSI = RSSI.replace('\n', '')
        RSSI = RSSI.replace('\r', '')
        if RSSI == '-1':
            RSSI = ' ?'
            RSSIs.append(RSSI)
        else:
            RSSIs.append(RSSI)

    # Get Encryption Protocol
    ENCs = []
    for i in range(1, TotalAPs):
        EncP = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $8}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        EncP = EncP.replace(',', '')
        EncP = EncP.replace('\n', '')
        EncP = EncP.replace('\r', '')
        ENCs.append(EncP)

    # Get Ciphers
    Ciphers = []
    for i in range(1, TotalAPs):
        Cipher = (subprocess.check_output(["cat /home/" + username +
                                           "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                           "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                           "| awk '(NR==" + str(i) + "){print $9}'"],
                                          shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Cipher = Cipher.replace(',', '')
        Cipher = Cipher.replace('\n', '')
        Cipher = Cipher.replace('\r', '')
        if Cipher == '':
            Cipher = 'NONE'
            Ciphers.append(Cipher)
        else:
            Ciphers.append(Cipher)

    # Get Authentication Method
    AuthMthds = []
    for i in range(1, TotalAPs):
        Auth = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $10}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Auth = Auth.replace(',', '')
        Auth = Auth.replace('\n', '')
        Auth = Auth.replace('\r', '')
        if Auth == '':
            Auth = 'NONE'
            AuthMthds.append(Auth)
        else:
            AuthMthds.append(Auth)

    # Group APs into lists, add lists to dictionary of detected APs
    APs = {}
    APRange = TotalAPs - 1
    for i in range(0, APRange):
        x = ("AP-" + str(i))
        APs[x] = [ESSIDs[i], BSSIDs[i], APVendors[i], Channels[i], Throughputs[i], RSSIs[i], ENCs[i], Ciphers[i], AuthMthds[i]]

    # Group APs into lists by ESSID
    WLANs = {}
    z = 0
    for i in range(0, APRange):
        x = (APs["AP-" + str(i)][0])
        WLANs[x] = []
        for y in range(0, APRange):
            if (APs["AP-" + str(i)][0]) == (APs["AP-" + str(z)][0]):
                WLANs[x] += ((APs["AP-" + str(z)][1]), )
                WLANs[x] += ((APs["AP-" + str(z)][2]), )
                WLANs[x] += ((APs["AP-" + str(z)][3]), )
                WLANs[x] += ((APs["AP-" + str(z)][4]), )
                WLANs[x] += ((APs["AP-" + str(z)][5]), )
                WLANs[x] += ((APs["AP-" + str(z)][6]), )
                WLANs[x] += ((APs["AP-" + str(z)][7]), )
                WLANs[x] += ((APs["AP-" + str(z)][8]), )
            else:
                pass
            z = z + 1
            if z >= APRange:
                z = 0
            else:
                pass

    # Group channels used by ESSID
    ChannelsDict = {}
    for key in WLANs:
        x = key
        ChannelsDict[x] = []
        for i in range(2, (8 * (int(len(WLANs[key])) // 8)), 8):
            try:
                if (WLANs[key][i]) not in ChannelsDict[x]:
                    ChannelsDict[x].append(WLANs[key][i])
                else:
                    pass
            except IndexError:
                pass

    # Retreive Station information from airodump-ng scan
    TotalStations = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                              "| wc -l"], shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalStations = int(TotalStations)

    # Get Station MAC and Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    StationMACs = []
    StationVendors = []
    for i in range(1, TotalStations):
        StationMAC = (subprocess.check_output(["cat /home/" + username +
                                               "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                               "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                               "| awk '(NR==" + str(i) + "){print $1}'"],
                                              shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationMAC = StationMAC.replace(',', '')
        StationMAC = StationMAC.replace('\n', '')
        StationMAC = StationMAC.replace('\r', '')
        if StationMAC == '':
            pass
        else:
            StationMACs.append(StationMAC)
        try:
            StationVendor = MacLookup().lookup(StationMAC)
            StationVendors.append(StationVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            StationVendor = " ?"
            StationVendors.append(StationVendor.strip())

    # Get Station RSSI rates
    StationRSSIs = []
    for i in range(1, TotalStations):
        StationRSSI = (subprocess.check_output(["cat /home/" + username +
                                                "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                                "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                                "| awk '(NR==" + str(i) + "){print $6}'"],
                                               shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationRSSI = StationRSSI.replace(',', '')
        StationRSSI = StationRSSI.replace('\n', '')
        StationRSSI = StationRSSI.replace('\r', '')
        if StationRSSI == '-1':
            StationRSSI = ' ?'
            StationRSSIs.append(StationRSSI.strip())
        else:
            StationRSSIs.append(StationRSSI)
            StationRSSIs.append(StationRSSI.strip())

    # Get Station Associated AP BSSID
    StationAPs = []
    for i in range(1, TotalStations):
        StationAP = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                              "| awk '(NR==" + str(i) + "){print $8}'"],
                                             shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationAP = StationAP.replace(',', '')
        StationAP = StationAP.replace('\n', '')
        StationAP = StationAP.replace('\r', '')
        if StationAP == '(not':
            StationAP = '(not associated)'
            StationAPs.append(StationAP.strip())
        else:
            StationAPs.append(StationAP.strip())

    # Group Stations into lists, add lists to dictionary of detected stations
    Stations = {}
    StationRange = TotalStations - 1
    for i in range(0, StationRange):
        x = ("Station-" + str(i))
        Stations[x] = [StationMACs[i], StationVendors[i], StationRSSIs[i], StationAPs[i]]

    # Group Stations into lists by associated BSSID
    AssociatedStations = {}
    UnassociatedStations = []
    z = 0
    for key in WLANs:
        AssociatedStations[key] = []
    for i in range(0, StationRange):
        for y in range(0, APRange):
            if (Stations["Station-" + str(i)][3]) == '(not associated)':
                UnassociatedStations.append((Stations["Station-" + str(i)][0]))
                UnassociatedStations.append((Stations["Station-" + str(i)][1]))
                UnassociatedStations.append((Stations["Station-" + str(i)][2]))
                break
            elif (Stations["Station-" + str(i)][3]) == (APs["AP-" + str(y)][1]):
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][0]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][1]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][2]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][3]),)
            else:
                pass

# Output data
    End = timeit.default_timer()
    TimeTaken = End - Start

    # Create output file
    filepath = "/home/" + username + "/Documents/NetScanner/"
    filename = filepath + str(datetime.datetime.now().astimezone().strftime('%d-%m-%Y_%H%M%S')) + '_Mode1.txt'
    sys.stdout = open(filename, 'w')

    # Print local interface details
    print(f"\
    \nNETSCANNER has completed on " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')) + "\
    \n \
    \n=============================================== \
    \nDetected Local Host Network Characteristics \
    \n=============================================== \
    \nMost Active Interface: " + MAI + " \
    \nInterface MAC Address: " + str(LANInfo[0]) + " (" + str(LANInfo[18]) + ")\
    \nInterface IPv4 Address: " + str(LANInfo[1]) + " \
    \nNetwork: " + str(LANInfo[6]) + str(LANInfo[5]) + " \
    \nData Exchanged: Transmit: " + str(LANInfo[4]) + ", Received: " + str(LANInfo[3]) + " \
    \nLink Speed: Transmit: " + str(LANInfo[7]) + "Mbps, Receive: " + str(LANInfo[8]) + "Mbps \
    \nActive 802.11 Protocol: " + str(LANInfo[9]) + "\
    \nConnected ESSID: " + str(LANInfo[10]) + " \
    \nAssociated Access Point BSSID: " + str(LANInfo[11]) + " (" + str(LANInfo[12]) + ") \
    \nAccess Point Channel: " + str(LANInfo[14]))
    if (str(LANInfo[13])) == 'N/A':
        print("Operating Frequency: " + str(LANInfo[13]))
    else:
        print("Operating Frequency: " + str(LANInfo[13]) + "Ghz")
    if (str(LANInfo[15])) == 'N/A':
        print("Link Quality: " + str(LANInfo[15]))
    else:
        print("Link Quality: " + str(LANInfo[15]) + "dBm, " + str(LANInfo[16]))
    print("===============================================")

    # Print host details + port states
    print("\n=============================================== \
    \nDiscovered Local Hosts: " + TotalUpHosts + " \
    \n===============================================")
    Range = int(TotalUpHosts)
    for i in range(Range):
        if ResLatency[i] == '':
            ResLatency[i] = 'Undetermined'
        else:
            pass
        print("Host " + ActiveIPs[i] + " (" + ActiveHostnames[i] + ") is up (" + ResLatency[i] + " latency)")
        print("MAC Address: " + ActiveMACAddr[i] + " (" + MACVendors[i] + ")")

        # Retrieve not shown ports or ignored state lines
        try:
            NotShown = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | grep 'Not shown: '"],
                                            shell=True).decode('utf-8'))
            NotShown = NotShown.replace('\n', '')
            print(NotShown)
        except subprocess.CalledProcessError:
            pass
        try:
            IsAllIgnored = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | grep 'All'"],
                                                    shell=True).decode('utf-8'))
            print("All scanned ports are in the ignored state \
            \n-----------------------------------------------")
        except subprocess.CalledProcessError:

            # Retrieve and print port statuses
            with open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt", "r") as f:
                output = f.read()
                if 'Not shown' in output:
                    NumOfPorts = sum(1 for l in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + str(ActiveIPs[i]) + ".txt")) - 1
                    if 'MAC' in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt").read():
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/Not shown:/{flag=1;next}/MAC/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                    else:
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/Not shown:/{flag=1;next}/Nmap/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                elif 'PORT' in output:
                    NumOfPorts = sum(1 for l in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + str(ActiveIPs[i]) + ".txt")) - 1
                    if 'MAC' in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt").read():
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/PORT/{flag=1;next}/MAC/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                    else:
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/PORT/{flag=1;next}/Nmap/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                else:
                    print('Port scan timeout', end="")
                    print("\n-----------------------------------------------")
    print(TotalUpHosts + "responsive hosts out of " + LANInfo[17] + " usable hosts ")
    print("-----------------------------------------------")

    # Print nearby 802.11 WLAN details
    # Print ESSID, ENC type and number of detected APs
    print("\n===============================================")
    TotalWLANs = len(WLANs)
    if 'Hidden' in WLANs:
        print("Discovered Wireless Networks (" + str((int(TotalWLANs)) - 1) + ")")
    else:
        print("Discovered Wireless Networks (" + str(TotalWLANs) + ")")
    print("===============================================")
    for key in WLANs:
        if key != 'Hidden':
            print("ESSID: " + key)
            print("----------------------------------------------- \
            \nDetected Encryption Protocol: " + WLANs[key][5] + "\
            \n----------------------------------------------- \
            \nDetected Channels in use: " + (', '.join('%s'%item for item in ChannelsDict[key])) + " \
            \n----------------------------------------------- \
            \nDiscovered Associated Access Points (" + str(int(len(WLANs[key])) // 8) + ") \
            \n----------------------------------------------- \
            \nBSSID              SIGNAL CH   RATE ENC   CIPHER AUTH  VENDOR")
            # Print list of associated APs
            for i in range(0, (8 * (int(len(WLANs[key])) // 8)), 8):
                print('{0:<19}'.format(WLANs[key][i]), end='')
                print('{0:<7}'.format(WLANs[key][i + 4]), end='')
                print('{0:<5}'.format(WLANs[key][i + 2]), end='')
                print('{0:<5}'.format(WLANs[key][i + 3]), end='')
                print('{0:<6}'.format(WLANs[key][i + 5]), end='')
                print('{0:<7}'.format(WLANs[key][i + 6]), end='')
                print('{0:<6}'.format(WLANs[key][i + 7]), end='')
                print('{0:<40}'.format(WLANs[key][i + 1]), end='')
                print()
            # Print list of associated stations
            print("----------------------------------------------- \
            \nDiscovered Associated Stations (" + str(int(len(AssociatedStations[key])) // 6) + ") \
            \n----------------------------------------------- \
            \nSTATION            ASSOCIATED-BSSID   SIGNAL  VENDOR ")
            if not AssociatedStations[key]:
                pass
            else:
                for i in range(0, (4 * (int(len(AssociatedStations[key])) // 4)), 4):
                    print('{0:<19}'.format(AssociatedStations[key][i]), end='')
                    print('{0:<19}'.format(AssociatedStations[key][i + 3]), end='')
                    print('{0:<8}'.format(AssociatedStations[key][i + 2]), end='')
                    print('{0:<40}'.format(AssociatedStations[key][i + 1]), end='')
                    print()
            print("=============================================== ")
        else:
            pass

    # Print list of hidden APs
    if 'Hidden' in WLANs:
        print("\n============================================== \
        \nDiscovered Hidden Access Points (" + str(int(len(WLANs['Hidden'])) // 8) + ") \
        \n============================================== \
        \nBSSID              SIGNAL CH   RATE ENC   CIPHER AUTH  VENDOR")
        for i in range(0, (8 * (int(len(WLANs['Hidden'])) // 8)), 8):
            print('{0:<19}'.format(WLANs['Hidden'][i]), end='')
            print('{0:<7}'.format(WLANs['Hidden'][i + 4]), end='')
            print('{0:<5}'.format(WLANs['Hidden'][i + 2]), end='')
            print('{0:<5}'.format(WLANs['Hidden'][i + 3]), end='')
            print('{0:<6}'.format(WLANs['Hidden'][i + 5]), end='')
            print('{0:<7}'.format(WLANs['Hidden'][i + 6]), end='')
            print('{0:<6}'.format(WLANs['Hidden'][i + 7]), end='')
            print('{0:<40}'.format(WLANs['Hidden'][i + 1]), end='')
            print()
        # Print list of associated stations
        print("----------------------------------------------- \
        \nDiscovered Associated Stations (" + str(int(len(AssociatedStations['Hidden'])) // 4) + ") \
        \n----------------------------------------------- \
        \nSTATION            ASSOCIATED-BSSID   SIGNAL  VENDOR ")
        if not AssociatedStations['Hidden']:
            pass
        else:
            for i in range(0, (4 * (int(len(AssociatedStations['Hidden'])) // 4)), 4):
                print('{0:<19}'.format(AssociatedStations['Hidden'][i]), end='')
                print('{0:<19}'.format(AssociatedStations['Hidden'][i + 3]), end='')
                print('{0:<8}'.format(AssociatedStations['Hidden'][i + 2]), end='')
                print('{0:<40}'.format(AssociatedStations['Hidden'][i + 1]), end='')
                print()
    else:
        pass

    # Print list of unassociated stations
    print("\n============================================== \
    \nDiscovered Unassociated Stations (" + str(int(len(UnassociatedStations)) // 3) + ") \
    \n============================================== \
    \nSTATION            SIGNAL   VENDOR ")
    for i in range(0, (3 * (int(len(UnassociatedStations)) // 3)), 3):
        print('{0:<19}'.format(UnassociatedStations[i]), end='')
        print('{0:<9}'.format(UnassociatedStations[i + 2]), end='')
        print('{0:<40}'.format(UnassociatedStations[i + 1]), end='')
        print()
    print("----------------------------------------------")

    # Print footer
    print("\n---------------------------------------------- \
    \nScan Complete - An export of this scan has been saved as " + filename + ". \
    \nTotal Scan Time: " + str(round(TimeTaken, 2)) + " Seconds \
    \n-----------------------------------------------")

    sys.stdout = sys.__stdout__

    output = (subprocess.check_output("cat " + filename,
                                      shell=True).decode('utf-8'))
    print(output)

    # Remove temp directory
    subprocess.run(["sudo rm -r /home/" + username + "/Documents/NetScanner/Temp"],
                   shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Execute Mode 2 (-nP)
def NOPORTSCAN():
# Print header
    print("\nStarting NETSCANNER at " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')))
    time.sleep(1)
    print("\nDo not kill the program during this process, it may disable your network connection.")

# Create temp directory
    username = os.getlogin()
    tempDir = '/home/' + username + '/Documents/NetScanner/Temp'
    os.chdir(".")
    if os.path.isdir(tempDir):
        pass
    else:
        os.makedirs(tempDir)

# Get most active interface
    # Disables loopback interface
    subprocess.run(["sudo -S ifconfig lo down"],
                   shell=True, stderr=subprocess.DEVNULL)

    # Run ifconfig
    ifconf = (subprocess.check_output('ifconfig', shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))

    # Run ifconfig to gather interface names
    ifaces = (subprocess.check_output(r"ifconfig | sed 's/[ \t].*//;/^$/d'",
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    Interfaces = []
    Received = []
    Transmit = []

    # Stores interface names into list
    for line in ifaces.splitlines():
        Interfaces.append(line)

    # Stores RX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("RX packets"):
            RX = line.strip().split(" ")[2]
            Received.append(int(RX))

    # Stores TX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("TX packets"):
            TX = line.strip().split(" ")[2]
            Transmit.append(int(TX))

    # Calculates index of most active interface
    getRXmax = max(Received)
    getTXmax = max(Transmit)
    maxRXindex = Received.index(getRXmax)
    maxTXindex = Transmit.index(getTXmax)
    if maxRXindex == maxTXindex:
        MAI = str(Interfaces[maxRXindex]).replace(':', '')
    else:
        print('Error: The most active interface cannot be determined.')
        sys.exit()

    # Re-enables loopback interface
    subprocess.run(["sudo -S ifconfig lo up"], shell=True, stderr=subprocess.DEVNULL)

# Get local interface info + append to list
    LANInfo = []

    # Get MAI MAC
    MAC = (subprocess.check_output(["ifconfig " + MAI + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    MAC = MAC.upper()
    LANInfo.append(MAC.strip())

    # Get MAI NIC Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError

    try:
        HostMAC = MacLookup().lookup(MAC.strip())
    except (InvalidMacError, VendorNotFoundError):
        HostMAC = "Unknown"

    # Get MAI IP
    IP = (subprocess.check_output(["ifconfig " + MAI + r" | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(IP.strip())

    # Get MAI subnet mask
    SubMask = (subprocess.check_output(["ifconfig " + MAI + " | grep -w inet | awk '{print $4}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(SubMask.strip())

    # Get data exchanged in MB
    RXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'RX packets' | awk '{printf $6}{print $7}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXMB = re.sub("[()]","", RXMB)
    LANInfo.append(RXMB.strip())
    TXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'TX packets' | awk '{printf $6}{print $7}'"],
                                shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TXMB = re.sub("[()]","", TXMB)
    LANInfo.append(TXMB.strip())

    # Calculate CIDR
    if SubMask == '128.0.0.0':
        CIDR = '/1'
        UsableHosts = '2,147,483,646'
    elif LANInfo[2] == '192.0.0.0':
        CIDR = '/2'
        UsableHosts = '1,073,741,822'
    elif LANInfo[2] == '224.0.0.0':
        CIDR = '/3'
        UsableHosts = '536,870,910'
    elif LANInfo[2] == '240.0.0.0':
        CIDR = '/4'
        UsableHosts = '268,435,454'
    elif LANInfo[2] == '248.0.0.0':
        CIDR = '/5'
        UsableHosts = '134,217,726'
    elif LANInfo[2] == '252.0.0.0':
        CIDR = '/6'
        UsableHosts = '67,108,862'
    elif LANInfo[2] == '254.0.0.0':
        CIDR = '/7'
        UsableHosts = '33,554,430'
    elif LANInfo[2] == '255.0.0.0':
        CIDR = '/8'
        UsableHosts = '16,777,214'
    elif LANInfo[2] == '255.128.0.0':
        CIDR = '/9'
        UsableHosts = '8,388,606'
    elif LANInfo[2] == '255.192.0.0':
        CIDR = '/10'
        UsableHosts = '4,194,302'
    elif LANInfo[2] == '255.224.0.0':
        CIDR = '/11'
        UsableHosts = '2,097,150'
    elif LANInfo[2] == '255.240.0.0':
        CIDR = '/12'
        UsableHosts = '1,048,574'
    elif LANInfo[2] == '255.248.0.0':
        CIDR = '/13'
        UsableHosts = '524,286'
    elif LANInfo[2] == '255.252.0.0':
        CIDR = '/14'
        UsableHosts = '262,142'
    elif LANInfo[2] == '255.254.0.0':
        CIDR = '/15'
        UsableHosts = '131,070'
    elif LANInfo[2] == '255.255.0.0':
        CIDR = '/16'
        UsableHosts = '65,534'
    elif LANInfo[2] == '255.255.128.0':
        CIDR = '/17'
        UsableHosts = '32,766'
    elif LANInfo[2] == '255.255.192.0':
        CIDR = '/18'
        UsableHosts = '16,382'
    elif LANInfo[2] == '255.255.224.0':
        CIDR = '/19'
        UsableHosts = '8,190'
    elif LANInfo[2] == '255.255.240.0':
        CIDR = '/20'
        UsableHosts = '4,094'
    elif LANInfo[2] == '255.255.248.0':
        CIDR = '/21'
        UsableHosts = '2,046'
    elif LANInfo[2] == '255.255.252.0':
        CIDR = '/22'
        UsableHosts = '1,022'
    elif LANInfo[2] == '255.255.254.0':
        CIDR = '/23'
        UsableHosts = '510'
    elif LANInfo[2] == '255.255.255.0':
        CIDR = '/24'
        UsableHosts = '254'
    elif LANInfo[2] == '255.255.255.128':
        CIDR = '/25'
        UsableHosts = '126'
    elif LANInfo[2] == '255.255.255.192':
        CIDR = '/26'
        UsableHosts = '62'
    elif LANInfo[2] == '255.255.255.224':
        CIDR = '/27'
        UsableHosts = '30'
    elif LANInfo[2] == '255.255.255.240':
        CIDR = '/28'
        UsableHosts = '14'
    elif LANInfo[2] == '255.255.255.248':
        CIDR = '/29'
        UsableHosts = '6'
    elif LANInfo[2] == '255.255.255.252':
        CIDR = '/30'
        UsableHosts = '2'
    elif LANInfo[2] == '255.255.255.254':
        CIDR = '/31'
        UsableHosts = '0'
    elif LANInfo[2] == '255.255.255.255':
        CIDR = '/32'
        UsableHosts = '0'
    else:
        print("\nError: This program requires a valid network connection to operate. Please check your settings and "   
              "try again.")
        sys.exit()
    LANInfo.append(CIDR.strip())

# Calculate network address
    # Convert subnet mask to binary
    BinNetAddr = []
    BinMask = '.'.join([bin(int(x)+256)[3:] for x in SubMask.split('.')])

    # Convert device ip to binary
    BinIP = '.'.join([bin(int(x)+256)[3:] for x in IP.split('.')])

    # Calculate network address in binary
    for i in range(len(BinMask)):
        if BinMask[i] == BinIP[i]:
            BinNetAddr.append(BinMask[i])
        else:
            BinNetAddr.append('0')

    # Convert binary network address to decimal
    BinNetAddr = ''.join(BinNetAddr)
    BinNetAddr = BinNetAddr.replace('.', '')
    FirstOctet = BinNetAddr[:8]
    SecondOctet = BinNetAddr[8:16]
    ThirdOctet = BinNetAddr[16:24]
    FourthOctet = BinNetAddr[24:32]
    FirstOctet = int(FirstOctet, 2)
    SecondOctet = int(SecondOctet, 2)
    ThirdOctet = int(ThirdOctet, 2)
    FourthOctet = int(FourthOctet, 2)

    # Arrange into dotted format.
    NetAddr = []
    NetAddr.append(str(FirstOctet))
    NetAddr.append(str(SecondOctet))
    NetAddr.append(str(ThirdOctet))
    NetAddr.append(str(FourthOctet))
    NetAddr = '.'.join(NetAddr)

    # Append network address to list
    LANInfo.append(NetAddr.strip())

    # Get link speeds
    TXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'txrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'rxrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    if TXLinkSp != '':
        TXLinkSp = float(TXLinkSp) / 1000000
        TXLinkSp = int(TXLinkSp)
        LANInfo.append(TXLinkSp)
    else:
        TXLinkSp = 'Unknown '
        LANInfo.append(TXLinkSp)

    if RXLinkSp != '':
        RXLinkSp = float(RXLinkSp) / 1000000
        RXLinkSp = int(RXLinkSp)
        LANInfo.append(RXLinkSp)
    else:
        RXLinkSp = 'Unknown '
        LANInfo.append(RXLinkSp)

    # Get WLAN info
    try:
        iwconf = (subprocess.check_output(["iwconfig " + MAI],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        # Get 802.11 protocol
        IEEEProt = (subprocess.check_output(["iwconfig " + MAI + " | grep 'IEEE' | awk '{printf $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(IEEEProt.strip())

        # Get associated ESSID
        ESSID = (subprocess.check_output(["iwconfig " + MAI + r" | grep ESSID | awk -F: '{print $2}' | sed 's/\"//g'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(ESSID.strip())

        # Get associated AP BSSID
        APMAC = (subprocess.check_output(["iwconfig " + MAI + " | grep 'Access Point' | awk '{print $6}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(APMAC.strip())

        # Get associated AP vendor
        from mac_vendor_lookup import MacLookup
        from mac_vendor_lookup import InvalidMacError
        from mac_vendor_lookup import VendorNotFoundError
        try:
            HostAPVendor = MacLookup().lookup(APMAC.strip())
            LANInfo.append(HostAPVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            HostAPVendor = "Unknown"
            LANInfo.append(HostAPVendor.strip())

        # Get operating frequency
        Freq = (subprocess.check_output(["iwconfig " + MAI + " | grep -o 'Frequency:.*GHz' | sed -e 's/[^0-9.]//g'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(Freq.strip())

        # Get operating channel
        Channel = (subprocess.check_output(["iwlist " + MAI + " channel | grep 'Current Frequency' | awk '{printf $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(')', '')
        if Channel == '':
            Channel = "Channel not identified"
        else:
            pass
        LANInfo.append(Channel.strip())

        # Get link quality
        LinkQual = (subprocess.check_output(["iwconfig " + MAI + "| grep 'Signal level=' | awk '{print $4}' |  sed -e " 
                                                                 "'s/level=//'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(LinkQual.strip())
        if int(LinkQual) <= -80:
            Strength = "Poor"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= -55:
            Strength = "Good"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= 0:
            Strength = "Excellent"
            LANInfo.append(str(Strength).strip())
    except subprocess.CalledProcessError:
        IEEEProt = "No wireless connection"
        LANInfo.append(IEEEProt.strip())
        ESSID = "N/A"
        LANInfo.append(ESSID.strip())
        APMAC = "N/A"
        LANInfo.append(APMAC.strip())
        APMACVendor = "N/A"
        LANInfo.append(APMACVendor.strip())
        Channel = "N/A"
        LANInfo.append(Channel.strip())
        Freq = "N/A "
        LANInfo.append(Freq.strip())
        LinkQual = "N/A "
        LANInfo.append(LinkQual.strip())
        Strength = " "
        LANInfo.append(Strength.strip())
    LANInfo.append(UsableHosts)
    LANInfo.append(HostMAC)

# Execute host discovery techniques
    # Execute Nmap ARP ping scan
    subprocess.run(["sudo -S nmap -PR -sn -T4 -n -oN /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Execute Nmap rDNS lookup scan
    subprocess.run(["sudo -S nmap -R -PR -sn -T5 -oN /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Retrieve required data from output
    # Retrieve total hosts
    ActiveIPs = []
    TotalUpHosts = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'Nmap done at' | awk '{print $14}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalUpHosts = TotalUpHosts.replace('(', '')
    TotalUpHosts = TotalUpHosts.replace('\n', ' ')

    # Retrieve host IP addresses from ARP Scan
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        IPAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        IPAddrs = IPAddrs.replace('\n', '')
        ActiveIPs.append(IPAddrs)

    # Retrieve hostnames from rDNS lookup
    ActiveHostnames = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Hostname = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt "
                                             + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Hostname = Hostname.strip()
        Hostname = Hostname.replace('\n', '')
        try:
            IsChar = Hostname[0]
        except IndexError:
            IsChar = '1'
        if IsChar.isdigit() == True:
            Hostname = 'Unknown Hostname'
            ActiveHostnames.append(Hostname)
        elif IsChar.isdigit() == False:
            ActiveHostnames.append(Hostname)

    # Retrieve ARP reply latency from ARP Scan
    ResLatency = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Latency = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Host is up' | awk 'NR==" + str(i) + "{print $4}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Latency = Latency.replace('(', '')
        Latency = Latency.replace('\n', '')
        ResLatency.append(Latency)

    # Retrieve host MAC address from ARP Scan
    ActiveMACAddr = []
    MACVendors = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        MACAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'MAC Address: ' | awk 'NR==" + str(i) + "{print $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        MACAddrs = MACAddrs.replace('(', '')
        MACAddrs = MACAddrs.replace('\n', '')
        if MACAddrs == '':
            MACAddrs = 'Unknown'
            ActiveMACAddr.append(MACAddrs)
        else:
            ActiveMACAddr.append(MACAddrs)

    # Determine host NIC vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    Range = int(TotalUpHosts)
    for i in range(0, Range):
        try:
            MACVendor = MacLookup().lookup(ActiveMACAddr[i].strip())
            MACVendors.append(MACVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            MACVendor = "Unknown"
            MACVendors.append(MACVendor.strip())

    # Execute airodump-ng capture
    subprocess.run(["sudo -S airmon-ng start " + MAI], shell=True, stdout=subprocess.DEVNULL)
    airodump = subprocess.Popen(["sudo -S airodump-ng " + MAI + "mon --band abg -w /home/" + username
                                 + "/Documents/NetScanner/Temp/airodump-ng --output-format csv"],
                                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(args.WLANScanPeriod)
    subprocess.run(["sudo kill -9 " + str(airodump.pid)], shell=True)
    subprocess.run(["sudo -S airmon-ng stop " + MAI + "mon"], shell=True, stdout=subprocess.DEVNULL)

    # Retrieve AP information from airodump-ng scan
    TotalAPs = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| wc -l"], shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalAPs = int(TotalAPs)

    # Get ESSIDs
    ESSIDs = []
    for i in range(1, TotalAPs):
        ESSID = (subprocess.check_output(["cat /home/" + username +
                                          "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                          "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                          "| awk '(NR==" + str(i) + "){print $18,$19}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        ESSID = ESSID.replace(',', '')
        ESSID = ESSID.replace('\n', '')
        ESSID = ESSID.replace('\r', '')
        IsESSID = any(str.isdigit(i) for i in ESSID)
        if IsESSID == True:
            ESSID = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                              "| awk '(NR==" + str(i) + "){print $19,$20}'"],
                                             shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
            ESSID = ESSID.replace(',', '')
            ESSID = ESSID.replace('\n', '')
            ESSID = ESSID.replace('\r', '')
            if ESSID == ' ':
                ESSIDs.append('Hidden')
            else:
                ESSID = ESSID.rstrip()
                ESSIDs.append(ESSID)
        else:
            if ESSID == ' ':
                ESSIDs.append('Hidden')
            else:
                ESSID = ESSID.rstrip()
                ESSIDs.append(ESSID)

    # Get BSSIDs and AP Vendors
    BSSIDs = []
    APVendors = []
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    for i in range(1, TotalAPs):
        BSSID = (subprocess.check_output(["cat /home/" + username +
                                          "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                          "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                          "| awk '(NR==" + str(i) + "){print $1}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        BSSID = BSSID.replace(',', '')
        BSSID = BSSID.replace('\n', '')
        BSSID = BSSID.replace('\r', '')
        BSSIDs.append(BSSID)
        try:
            APVendor = MacLookup().lookup(BSSID)
            APVendors.append(APVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            APVendor = "Unknown"
            APVendors.append(APVendor.strip())

    # Get AP channels
    Channels = []
    for i in range(1, TotalAPs):
        Channel = (subprocess.check_output(["cat /home/" + username +
                                            "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                            "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                            "| awk '(NR==" + str(i) + "){print $6}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(',', '')
        Channel = Channel.replace('\n', '')
        Channel = Channel.replace('\r', '')
        Channels.append(Channel)

    # Get throughput rates
    Throughputs = []
    for i in range(1, TotalAPs):
        Throughput = (subprocess.check_output(["cat /home/" + username +
                                               "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                               "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                               "| awk '(NR==" + str(i) + "){print $7}'"],
                                              shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Throughput = Throughput.replace(',', '')
        Throughput = Throughput.replace('\n', '')
        Throughput = Throughput.replace('\r', '')
        if Throughput == '-1':
            Throughput = ' ?'
            Throughputs.append(Throughput)
        else:
            Throughputs.append(Throughput)

    # Get RSSIs
    RSSIs = []
    for i in range(1, TotalAPs):
        RSSI = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $11}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        RSSI = RSSI.replace(',', '')
        RSSI = RSSI.replace('\n', '')
        RSSI = RSSI.replace('\r', '')
        if RSSI == '-1':
            RSSI = ' ?'
            RSSIs.append(RSSI)
        else:
            RSSIs.append(RSSI)

    # Get Encryption Protocol
    ENCs = []
    for i in range(1, TotalAPs):
        EncP = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $8}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        EncP = EncP.replace(',', '')
        EncP = EncP.replace('\n', '')
        EncP = EncP.replace('\r', '')
        ENCs.append(EncP)

    # Get Ciphers
    Ciphers = []
    for i in range(1, TotalAPs):
        Cipher = (subprocess.check_output(["cat /home/" + username +
                                           "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                           "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                           "| awk '(NR==" + str(i) + "){print $9}'"],
                                          shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Cipher = Cipher.replace(',', '')
        Cipher = Cipher.replace('\n', '')
        Cipher = Cipher.replace('\r', '')
        if Cipher == '':
            Cipher = 'NONE'
            Ciphers.append(Cipher)
        else:
            Ciphers.append(Cipher)

    # Get Authentication Method
    AuthMthds = []
    for i in range(1, TotalAPs):
        Auth = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $10}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Auth = Auth.replace(',', '')
        Auth = Auth.replace('\n', '')
        Auth = Auth.replace('\r', '')
        if Auth == '':
            Auth = 'NONE'
            AuthMthds.append(Auth)
        else:
            AuthMthds.append(Auth)

    # Group APs into lists, add lists to dictionary of detected APs
    APs = {}
    APRange = TotalAPs - 1
    for i in range(0, APRange):
        x = ("AP-" + str(i))
        APs[x] = [ESSIDs[i], BSSIDs[i], APVendors[i], Channels[i], Throughputs[i], RSSIs[i], ENCs[i], Ciphers[i], AuthMthds[i]]

    # Group APs into lists by ESSID
    WLANs = {}
    z = 0
    for i in range(0, APRange):
        x = (APs["AP-" + str(i)][0])
        WLANs[x] = []
        for y in range(0, APRange):
            if (APs["AP-" + str(i)][0]) == (APs["AP-" + str(z)][0]):
                WLANs[x] += ((APs["AP-" + str(z)][1]), )
                WLANs[x] += ((APs["AP-" + str(z)][2]), )
                WLANs[x] += ((APs["AP-" + str(z)][3]), )
                WLANs[x] += ((APs["AP-" + str(z)][4]), )
                WLANs[x] += ((APs["AP-" + str(z)][5]), )
                WLANs[x] += ((APs["AP-" + str(z)][6]), )
                WLANs[x] += ((APs["AP-" + str(z)][7]), )
                WLANs[x] += ((APs["AP-" + str(z)][8]), )
            else:
                pass
            z = z + 1
            if z >= APRange:
                z = 0
            else:
                pass

    # Group channels used by ESSID
    ChannelsDict = {}
    for key in WLANs:
        x = key
        ChannelsDict[x] = []
        for i in range(2, (8 * (int(len(WLANs[key])) // 8)), 8):
            try:
                if (WLANs[key][i]) not in ChannelsDict[x]:
                    ChannelsDict[x].append(WLANs[key][i])
                else:
                    pass
            except IndexError:
                pass

    # Retreive Station information from airodump-ng scan
    TotalStations = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                              "| wc -l"], shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalStations = int(TotalStations)

    # Get Station MAC and Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    StationMACs = []
    StationVendors = []
    for i in range(1, TotalStations):
        StationMAC = (subprocess.check_output(["cat /home/" + username +
                                               "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                               "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                               "| awk '(NR==" + str(i) + "){print $1}'"],
                                              shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationMAC = StationMAC.replace(',', '')
        StationMAC = StationMAC.replace('\n', '')
        StationMAC = StationMAC.replace('\r', '')
        if StationMAC == '':
            pass
        else:
            StationMACs.append(StationMAC)
        try:
            StationVendor = MacLookup().lookup(StationMAC)
            StationVendors.append(StationVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            StationVendor = " ?"
            StationVendors.append(StationVendor.strip())

    # Get Station RSSI rates
    StationRSSIs = []
    for i in range(1, TotalStations):
        StationRSSI = (subprocess.check_output(["cat /home/" + username +
                                                "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                                "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                                "| awk '(NR==" + str(i) + "){print $6}'"],
                                               shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationRSSI = StationRSSI.replace(',', '')
        StationRSSI = StationRSSI.replace('\n', '')
        StationRSSI = StationRSSI.replace('\r', '')
        if StationRSSI == '-1':
            StationRSSI = ' ?'
            StationRSSIs.append(StationRSSI.strip())
        else:
            StationRSSIs.append(StationRSSI)
            StationRSSIs.append(StationRSSI.strip())

    # Get Station Associated AP BSSID
    StationAPs = []
    for i in range(1, TotalStations):
        StationAP = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                              "| awk '(NR==" + str(i) + "){print $8}'"],
                                             shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationAP = StationAP.replace(',', '')
        StationAP = StationAP.replace('\n', '')
        StationAP = StationAP.replace('\r', '')
        if StationAP == '(not':
            StationAP = '(not associated)'
            StationAPs.append(StationAP.strip())
        else:
            StationAPs.append(StationAP.strip())

    # Group Stations into lists, add lists to dictionary of detected stations
    Stations = {}
    StationRange = TotalStations - 1
    for i in range(0, StationRange):
        x = ("Station-" + str(i))
        Stations[x] = [StationMACs[i], StationVendors[i], StationRSSIs[i], StationAPs[i]]

    # Group Stations into lists by associated BSSID
    AssociatedStations = {}
    UnassociatedStations = []
    z = 0
    for key in WLANs:
        AssociatedStations[key] = []
    for i in range(0, StationRange):
        for y in range(0, APRange):
            if (Stations["Station-" + str(i)][3]) == '(not associated)':
                UnassociatedStations.append((Stations["Station-" + str(i)][0]))
                UnassociatedStations.append((Stations["Station-" + str(i)][1]))
                UnassociatedStations.append((Stations["Station-" + str(i)][2]))
                break
            elif (Stations["Station-" + str(i)][3]) == (APs["AP-" + str(y)][1]):
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][0]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][1]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][2]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][3]),)
            else:
                pass

# Output data
    End = timeit.default_timer()
    TimeTaken = End - Start

    # Create output file
    filepath = "/home/" + username + "/Documents/NetScanner/"
    filename = filepath + str(datetime.datetime.now().astimezone().strftime('%d-%m-%Y_%H%M%S')) + '_Mode2.txt'
    sys.stdout = open(filename, 'w')

    # Print local interface details
    print(f"\
    \nNETSCANNER has completed on " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')) + "\
    \n \
    \n=============================================== \
    \nDetected Local Host Network Characteristics \
    \n=============================================== \
    \nMost Active Interface: " + MAI + " \
    \nInterface MAC Address: " + str(LANInfo[0]) + " (" + str(LANInfo[18]) + ")\
    \nInterface IPv4 Address: " + str(LANInfo[1]) + " \
    \nNetwork: " + str(LANInfo[6]) + str(LANInfo[5]) + " \
    \nData Exchanged: Transmit: " + str(LANInfo[4]) + ", Received: " + str(LANInfo[3]) + " \
    \nLink Speed: Transmit: " + str(LANInfo[7]) + "Mbps, Receive: " + str(LANInfo[8]) + "Mbps \
    \nActive 802.11 Protocol: " + str(LANInfo[9]) + "\
    \nConnected ESSID: " + str(LANInfo[10]) + " \
    \nAssociated Access Point BSSID: " + str(LANInfo[11]) + " (" + str(LANInfo[12]) + ") \
    \nAccess Point Channel: " + str(LANInfo[14]))
    if (str(LANInfo[13])) == 'N/A':
        print("Operating Frequency: " + str(LANInfo[13]))
    else:
        print("Operating Frequency: " + str(LANInfo[13]) + "Ghz")
    if (str(LANInfo[15])) == 'N/A':
        print("Link Quality: " + str(LANInfo[15]))
    else:
        print("Link Quality: " + str(LANInfo[15]) + "dBm, " + str(LANInfo[16]))
    print("===============================================")

    # Print host details
    print("\n=============================================== \
        \nDiscovered Local Hosts: " + TotalUpHosts + " \
        \n===============================================")
    Range = int(TotalUpHosts)
    for i in range(Range):
        if ResLatency[i] == '':
            ResLatency[i] = 'Undetermined'
        else:
            pass
        print("Host " + ActiveIPs[i] + " (" + ActiveHostnames[i] + ") is up (" + ResLatency[i] + " latency)")
        print("MAC Address: " + ActiveMACAddr[i] + " (" + MACVendors[i] + ")")
        print("-----------------------------------------------")
    print(TotalUpHosts + "responsive hosts out of " + LANInfo[17] + " usable hosts ")
    print("-----------------------------------------------")

    # Print nearby 802.11 WLAN details
    # Print ESSID, ENC type and number of detected APs
    print("\n===============================================")
    TotalWLANs = len(WLANs)
    if 'Hidden' in WLANs:
        print("Discovered Wireless Networks (" + str((int(TotalWLANs)) - 1) + ")")
    else:
        print("Discovered Wireless Networks (" + str(TotalWLANs) + ")")
    print("===============================================")
    for key in WLANs:
        if key != 'Hidden':
            print("ESSID: " + key)
            print("----------------------------------------------- \
            \nDetected Encryption Protocol: " + WLANs[key][5] + "\
            \n----------------------------------------------- \
            \nDetected Channels in use: " + (', '.join('%s'%item for item in ChannelsDict[key])) + " \
            \n----------------------------------------------- \
            \nDiscovered Associated Access Points (" + str(int(len(WLANs[key])) // 8) + ") \
            \n----------------------------------------------- \
            \nBSSID              SIGNAL CH   RATE ENC   CIPHER AUTH  VENDOR")
            # Print list of associated APs
            for i in range(0, (8 * (int(len(WLANs[key])) // 8)), 8):
                print('{0:<19}'.format(WLANs[key][i]), end='')
                print('{0:<7}'.format(WLANs[key][i + 4]), end='')
                print('{0:<5}'.format(WLANs[key][i + 2]), end='')
                print('{0:<5}'.format(WLANs[key][i + 3]), end='')
                print('{0:<6}'.format(WLANs[key][i + 5]), end='')
                print('{0:<7}'.format(WLANs[key][i + 6]), end='')
                print('{0:<6}'.format(WLANs[key][i + 7]), end='')
                print('{0:<40}'.format(WLANs[key][i + 1]), end='')
                print()
            # Print list of associated stations
            print("----------------------------------------------- \
            \nDiscovered Associated Stations (" + str(int(len(AssociatedStations[key])) // 6) + ") \
            \n----------------------------------------------- \
            \nSTATION            ASSOCIATED-BSSID   SIGNAL  VENDOR ")
            if not AssociatedStations[key]:
                pass
            else:
                for i in range(0, (4 * (int(len(AssociatedStations[key])) // 4)), 4):
                    print('{0:<19}'.format(AssociatedStations[key][i]), end='')
                    print('{0:<19}'.format(AssociatedStations[key][i + 3]), end='')
                    print('{0:<8}'.format(AssociatedStations[key][i + 2]), end='')
                    print('{0:<40}'.format(AssociatedStations[key][i + 1]), end='')
                    print()
            print("=============================================== ")
        else:
            pass

    # Print list of hidden APs
    if 'Hidden' in WLANs:
        print("\n============================================== \
        \nDiscovered Hidden Access Points (" + str(int(len(WLANs['Hidden'])) // 8) + ") \
        \n============================================== \
        \nBSSID              SIGNAL CH   RATE ENC   CIPHER AUTH  VENDOR")
        for i in range(0, (8 * (int(len(WLANs['Hidden'])) // 8)), 8):
            print('{0:<19}'.format(WLANs['Hidden'][i]), end='')
            print('{0:<7}'.format(WLANs['Hidden'][i + 4]), end='')
            print('{0:<5}'.format(WLANs['Hidden'][i + 2]), end='')
            print('{0:<5}'.format(WLANs['Hidden'][i + 3]), end='')
            print('{0:<6}'.format(WLANs['Hidden'][i + 5]), end='')
            print('{0:<7}'.format(WLANs['Hidden'][i + 6]), end='')
            print('{0:<6}'.format(WLANs['Hidden'][i + 7]), end='')
            print('{0:<40}'.format(WLANs['Hidden'][i + 1]), end='')
            print()
        # Print list of associated stations
        print("----------------------------------------------- \
        \nDiscovered Associated Stations (" + str(int(len(AssociatedStations['Hidden'])) // 4) + ") \
        \n----------------------------------------------- \
        \nSTATION            ASSOCIATED-BSSID   SIGNAL  VENDOR ")
        if not AssociatedStations['Hidden']:
            pass
        else:
            for i in range(0, (4 * (int(len(AssociatedStations['Hidden'])) // 4)), 4):
                print('{0:<19}'.format(AssociatedStations['Hidden'][i]), end='')
                print('{0:<19}'.format(AssociatedStations['Hidden'][i + 3]), end='')
                print('{0:<8}'.format(AssociatedStations['Hidden'][i + 2]), end='')
                print('{0:<40}'.format(AssociatedStations['Hidden'][i + 1]), end='')
                print()
    else:
        pass

    # Print list of unassociated stations
    print("\n============================================== \
    \nDiscovered Unassociated Stations (" + str(int(len(UnassociatedStations)) // 3) + ") \
    \n============================================== \
    \nSTATION            SIGNAL   VENDOR ")
    for i in range(0, (3 * (int(len(UnassociatedStations)) // 3)), 3):
        print('{0:<19}'.format(UnassociatedStations[i]), end='')
        print('{0:<9}'.format(UnassociatedStations[i + 2]), end='')
        print('{0:<40}'.format(UnassociatedStations[i + 1]), end='')
        print()
    print("----------------------------------------------")

    # Print footer
    print("\n---------------------------------------------- \
    \nScan Complete - An export of this scan has been saved as " + filename + ". \
    \nTotal Scan Time: " + str(round(TimeTaken, 2)) + " Seconds \
    \n-----------------------------------------------")

    sys.stdout = sys.__stdout__

    output = (subprocess.check_output("cat " + filename,
                                      shell=True).decode('utf-8'))
    print(output)

    # Remove temp directory
    subprocess.run(["sudo rm -r /home/" + username + "/Documents/NetScanner/Temp"],
                   shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Execute Mode 3 (-w)
def WIRELESSONLY():
# Print header
    print("\nStarting NETSCANNER at " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')))
    time.sleep(1)
    print("\nDo not kill the program during this process, it may disable your network connection.")

# Create temp directory
    username = os.getlogin()
    tempDir = '/home/' + username + '/Documents/NetScanner/Temp'
    os.chdir(".")
    if os.path.isdir(tempDir):
        pass
    else:
        os.makedirs(tempDir)

# Get most active interface
    # Disables loopback interface
    subprocess.run(["sudo -S ifconfig lo down"],
                   shell=True, stderr=subprocess.DEVNULL)

    # Run ifconfig
    ifconf = (subprocess.check_output('ifconfig', shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))

    # Run ifconfig to gather interface names
    ifaces = (subprocess.check_output(r"ifconfig | sed 's/[ \t].*//;/^$/d'",
                                      shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    Interfaces = []
    Received = []
    Transmit = []

    # Stores interface names into list
    for line in ifaces.splitlines():
        Interfaces.append(line)

    # Stores RX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("RX packets"):
            RX = line.strip().split(" ")[2]
            Received.append(int(RX))

    # Stores TX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("TX packets"):
            TX = line.strip().split(" ")[2]
            Transmit.append(int(TX))

    # Calculates index of most active interface
    getRXmax = max(Received)
    getTXmax = max(Transmit)
    maxRXindex = Received.index(getRXmax)
    maxTXindex = Transmit.index(getTXmax)
    if maxRXindex == maxTXindex:
        MAI = str(Interfaces[maxRXindex]).replace(':', '')
    else:
        print('Error: The most active interface cannot be determined.')
        sys.exit()

    # Re-enables loopback interface
    subprocess.run(["sudo -S ifconfig lo up"], shell=True, stderr=subprocess.DEVNULL)

# Get local interface info + append to list
    LANInfo = []

    # Get MAI MAC
    MAC = (subprocess.check_output(["ifconfig " + MAI + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    MAC = MAC.upper()
    LANInfo.append(MAC.strip())

    # Get MAI NIC Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError

    try:
        HostMAC = MacLookup().lookup(MAC.strip())
    except (InvalidMacError, VendorNotFoundError):
        HostMAC = "Unknown"

    # Get MAI IP
    IP = (subprocess.check_output(["ifconfig " + MAI + r" | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(IP.strip())

    # Get MAI subnet mask
    SubMask = (subprocess.check_output(["ifconfig " + MAI + " | grep -w inet | awk '{print $4}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(SubMask.strip())

    # Get data exchanged in MB
    RXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'RX packets' | awk '{printf $6}{print $7}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXMB = re.sub("[()]","", RXMB)
    LANInfo.append(RXMB.strip())
    TXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'TX packets' | awk '{printf $6}{print $7}'"],
                                shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TXMB = re.sub("[()]","", TXMB)
    LANInfo.append(TXMB.strip())

    # Calculate CIDR
    if SubMask == '128.0.0.0':
        CIDR = '/1'
        UsableHosts = '2,147,483,646'
    elif LANInfo[2] == '192.0.0.0':
        CIDR = '/2'
        UsableHosts = '1,073,741,822'
    elif LANInfo[2] == '224.0.0.0':
        CIDR = '/3'
        UsableHosts = '536,870,910'
    elif LANInfo[2] == '240.0.0.0':
        CIDR = '/4'
        UsableHosts = '268,435,454'
    elif LANInfo[2] == '248.0.0.0':
        CIDR = '/5'
        UsableHosts = '134,217,726'
    elif LANInfo[2] == '252.0.0.0':
        CIDR = '/6'
        UsableHosts = '67,108,862'
    elif LANInfo[2] == '254.0.0.0':
        CIDR = '/7'
        UsableHosts = '33,554,430'
    elif LANInfo[2] == '255.0.0.0':
        CIDR = '/8'
        UsableHosts = '16,777,214'
    elif LANInfo[2] == '255.128.0.0':
        CIDR = '/9'
        UsableHosts = '8,388,606'
    elif LANInfo[2] == '255.192.0.0':
        CIDR = '/10'
        UsableHosts = '4,194,302'
    elif LANInfo[2] == '255.224.0.0':
        CIDR = '/11'
        UsableHosts = '2,097,150'
    elif LANInfo[2] == '255.240.0.0':
        CIDR = '/12'
        UsableHosts = '1,048,574'
    elif LANInfo[2] == '255.248.0.0':
        CIDR = '/13'
        UsableHosts = '524,286'
    elif LANInfo[2] == '255.252.0.0':
        CIDR = '/14'
        UsableHosts = '262,142'
    elif LANInfo[2] == '255.254.0.0':
        CIDR = '/15'
        UsableHosts = '131,070'
    elif LANInfo[2] == '255.255.0.0':
        CIDR = '/16'
        UsableHosts = '65,534'
    elif LANInfo[2] == '255.255.128.0':
        CIDR = '/17'
        UsableHosts = '32,766'
    elif LANInfo[2] == '255.255.192.0':
        CIDR = '/18'
        UsableHosts = '16,382'
    elif LANInfo[2] == '255.255.224.0':
        CIDR = '/19'
        UsableHosts = '8,190'
    elif LANInfo[2] == '255.255.240.0':
        CIDR = '/20'
        UsableHosts = '4,094'
    elif LANInfo[2] == '255.255.248.0':
        CIDR = '/21'
        UsableHosts = '2,046'
    elif LANInfo[2] == '255.255.252.0':
        CIDR = '/22'
        UsableHosts = '1,022'
    elif LANInfo[2] == '255.255.254.0':
        CIDR = '/23'
        UsableHosts = '510'
    elif LANInfo[2] == '255.255.255.0':
        CIDR = '/24'
        UsableHosts = '254'
    elif LANInfo[2] == '255.255.255.128':
        CIDR = '/25'
        UsableHosts = '126'
    elif LANInfo[2] == '255.255.255.192':
        CIDR = '/26'
        UsableHosts = '62'
    elif LANInfo[2] == '255.255.255.224':
        CIDR = '/27'
        UsableHosts = '30'
    elif LANInfo[2] == '255.255.255.240':
        CIDR = '/28'
        UsableHosts = '14'
    elif LANInfo[2] == '255.255.255.248':
        CIDR = '/29'
        UsableHosts = '6'
    elif LANInfo[2] == '255.255.255.252':
        CIDR = '/30'
        UsableHosts = '2'
    elif LANInfo[2] == '255.255.255.254':
        CIDR = '/31'
        UsableHosts = '0'
    elif LANInfo[2] == '255.255.255.255':
        CIDR = '/32'
        UsableHosts = '0'
    else:
        print("\nError: This program requires a valid network connection to operate. Please check your settings and "
              "try again.")
        sys.exit()
    LANInfo.append(CIDR.strip())

# Calculate network address
    # Convert subnet mask to binary
    BinNetAddr = []
    BinMask = '.'.join([bin(int(x)+256)[3:] for x in SubMask.split('.')])

    # Convert device ip to binary
    BinIP = '.'.join([bin(int(x)+256)[3:] for x in IP.split('.')])

    # Calculate network address in binary
    for i in range(len(BinMask)):
        if BinMask[i] == BinIP[i]:
            BinNetAddr.append(BinMask[i])
        else:
            BinNetAddr.append('0')

    # Convert binary network address to decimal
    BinNetAddr = ''.join(BinNetAddr)
    BinNetAddr = BinNetAddr.replace('.', '')
    FirstOctet = BinNetAddr[:8]
    SecondOctet = BinNetAddr[8:16]
    ThirdOctet = BinNetAddr[16:24]
    FourthOctet = BinNetAddr[24:32]
    FirstOctet = int(FirstOctet, 2)
    SecondOctet = int(SecondOctet, 2)
    ThirdOctet = int(ThirdOctet, 2)
    FourthOctet = int(FourthOctet, 2)

    # Arrange into dotted format.
    NetAddr = []
    NetAddr.append(str(FirstOctet))
    NetAddr.append(str(SecondOctet))
    NetAddr.append(str(ThirdOctet))
    NetAddr.append(str(FourthOctet))
    NetAddr = '.'.join(NetAddr)

    # Append network address to list
    LANInfo.append(NetAddr.strip())

    # Get link speeds
    TXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'txrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'rxrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    if TXLinkSp != '':
        TXLinkSp = float(TXLinkSp) / 1000000
        TXLinkSp = int(TXLinkSp)
        LANInfo.append(TXLinkSp)
    else:
        TXLinkSp = 'Unknown '
        LANInfo.append(TXLinkSp)

    if RXLinkSp != '':
        RXLinkSp = float(RXLinkSp) / 1000000
        RXLinkSp = int(RXLinkSp)
        LANInfo.append(RXLinkSp)
    else:
        RXLinkSp = 'Unknown '
        LANInfo.append(RXLinkSp)

    # Get WLAN info
    try:
        iwconf = (subprocess.check_output(["iwconfig " + MAI],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        # Get 802.11 protocol
        IEEEProt = (subprocess.check_output(["iwconfig " + MAI + " | grep 'IEEE' | awk '{printf $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(IEEEProt.strip())

        # Get associated ESSID
        ESSID = (subprocess.check_output(["iwconfig " + MAI + r" | grep ESSID | awk -F: '{print $2}' | sed 's/\"//g'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(ESSID.strip())

        # Get associated AP BSSID
        APMAC = (subprocess.check_output(["iwconfig " + MAI + " | grep 'Access Point' | awk '{print $6}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(APMAC.strip())

        # Get associated AP vendor
        from mac_vendor_lookup import MacLookup
        from mac_vendor_lookup import InvalidMacError
        from mac_vendor_lookup import VendorNotFoundError
        try:
            HostAPVendor = MacLookup().lookup(APMAC.strip())
            LANInfo.append(HostAPVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            HostAPVendor = "Unknown"
            LANInfo.append(HostAPVendor.strip())

        # Get operating frequency
        Freq = (subprocess.check_output(["iwconfig " + MAI + " | grep -o 'Frequency:.*GHz' | sed -e 's/[^0-9.]//g'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(Freq.strip())

        # Get operating channel
        Channel = (subprocess.check_output(["iwlist " + MAI + " channel | grep 'Current Frequency' | awk '{printf $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(')', '')
        if Channel == '':
            Channel = "Channel not identified"
        else:
            pass
        LANInfo.append(Channel.strip())

        # Get link quality
        LinkQual = (subprocess.check_output(["iwconfig " + MAI + "| grep 'Signal level=' | awk '{print $4}' |  sed -e " 
                                                                 "'s/level=//'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(LinkQual.strip())
        if int(LinkQual) <= -80:
            Strength = "Poor"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= -55:
            Strength = "Good"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= 0:
            Strength = "Excellent"
            LANInfo.append(str(Strength).strip())
    except subprocess.CalledProcessError:
        IEEEProt = "No wireless connection"
        LANInfo.append(IEEEProt.strip())
        ESSID = "N/A"
        LANInfo.append(ESSID.strip())
        APMAC = "N/A"
        LANInfo.append(APMAC.strip())
        APMACVendor = "N/A"
        LANInfo.append(APMACVendor.strip())
        Channel = "N/A"
        LANInfo.append(Channel.strip())
        Freq = "N/A "
        LANInfo.append(Freq.strip())
        LinkQual = "N/A "
        LANInfo.append(LinkQual.strip())
        Strength = " "
        LANInfo.append(Strength.strip())
    LANInfo.append(UsableHosts)
    LANInfo.append(HostMAC)

    # Execute airodump-ng capture
    subprocess.run(["sudo -S airmon-ng start " + MAI], shell=True, stdout=subprocess.DEVNULL)
    airodump = subprocess.Popen(["sudo -S airodump-ng " + MAI + "mon --band abg -w /home/" + username
                                 + "/Documents/NetScanner/Temp/airodump-ng --output-format csv"],
                                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(args.WLANScanPeriod)
    subprocess.run(["sudo kill -9 " + str(airodump.pid)], shell=True)
    subprocess.run(["sudo -S airmon-ng stop " + MAI + "mon"],
                   shell=True, stdout=subprocess.DEVNULL)

    # Retrieve AP information from airodump-ng scan
    TotalAPs = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| wc -l"], shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalAPs = int(TotalAPs)

    # Get ESSIDs
    ESSIDs = []
    for i in range(1, TotalAPs):
        ESSID = (subprocess.check_output(["cat /home/" + username +
                                          "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                          "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                          "| awk '(NR==" + str(i) + "){print $18,$19}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        ESSID = ESSID.replace(',', '')
        ESSID = ESSID.replace('\n', '')
        ESSID = ESSID.replace('\r', '')
        IsESSID = any(str.isdigit(i) for i in ESSID)
        if IsESSID == True:
            ESSID = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                              "| awk '(NR==" + str(i) + "){print $19,$20}'"],
                                             shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
            ESSID = ESSID.replace(',', '')
            ESSID = ESSID.replace('\n', '')
            ESSID = ESSID.replace('\r', '')
            if ESSID == ' ':
                ESSIDs.append('Hidden')
            else:
                ESSID = ESSID.rstrip()
                ESSIDs.append(ESSID)
        else:
            if ESSID == ' ':
                ESSIDs.append('Hidden')
            else:
                ESSID = ESSID.rstrip()
                ESSIDs.append(ESSID)

    # Get BSSIDs and AP Vendors
    BSSIDs = []
    APVendors = []
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    for i in range(1, TotalAPs):
        BSSID = (subprocess.check_output(["cat /home/" + username +
                                          "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                          "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                          "| awk '(NR==" + str(i) + "){print $1}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        BSSID = BSSID.replace(',', '')
        BSSID = BSSID.replace('\n', '')
        BSSID = BSSID.replace('\r', '')
        BSSIDs.append(BSSID)
        try:
            APVendor = MacLookup().lookup(BSSID)
            APVendors.append(APVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            APVendor = "Unknown"
            APVendors.append(APVendor.strip())

    # Get AP channels
    Channels = []
    for i in range(1, TotalAPs):
        Channel = (subprocess.check_output(["cat /home/" + username +
                                            "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                            "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                            "| awk '(NR==" + str(i) + "){print $6}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(',', '')
        Channel = Channel.replace('\n', '')
        Channel = Channel.replace('\r', '')
        Channels.append(Channel)

    # Get throughput rates
    Throughputs = []
    for i in range(1, TotalAPs):
        Throughput = (subprocess.check_output(["cat /home/" + username +
                                               "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                               "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                               "| awk '(NR==" + str(i) + "){print $7}'"],
                                              shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Throughput = Throughput.replace(',', '')
        Throughput = Throughput.replace('\n', '')
        Throughput = Throughput.replace('\r', '')
        if Throughput == '-1':
            Throughput = ' ?'
            Throughputs.append(Throughput)
        else:
            Throughputs.append(Throughput)

    # Get RSSIs
    RSSIs = []
    for i in range(1, TotalAPs):
        RSSI = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $11}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        RSSI = RSSI.replace(',', '')
        RSSI = RSSI.replace('\n', '')
        RSSI = RSSI.replace('\r', '')
        if RSSI == '-1':
            RSSI = ' ?'
            RSSIs.append(RSSI)
        else:
            RSSIs.append(RSSI)

    # Get Encryption Protocol
    ENCs = []
    for i in range(1, TotalAPs):
        EncP = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $8}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        EncP = EncP.replace(',', '')
        EncP = EncP.replace('\n', '')
        EncP = EncP.replace('\r', '')
        ENCs.append(EncP)

    # Get Ciphers
    Ciphers = []
    for i in range(1, TotalAPs):
        Cipher = (subprocess.check_output(["cat /home/" + username +
                                           "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                           "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                           "| awk '(NR==" + str(i) + "){print $9}'"],
                                          shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Cipher = Cipher.replace(',', '')
        Cipher = Cipher.replace('\n', '')
        Cipher = Cipher.replace('\r', '')
        if Cipher == '':
            Cipher = 'NONE'
            Ciphers.append(Cipher)
        else:
            Ciphers.append(Cipher)

    # Get Authentication Method
    AuthMthds = []
    for i in range(1, TotalAPs):
        Auth = (subprocess.check_output(["cat /home/" + username +
                                         "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                         "| awk '/Key/{flag=1;next}/Station/{flag=0}flag' "
                                         "| awk '(NR==" + str(i) + "){print $10}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Auth = Auth.replace(',', '')
        Auth = Auth.replace('\n', '')
        Auth = Auth.replace('\r', '')
        if Auth == '':
            Auth = 'NONE'
            AuthMthds.append(Auth)
        else:
            AuthMthds.append(Auth)

    # Group APs into lists, add lists to dictionary of detected APs
    APs = {}
    APRange = TotalAPs - 1
    for i in range(0, APRange):
        x = ("AP-" + str(i))
        APs[x] = [ESSIDs[i], BSSIDs[i], APVendors[i], Channels[i], Throughputs[i], RSSIs[i], ENCs[i], Ciphers[i], AuthMthds[i]]

    # Group APs into lists by ESSID
    WLANs = {}
    z = 0
    for i in range(0, APRange):
        x = (APs["AP-" + str(i)][0])
        WLANs[x] = []
        for y in range(0, APRange):
            if (APs["AP-" + str(i)][0]) == (APs["AP-" + str(z)][0]):
                WLANs[x] += ((APs["AP-" + str(z)][1]), )
                WLANs[x] += ((APs["AP-" + str(z)][2]), )
                WLANs[x] += ((APs["AP-" + str(z)][3]), )
                WLANs[x] += ((APs["AP-" + str(z)][4]), )
                WLANs[x] += ((APs["AP-" + str(z)][5]), )
                WLANs[x] += ((APs["AP-" + str(z)][6]), )
                WLANs[x] += ((APs["AP-" + str(z)][7]), )
                WLANs[x] += ((APs["AP-" + str(z)][8]), )
            else:
                pass
            z = z + 1
            if z >= APRange:
                z = 0
            else:
                pass

    # Group channels used by ESSID
    ChannelsDict = {}
    for key in WLANs:
        x = key
        ChannelsDict[x] = []
        for i in range(2, (8 * (int(len(WLANs[key])) // 8)), 8):
            try:
                if (WLANs[key][i]) not in ChannelsDict[x]:
                    ChannelsDict[x].append(WLANs[key][i])
                else:
                    pass
            except IndexError:
                pass

    # Retreive Station information from airodump-ng scan
    TotalStations = (subprocess.check_output(["cat /home/" + username
                                              + "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                                "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                                "| wc -l"], shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalStations = int(TotalStations)

    # Get Station MAC and Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    StationMACs = []
    StationVendors = []
    for i in range(1, TotalStations):
        StationMAC = (subprocess.check_output(["cat /home/" + username +
                                               "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                               "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                               "| awk '(NR==" + str(i) + "){print $1}'"],
                                              shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationMAC = StationMAC.replace(',', '')
        StationMAC = StationMAC.replace('\n', '')
        StationMAC = StationMAC.replace('\r', '')
        if StationMAC == '':
            pass
        else:
            StationMACs.append(StationMAC)
        try:
            StationVendor = MacLookup().lookup(StationMAC)
            StationVendors.append(StationVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            StationVendor = " ?"
            StationVendors.append(StationVendor.strip())

    # Get Station RSSI rates
    StationRSSIs = []
    for i in range(1, TotalStations):
        StationRSSI = (subprocess.check_output(["cat /home/" + username +
                                                "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                                "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                                "| awk '(NR==" + str(i) + "){print $6}'"],
                                               shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationRSSI = StationRSSI.replace(',', '')
        StationRSSI = StationRSSI.replace('\n', '')
        StationRSSI = StationRSSI.replace('\r', '')
        if StationRSSI == '-1':
            StationRSSI = ' ?'
            StationRSSIs.append(StationRSSI.strip())
        else:
            StationRSSIs.append(StationRSSI)
            StationRSSIs.append(StationRSSI.strip())

    # Get Station Associated AP BSSID
    StationAPs = []
    for i in range(1, TotalStations):
        StationAP = (subprocess.check_output(["cat /home/" + username +
                                              "/Documents/NetScanner/Temp/airodump-ng-01.csv "
                                              "| awk '/ESSIDs/{flag=1;next}/'abcdefghijklmnopqrstuvwxyz'/{flag=0}flag' "
                                              "| awk '(NR==" + str(i) + "){print $8}'"],
                                             shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        StationAP = StationAP.replace(',', '')
        StationAP = StationAP.replace('\n', '')
        StationAP = StationAP.replace('\r', '')
        if StationAP == '(not':
            StationAP = '(not associated)'
            StationAPs.append(StationAP.strip())
        else:
            StationAPs.append(StationAP.strip())

    # Group Stations into lists, add lists to dictionary of detected stations
    Stations = {}
    StationRange = TotalStations - 1
    for i in range(0, StationRange):
        x = ("Station-" + str(i))
        Stations[x] = [StationMACs[i], StationVendors[i], StationRSSIs[i], StationAPs[i]]

    # Group Stations into lists by associated BSSID
    AssociatedStations = {}
    UnassociatedStations = []
    z = 0
    for key in WLANs:
        AssociatedStations[key] = []
    for i in range(0, StationRange):
        for y in range(0, APRange):
            if (Stations["Station-" + str(i)][3]) == '(not associated)':
                UnassociatedStations.append((Stations["Station-" + str(i)][0]))
                UnassociatedStations.append((Stations["Station-" + str(i)][1]))
                UnassociatedStations.append((Stations["Station-" + str(i)][2]))
                break
            elif (Stations["Station-" + str(i)][3]) == (APs["AP-" + str(y)][1]):
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][0]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][1]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][2]), )
                AssociatedStations[(APs["AP-" + str(y)][0])] += ((Stations["Station-" + str(i)][3]),)
            else:
                pass

# Output data
    End = timeit.default_timer()
    TimeTaken = End - Start

    # Create output file
    filepath = "/home/" + username + "/Documents/NetScanner/"
    filename = filepath + str(datetime.datetime.now().astimezone().strftime('%d-%m-%Y_%H%M%S')) + '_Mode3.txt'
    sys.stdout = open(filename, 'w')

    # Print local interface details
    print(f"\
    \nNETSCANNER has completed on " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')) + "\
    \n \
    \n=============================================== \
    \nDetected Local Host Network Characteristics \
    \n=============================================== \
    \nMost Active Interface: " + MAI + " \
    \nInterface MAC Address: " + str(LANInfo[0]) + " (" + str(LANInfo[18]) + ")\
    \nInterface IPv4 Address: " + str(LANInfo[1]) + " \
    \nNetwork: " + str(LANInfo[6]) + str(LANInfo[5]) + " \
    \nData Exchanged: Transmit: " + str(LANInfo[4]) + ", Received: " + str(LANInfo[3]) + " \
    \nLink Speed: Transmit: " + str(LANInfo[7]) + "Mbps, Receive: " + str(LANInfo[8]) + "Mbps \
    \nActive 802.11 Protocol: " + str(LANInfo[9]) + "\
    \nConnected ESSID: " + str(LANInfo[10]) + " \
    \nAssociated Access Point BSSID: " + str(LANInfo[11]) + " (" + str(LANInfo[12]) + ") \
    \nAccess Point Channel: " + str(LANInfo[14]))
    if (str(LANInfo[13])) == 'N/A':
        print("Operating Frequency: " + str(LANInfo[13]))
    else:
        print("Operating Frequency: " + str(LANInfo[13]) + "Ghz")
    if (str(LANInfo[15])) == 'N/A':
        print("Link Quality: " + str(LANInfo[15]))
    else:
        print("Link Quality: " + str(LANInfo[15]) + "dBm, " + str(LANInfo[16]))
    print("===============================================")

    # Print nearby 802.11 WLAN details
    # Print ESSID, ENC type and number of detected APs
    print("\n===============================================")
    TotalWLANs = len(WLANs)
    if 'Hidden' in WLANs:
        print("Discovered Wireless Networks (" + str((int(TotalWLANs)) - 1) + ")")
    else:
        print("Discovered Wireless Networks (" + str(TotalWLANs) + ")")
    print("===============================================")
    for key in WLANs:
        if key != 'Hidden':
            print("ESSID: " + key)
            print("----------------------------------------------- \
            \nDetected Encryption Protocol: " + WLANs[key][5] + "\
            \n----------------------------------------------- \
            \nDetected Channels in use: " + (', '.join('%s'%item for item in ChannelsDict[key])) + " \
            \n----------------------------------------------- \
            \nDiscovered Associated Access Points (" + str(int(len(WLANs[key])) // 8) + ") \
            \n----------------------------------------------- \
            \nBSSID              SIGNAL CH   RATE ENC   CIPHER AUTH  VENDOR")
            # Print list of associated APs
            for i in range(0, (8 * (int(len(WLANs[key])) // 8)), 8):
                print('{0:<19}'.format(WLANs[key][i]), end='')
                print('{0:<7}'.format(WLANs[key][i + 4]), end='')
                print('{0:<5}'.format(WLANs[key][i + 2]), end='')
                print('{0:<5}'.format(WLANs[key][i + 3]), end='')
                print('{0:<6}'.format(WLANs[key][i + 5]), end='')
                print('{0:<7}'.format(WLANs[key][i + 6]), end='')
                print('{0:<6}'.format(WLANs[key][i + 7]), end='')
                print('{0:<40}'.format(WLANs[key][i + 1]), end='')
                print()
            # Print list of associated stations
            print("----------------------------------------------- \
            \nDiscovered Associated Stations (" + str(int(len(AssociatedStations[key])) // 6) + ") \
            \n----------------------------------------------- \
            \nSTATION            ASSOCIATED-BSSID   SIGNAL  VENDOR ")
            if not AssociatedStations[key]:
                pass
            else:
                for i in range(0, (4 * (int(len(AssociatedStations[key])) // 4)), 4):
                    print('{0:<19}'.format(AssociatedStations[key][i]), end='')
                    print('{0:<19}'.format(AssociatedStations[key][i + 3]), end='')
                    print('{0:<8}'.format(AssociatedStations[key][i + 2]), end='')
                    print('{0:<40}'.format(AssociatedStations[key][i + 1]), end='')
                    print()
            print("=============================================== ")
        else:
            pass

    # Print list of hidden APs
    if 'Hidden' in WLANs:
        print("\n============================================== \
        \nDiscovered Hidden Access Points (" + str(int(len(WLANs['Hidden'])) // 8) + ") \
        \n============================================== \
        \nBSSID              SIGNAL CH   RATE ENC   CIPHER AUTH  VENDOR")
        for i in range(0, (8 * (int(len(WLANs['Hidden'])) // 8)), 8):
            print('{0:<19}'.format(WLANs['Hidden'][i]), end='')
            print('{0:<7}'.format(WLANs['Hidden'][i + 4]), end='')
            print('{0:<5}'.format(WLANs['Hidden'][i + 2]), end='')
            print('{0:<5}'.format(WLANs['Hidden'][i + 3]), end='')
            print('{0:<6}'.format(WLANs['Hidden'][i + 5]), end='')
            print('{0:<7}'.format(WLANs['Hidden'][i + 6]), end='')
            print('{0:<6}'.format(WLANs['Hidden'][i + 7]), end='')
            print('{0:<40}'.format(WLANs['Hidden'][i + 1]), end='')
            print()
        # Print list of associated stations
        print("----------------------------------------------- \
        \nDiscovered Associated Stations (" + str(int(len(AssociatedStations['Hidden'])) // 4) + ") \
        \n----------------------------------------------- \
        \nSTATION            ASSOCIATED-BSSID   SIGNAL  VENDOR ")
        if not AssociatedStations['Hidden']:
            pass
        else:
            for i in range(0, (4 * (int(len(AssociatedStations['Hidden'])) // 4)), 4):
                print('{0:<19}'.format(AssociatedStations['Hidden'][i]), end='')
                print('{0:<19}'.format(AssociatedStations['Hidden'][i + 3]), end='')
                print('{0:<8}'.format(AssociatedStations['Hidden'][i + 2]), end='')
                print('{0:<40}'.format(AssociatedStations['Hidden'][i + 1]), end='')
                print()
    else:
        pass

    # Print list of unassociated stations
    print("\n============================================== \
    \nDiscovered Unassociated Stations (" + str(int(len(UnassociatedStations)) // 3) + ") \
    \n============================================== \
    \nSTATION            SIGNAL   VENDOR ")
    for i in range(0, (3 * (int(len(UnassociatedStations)) // 3)), 3):
        print('{0:<19}'.format(UnassociatedStations[i]), end='')
        print('{0:<9}'.format(UnassociatedStations[i + 2]), end='')
        print('{0:<40}'.format(UnassociatedStations[i + 1]), end='')
        print()
    print("----------------------------------------------")

    # Print footer
    print("\n---------------------------------------------- \
    \nScan Complete - An export of this scan has been saved as " + filename + ". \
    \nTotal Scan Time: " + str(round(TimeTaken, 2)) + " Seconds \
    \n-----------------------------------------------")

    sys.stdout = sys.__stdout__

    output = (subprocess.check_output("cat " + filename,
                                      shell=True).decode('utf-8'))
    print(output)

    # Remove temp directory
    subprocess.run(["sudo rm -r /home/" + username + "/Documents/NetScanner/Temp"],
                   shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Execute Mode 4 (-l)
def LOCALONLY():
# Print header
    print("\nStarting NETSCANNER at " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')))
    time.sleep(1)
    print("\nDo not kill the program during this process, it may disable your network connection.")

# Create temp directory
    username = os.getlogin()
    tempDir = '/home/' + username + '/Documents/NetScanner/Temp'
    os.chdir(".")
    if os.path.isdir(tempDir):
        pass
    else:
        os.makedirs(tempDir)

# Get most active interface
    # Disables loopback interface
    subprocess.run(["sudo -S ifconfig lo down"],
                   shell=True, stderr=subprocess.DEVNULL)

    # Run ifconfig
    ifconf = (subprocess.check_output('ifconfig', shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))

    # Run ifconfig to gather interface names
    ifaces = (subprocess.check_output(r"ifconfig | sed 's/[ \t].*//;/^$/d'",
                                      shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    Interfaces = []
    Received = []
    Transmit = []

    # Stores interface names into list
    for line in ifaces.splitlines():
        Interfaces.append(line)

    # Stores RX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("RX packets"):
            RX = line.strip().split(" ")[2]
            Received.append(int(RX))

    # Stores TX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("TX packets"):
            TX = line.strip().split(" ")[2]
            Transmit.append(int(TX))

    # Calculates index of most active interface
    getRXmax = max(Received)
    getTXmax = max(Transmit)
    maxRXindex = Received.index(getRXmax)
    maxTXindex = Transmit.index(getTXmax)
    if maxRXindex == maxTXindex:
        MAI = str(Interfaces[maxRXindex]).replace(':', '')
    else:
        print('Error: The most active interface cannot be determined.')
        sys.exit()

    # Re-enables loopback interface
    subprocess.run(["sudo -S ifconfig lo up"], shell=True, stderr=subprocess.DEVNULL)

# Get local interface info + append to list
    LANInfo = []

    # Get MAI MAC
    MAC = (subprocess.check_output(["ifconfig " + MAI + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    MAC = MAC.upper()
    LANInfo.append(MAC.strip())

    # Get MAI NIC Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError

    try:
        HostMAC = MacLookup().lookup(MAC.strip())
    except (InvalidMacError, VendorNotFoundError):
        HostMAC = "Unknown"

    # Get MAI IP
    IP = (subprocess.check_output(["ifconfig " + MAI + r" | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(IP.strip())

    # Get MAI subnet mask
    SubMask = (subprocess.check_output(["ifconfig " + MAI + " | grep -w inet | awk '{print $4}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(SubMask.strip())

    # Get data exchanged in MB
    RXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'RX packets' | awk '{printf $6}{print $7}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXMB = re.sub("[()]","", RXMB)
    LANInfo.append(RXMB.strip())
    TXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'TX packets' | awk '{printf $6}{print $7}'"],
                                shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TXMB = re.sub("[()]","", TXMB)
    LANInfo.append(TXMB.strip())

    # Calculate CIDR
    if SubMask == '128.0.0.0':
        CIDR = '/1'
        UsableHosts = '2,147,483,646'
    elif LANInfo[2] == '192.0.0.0':
        CIDR = '/2'
        UsableHosts = '1,073,741,822'
    elif LANInfo[2] == '224.0.0.0':
        CIDR = '/3'
        UsableHosts = '536,870,910'
    elif LANInfo[2] == '240.0.0.0':
        CIDR = '/4'
        UsableHosts = '268,435,454'
    elif LANInfo[2] == '248.0.0.0':
        CIDR = '/5'
        UsableHosts = '134,217,726'
    elif LANInfo[2] == '252.0.0.0':
        CIDR = '/6'
        UsableHosts = '67,108,862'
    elif LANInfo[2] == '254.0.0.0':
        CIDR = '/7'
        UsableHosts = '33,554,430'
    elif LANInfo[2] == '255.0.0.0':
        CIDR = '/8'
        UsableHosts = '16,777,214'
    elif LANInfo[2] == '255.128.0.0':
        CIDR = '/9'
        UsableHosts = '8,388,606'
    elif LANInfo[2] == '255.192.0.0':
        CIDR = '/10'
        UsableHosts = '4,194,302'
    elif LANInfo[2] == '255.224.0.0':
        CIDR = '/11'
        UsableHosts = '2,097,150'
    elif LANInfo[2] == '255.240.0.0':
        CIDR = '/12'
        UsableHosts = '1,048,574'
    elif LANInfo[2] == '255.248.0.0':
        CIDR = '/13'
        UsableHosts = '524,286'
    elif LANInfo[2] == '255.252.0.0':
        CIDR = '/14'
        UsableHosts = '262,142'
    elif LANInfo[2] == '255.254.0.0':
        CIDR = '/15'
        UsableHosts = '131,070'
    elif LANInfo[2] == '255.255.0.0':
        CIDR = '/16'
        UsableHosts = '65,534'
    elif LANInfo[2] == '255.255.128.0':
        CIDR = '/17'
        UsableHosts = '32,766'
    elif LANInfo[2] == '255.255.192.0':
        CIDR = '/18'
        UsableHosts = '16,382'
    elif LANInfo[2] == '255.255.224.0':
        CIDR = '/19'
        UsableHosts = '8,190'
    elif LANInfo[2] == '255.255.240.0':
        CIDR = '/20'
        UsableHosts = '4,094'
    elif LANInfo[2] == '255.255.248.0':
        CIDR = '/21'
        UsableHosts = '2,046'
    elif LANInfo[2] == '255.255.252.0':
        CIDR = '/22'
        UsableHosts = '1,022'
    elif LANInfo[2] == '255.255.254.0':
        CIDR = '/23'
        UsableHosts = '510'
    elif LANInfo[2] == '255.255.255.0':
        CIDR = '/24'
        UsableHosts = '254'
    elif LANInfo[2] == '255.255.255.128':
        CIDR = '/25'
        UsableHosts = '126'
    elif LANInfo[2] == '255.255.255.192':
        CIDR = '/26'
        UsableHosts = '62'
    elif LANInfo[2] == '255.255.255.224':
        CIDR = '/27'
        UsableHosts = '30'
    elif LANInfo[2] == '255.255.255.240':
        CIDR = '/28'
        UsableHosts = '14'
    elif LANInfo[2] == '255.255.255.248':
        CIDR = '/29'
        UsableHosts = '6'
    elif LANInfo[2] == '255.255.255.252':
        CIDR = '/30'
        UsableHosts = '2'
    elif LANInfo[2] == '255.255.255.254':
        CIDR = '/31'
        UsableHosts = '0'
    elif LANInfo[2] == '255.255.255.255':
        CIDR = '/32'
        UsableHosts = '0'
    else:
        print("\nError: This program requires a valid network connection to operate. Please check your settings and "   
              "try again.")
        sys.exit()
    LANInfo.append(CIDR.strip())

# Calculate network address
    # Convert subnet mask to binary
    BinNetAddr = []
    BinMask = '.'.join([bin(int(x)+256)[3:] for x in SubMask.split('.')])

    # Convert device ip to binary
    BinIP = '.'.join([bin(int(x)+256)[3:] for x in IP.split('.')])

    # Calculate network address in binary
    for i in range(len(BinMask)):
        if BinMask[i] == BinIP[i]:
            BinNetAddr.append(BinMask[i])
        else:
            BinNetAddr.append('0')

    # Convert binary network address to decimal
    BinNetAddr = ''.join(BinNetAddr)
    BinNetAddr = BinNetAddr.replace('.', '')
    FirstOctet = BinNetAddr[:8]
    SecondOctet = BinNetAddr[8:16]
    ThirdOctet = BinNetAddr[16:24]
    FourthOctet = BinNetAddr[24:32]
    FirstOctet = int(FirstOctet, 2)
    SecondOctet = int(SecondOctet, 2)
    ThirdOctet = int(ThirdOctet, 2)
    FourthOctet = int(FourthOctet, 2)

    # Arrange into dotted format.
    NetAddr = []
    NetAddr.append(str(FirstOctet))
    NetAddr.append(str(SecondOctet))
    NetAddr.append(str(ThirdOctet))
    NetAddr.append(str(FourthOctet))
    NetAddr = '.'.join(NetAddr)

    # Append network address to list
    LANInfo.append(NetAddr.strip())

    # Get link speeds
    TXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'txrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'rxrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    if TXLinkSp != '':
        TXLinkSp = float(TXLinkSp) / 1000000
        TXLinkSp = int(TXLinkSp)
        LANInfo.append(TXLinkSp)
    else:
        TXLinkSp = 'Unknown '
        LANInfo.append(TXLinkSp)

    if RXLinkSp != '':
        RXLinkSp = float(RXLinkSp) / 1000000
        RXLinkSp = int(RXLinkSp)
        LANInfo.append(RXLinkSp)
    else:
        RXLinkSp = 'Unknown '
        LANInfo.append(RXLinkSp)

    # Get WLAN info
    try:
        iwconf = (subprocess.check_output(["iwconfig " + MAI],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        # Get 802.11 protocol
        IEEEProt = (subprocess.check_output(["iwconfig " + MAI + " | grep 'IEEE' | awk '{printf $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(IEEEProt.strip())

        # Get associated ESSID
        ESSID = (subprocess.check_output(["iwconfig " + MAI + r" | grep ESSID | awk -F: '{print $2}' | sed 's/\"//g'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(ESSID.strip())

        # Get associated AP BSSID
        APMAC = (subprocess.check_output(["iwconfig " + MAI + " | grep 'Access Point' | awk '{print $6}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(APMAC.strip())

        # Get associated AP vendor
        from mac_vendor_lookup import MacLookup
        from mac_vendor_lookup import InvalidMacError
        from mac_vendor_lookup import VendorNotFoundError
        try:
            HostAPVendor = MacLookup().lookup(APMAC.strip())
            LANInfo.append(HostAPVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            HostAPVendor = "Unknown"
            LANInfo.append(HostAPVendor.strip())

        # Get operating frequency
        Freq = (subprocess.check_output(["iwconfig " + MAI + " | grep -o 'Frequency:.*GHz' | sed -e 's/[^0-9.]//g'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(Freq.strip())

        # Get operating channel
        Channel = (subprocess.check_output(["iwlist " + MAI + " channel | grep 'Current Frequency' | awk '{printf $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(')', '')
        if Channel == '':
            Channel = "Channel not identified"
        else:
            pass
        LANInfo.append(Channel.strip())

        # Get link quality
        LinkQual = (subprocess.check_output(["iwconfig " + MAI + "| grep 'Signal level=' | awk '{print $4}' |  sed -e " 
                                                                 "'s/level=//'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(LinkQual.strip())
        if int(LinkQual) <= -80:
            Strength = "Poor"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= -55:
            Strength = "Good"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= 0:
            Strength = "Excellent"
            LANInfo.append(str(Strength).strip())
    except subprocess.CalledProcessError:
        IEEEProt = "No wireless connection"
        LANInfo.append(IEEEProt.strip())
        ESSID = "N/A"
        LANInfo.append(ESSID.strip())
        APMAC = "N/A"
        LANInfo.append(APMAC.strip())
        APMACVendor = "N/A"
        LANInfo.append(APMACVendor.strip())
        Channel = "N/A"
        LANInfo.append(Channel.strip())
        Freq = "N/A "
        LANInfo.append(Freq.strip())
        LinkQual = "N/A "
        LANInfo.append(LinkQual.strip())
        Strength = " "
        LANInfo.append(Strength.strip())
    LANInfo.append(UsableHosts)
    LANInfo.append(HostMAC)

# Execute host discovery techniques
    # Execute Nmap ARP ping scan
    subprocess.run(["sudo -S nmap -PR -sn -T4 -n -oN /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Execute Nmap rDNS lookup scan
    subprocess.run(["sudo -S nmap -R -PR -sn -T5 -oN /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Retrieve required data from output
    # Retrieve total hosts
    ActiveIPs = []
    TotalUpHosts = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'Nmap done at' | awk '{print $14}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalUpHosts = TotalUpHosts.replace('(', '')
    TotalUpHosts = TotalUpHosts.replace('\n', ' ')

    # Retrieve host IP addresses from ARP Scan
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        IPAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        IPAddrs = IPAddrs.replace('\n', '')
        ActiveIPs.append(IPAddrs)

    # Retrieve hostnames from rDNS lookup
    ActiveHostnames = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Hostname = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt "
                                             + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Hostname = Hostname.strip()
        Hostname = Hostname.replace('\n', '')
        try:
            IsChar = Hostname[0]
        except IndexError:
            IsChar = '1'
        if IsChar.isdigit() == True:
            Hostname = 'Unknown Hostname'
            ActiveHostnames.append(Hostname)
        elif IsChar.isdigit() == False:
            ActiveHostnames.append(Hostname)

    # Retrieve ARP reply latency from ARP Scan
    ResLatency = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Latency = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Host is up' | awk 'NR==" + str(i) + "{print $4}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Latency = Latency.replace('(', '')
        Latency = Latency.replace('\n', '')
        ResLatency.append(Latency)

    # Retrieve host MAC address from ARP Scan
    ActiveMACAddr = []
    MACVendors = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        MACAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'MAC Address: ' | awk 'NR==" + str(i) + "{print $3}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        MACAddrs = MACAddrs.replace('(', '')
        MACAddrs = MACAddrs.replace('\n', '')
        if MACAddrs == '':
            MACAddrs = 'Unknown'
            ActiveMACAddr.append(MACAddrs)
        else:
            ActiveMACAddr.append(MACAddrs)

    # Determine host NIC vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    Range = int(TotalUpHosts)
    for i in range(0, Range):
        try:
            MACVendor = MacLookup().lookup(ActiveMACAddr[i].strip())
            MACVendors.append(MACVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            MACVendor = "Unknown"
            MACVendors.append(MACVendor.strip())

# Execute port scans
    # Execute Nmap TCP Half Open and UDP port scan on all hosts
    # This can be resource intensive
    Range = int(TotalUpHosts) - 1
    PortScanCmds = []
    for i in range(0, Range, 9):
        try:
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i]
                                + ".txt " + ActiveIPs[i] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+1]
                                + ".txt " + ActiveIPs[i+1] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+2]
                                + ".txt " + ActiveIPs[i+2] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+3]
                                + ".txt " + ActiveIPs[i+3] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+4]
                                + ".txt " + ActiveIPs[i+4] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+5]
                                + ".txt " + ActiveIPs[i+5] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+6]
                                + ".txt " + ActiveIPs[i+6] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+7]
                                + ".txt " + ActiveIPs[i+7] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+8]
                                + ".txt " + ActiveIPs[i+8] + "/32")
            PortScanCmds.append("sudo -S nmap -sS -sU -T4 -n -Pn " + PortRange
                                + " -oN /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i+9]
                                + ".txt " + ActiveIPs[i+9] + "/32")
        except IndexError:
            pass
    from subprocess import Popen
    processes = [Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) for cmd in PortScanCmds]
    time.sleep(args.PortScanPeriod)

# Output data
    End = timeit.default_timer()
    TimeTaken = End - Start

    # Create output file
    filepath = "/home/" + username + "/Documents/NetScanner/"
    filename = filepath + str(datetime.datetime.now().astimezone().strftime('%d-%m-%Y_%H%M%S')) + '_Mode4.txt'
    sys.stdout = open(filename, 'w')

    # Print local interface details
    print(f"\
    \nNETSCANNER has completed on " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')) + "\
    \n \
    \n=============================================== \
    \nDetected Local Host Network Characteristics \
    \n=============================================== \
    \nMost Active Interface: " + MAI + " \
    \nInterface MAC Address: " + str(LANInfo[0]) + " (" + str(LANInfo[18]) + ")\
    \nInterface IPv4 Address: " + str(LANInfo[1]) + " \
    \nNetwork: " + str(LANInfo[6]) + str(LANInfo[5]) + " \
    \nData Exchanged: Transmit: " + str(LANInfo[4]) + ", Received: " + str(LANInfo[3]) + " \
    \nLink Speed: Transmit: " + str(LANInfo[7]) + "Mbps, Receive: " + str(LANInfo[8]) + "Mbps \
    \nActive 802.11 Protocol: " + str(LANInfo[9]) + "\
    \nConnected ESSID: " + str(LANInfo[10]) + " \
    \nAssociated Access Point BSSID: " + str(LANInfo[11]) + " (" + str(LANInfo[12]) + ") \
    \nAccess Point Channel: " + str(LANInfo[14]))
    if (str(LANInfo[13])) == 'N/A':
        print("Operating Frequency: " + str(LANInfo[13]))
    else:
        print("Operating Frequency: " + str(LANInfo[13]) + "Ghz")
    if (str(LANInfo[15])) == 'N/A':
        print("Link Quality: " + str(LANInfo[15]))
    else:
        print("Link Quality: " + str(LANInfo[15]) + "dBm, " + str(LANInfo[16]))
    print("===============================================")

    # Print host details + port states
    print("\n=============================================== \
    \nDiscovered Local Hosts: " + TotalUpHosts + " \
    \n===============================================")
    Range = int(TotalUpHosts)
    for i in range(Range):
        if ResLatency[i] == '':
            ResLatency[i] = 'Undetermined'
        else:
            pass
        print("Host " + ActiveIPs[i] + " (" + ActiveHostnames[i] + ") is up (" + ResLatency[i] + " latency)")
        print("MAC Address: " + ActiveMACAddr[i] + " (" + MACVendors[i] + ")")

        # Retrieve not shown ports or ignored state lines
        try:
            NotShown = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | grep 'Not shown: '"],
                                            shell=True).decode('utf-8'))
            NotShown = NotShown.replace('\n', '')
            print(NotShown)
        except subprocess.CalledProcessError:
            pass
        try:
            IsAllIgnored = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | grep 'All'"],
                                                    shell=True).decode('utf-8'))
            print("All scanned ports are in the ignored state \
            \n-----------------------------------------------")
        except subprocess.CalledProcessError:

            # Retrieve and print port statuses
            with open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt", "r") as f:
                output = f.read()
                if 'Not shown' in output:
                    NumOfPorts = sum(1 for l in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + str(ActiveIPs[i]) + ".txt")) - 1
                    if 'MAC' in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt").read():
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/Not shown:/{flag=1;next}/MAC/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                    else:
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/Not shown:/{flag=1;next}/Nmap/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                elif 'PORT' in output:
                    NumOfPorts = sum(1 for l in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + str(ActiveIPs[i]) + ".txt")) - 1
                    if 'MAC' in open("/home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt").read():
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/PORT/{flag=1;next}/MAC/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                    else:
                        Ports = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/PortScan-" + ActiveIPs[i] + ".txt | awk '/PORT/{flag=1;next}/Nmap/{flag=0}flag'"],
                                                         shell=True).decode('utf-8'))
                        print(Ports.strip())
                        print("-----------------------------------------------")
                else:
                    print('Port scan timeout', end="")
                    print("\n-----------------------------------------------")
    print(TotalUpHosts + "responsive hosts out of " + LANInfo[17] + " usable hosts ")
    print("-----------------------------------------------")


    # Print footer
    print("\n---------------------------------------------- \
    \nScan Complete - An export of this scan has been saved as " + filename + ". \
    \nTotal Scan Time: " + str(round(TimeTaken, 2)) + " Seconds \
    \n-----------------------------------------------")

    sys.stdout = sys.__stdout__

    output = (subprocess.check_output("cat " + filename,
                                      shell=True).decode('utf-8'))
    print(output)

    # Remove temp directory
    subprocess.run(["sudo rm -r /home/" + username + "/Documents/NetScanner/Temp"],
                   shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Execute Mode 5 (-hD)
def HOSTDISCOVERYONLY():
# Print header
    print("\nStarting NETSCANNER at " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')))
    time.sleep(1)
    print("\nDo not kill the program during this process, it may disable your network connection.")

# Create temp directory
    username = os.getlogin()
    tempDir = '/home/' + username + '/Documents/NetScanner/Temp'
    os.chdir(".")
    if os.path.isdir(tempDir):
        pass
    else:
        os.makedirs(tempDir)

# Get most active interface
    # Disables loopback interface
    subprocess.run(["sudo -S ifconfig lo down"],
                   shell=True, stderr=subprocess.DEVNULL)

    # Run ifconfig
    ifconf = (subprocess.check_output('ifconfig', shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))

    # Run ifconfig to gather interface names
    ifaces = (subprocess.check_output(r"ifconfig | sed 's/[ \t].*//;/^$/d'",
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    Interfaces = []
    Received = []
    Transmit = []

    # Stores interface names into list
    for line in ifaces.splitlines():
        Interfaces.append(line)

    # Stores RX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("RX packets"):
            RX = line.strip().split(" ")[2]
            Received.append(int(RX))

    # Stores TX packet values into list
    for line in ifconf.splitlines():
        if line.strip().startswith("TX packets"):
            TX = line.strip().split(" ")[2]
            Transmit.append(int(TX))

    # Calculates index of most active interface
    getRXmax = max(Received)
    getTXmax = max(Transmit)
    maxRXindex = Received.index(getRXmax)
    maxTXindex = Transmit.index(getTXmax)
    if maxRXindex == maxTXindex:
        MAI = str(Interfaces[maxRXindex]).replace(':', '')
    else:
        print('Error: The most active interface cannot be determined.')
        sys.exit()

    # Re-enables loopback interface
    subprocess.run(["sudo -S ifconfig lo up"], shell=True, stderr=subprocess.DEVNULL)

# Get local interface info + append to list
    LANInfo = []

    # Get MAI MAC
    MAC = (subprocess.check_output(["ifconfig " + MAI + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    MAC = MAC.upper()
    LANInfo.append(MAC.strip())


    # Get MAI NIC Vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError

    try:
        HostMAC = MacLookup().lookup(MAC.strip())
    except (InvalidMacError, VendorNotFoundError):
        HostMAC = "Unknown"

    # Get MAI IP
    IP = (subprocess.check_output(["ifconfig " + MAI + r" | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(IP.strip())

    # Get MAI subnet mask
    SubMask = (subprocess.check_output(["ifconfig " + MAI + " | grep -w inet | awk '{print $4}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    LANInfo.append(SubMask.strip())

    # Get data exchanged in MB
    RXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'RX packets' | awk '{printf $6}{print $7}'"],
                                   shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXMB = re.sub("[()]","", RXMB)
    LANInfo.append(RXMB.strip())
    TXMB = (subprocess.check_output(["ifconfig " + MAI + " | grep 'TX packets' | awk '{printf $6}{print $7}'"],
                                shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TXMB = re.sub("[()]","", TXMB)
    LANInfo.append(TXMB.strip())

    # Calculate CIDR
    if SubMask == '128.0.0.0':
        CIDR = '/1'
        UsableHosts = '2,147,483,646'
    elif LANInfo[2] == '192.0.0.0':
        CIDR = '/2'
        UsableHosts = '1,073,741,822'
    elif LANInfo[2] == '224.0.0.0':
        CIDR = '/3'
        UsableHosts = '536,870,910'
    elif LANInfo[2] == '240.0.0.0':
        CIDR = '/4'
        UsableHosts = '268,435,454'
    elif LANInfo[2] == '248.0.0.0':
        CIDR = '/5'
        UsableHosts = '134,217,726'
    elif LANInfo[2] == '252.0.0.0':
        CIDR = '/6'
        UsableHosts = '67,108,862'
    elif LANInfo[2] == '254.0.0.0':
        CIDR = '/7'
        UsableHosts = '33,554,430'
    elif LANInfo[2] == '255.0.0.0':
        CIDR = '/8'
        UsableHosts = '16,777,214'
    elif LANInfo[2] == '255.128.0.0':
        CIDR = '/9'
        UsableHosts = '8,388,606'
    elif LANInfo[2] == '255.192.0.0':
        CIDR = '/10'
        UsableHosts = '4,194,302'
    elif LANInfo[2] == '255.224.0.0':
        CIDR = '/11'
        UsableHosts = '2,097,150'
    elif LANInfo[2] == '255.240.0.0':
        CIDR = '/12'
        UsableHosts = '1,048,574'
    elif LANInfo[2] == '255.248.0.0':
        CIDR = '/13'
        UsableHosts = '524,286'
    elif LANInfo[2] == '255.252.0.0':
        CIDR = '/14'
        UsableHosts = '262,142'
    elif LANInfo[2] == '255.254.0.0':
        CIDR = '/15'
        UsableHosts = '131,070'
    elif LANInfo[2] == '255.255.0.0':
        CIDR = '/16'
        UsableHosts = '65,534'
    elif LANInfo[2] == '255.255.128.0':
        CIDR = '/17'
        UsableHosts = '32,766'
    elif LANInfo[2] == '255.255.192.0':
        CIDR = '/18'
        UsableHosts = '16,382'
    elif LANInfo[2] == '255.255.224.0':
        CIDR = '/19'
        UsableHosts = '8,190'
    elif LANInfo[2] == '255.255.240.0':
        CIDR = '/20'
        UsableHosts = '4,094'
    elif LANInfo[2] == '255.255.248.0':
        CIDR = '/21'
        UsableHosts = '2,046'
    elif LANInfo[2] == '255.255.252.0':
        CIDR = '/22'
        UsableHosts = '1,022'
    elif LANInfo[2] == '255.255.254.0':
        CIDR = '/23'
        UsableHosts = '510'
    elif LANInfo[2] == '255.255.255.0':
        CIDR = '/24'
        UsableHosts = '254'
    elif LANInfo[2] == '255.255.255.128':
        CIDR = '/25'
        UsableHosts = '126'
    elif LANInfo[2] == '255.255.255.192':
        CIDR = '/26'
        UsableHosts = '62'
    elif LANInfo[2] == '255.255.255.224':
        CIDR = '/27'
        UsableHosts = '30'
    elif LANInfo[2] == '255.255.255.240':
        CIDR = '/28'
        UsableHosts = '14'
    elif LANInfo[2] == '255.255.255.248':
        CIDR = '/29'
        UsableHosts = '6'
    elif LANInfo[2] == '255.255.255.252':
        CIDR = '/30'
        UsableHosts = '2'
    elif LANInfo[2] == '255.255.255.254':
        CIDR = '/31'
        UsableHosts = '0'
    elif LANInfo[2] == '255.255.255.255':
        CIDR = '/32'
        UsableHosts = '0'
    else:
        print("\nError: This program requires a valid network connection to operate. Please check your settings and "
              "try again")
        sys.exit()
    LANInfo.append(CIDR.strip())

# Calculate network address
    # Convert subnet mask to binary
    BinNetAddr = []
    BinMask = '.'.join([bin(int(x)+256)[3:] for x in SubMask.split('.')])

    # Convert device ip to binary
    BinIP = '.'.join([bin(int(x)+256)[3:] for x in IP.split('.')])

    # Calculate network address in binary
    for i in range(len(BinMask)):
        if BinMask[i] == BinIP[i]:
            BinNetAddr.append(BinMask[i])
        else:
            BinNetAddr.append('0')

    # Convert binary network address to decimal
    BinNetAddr = ''.join(BinNetAddr)
    BinNetAddr = BinNetAddr.replace('.', '')
    FirstOctet = BinNetAddr[:8]
    SecondOctet = BinNetAddr[8:16]
    ThirdOctet = BinNetAddr[16:24]
    FourthOctet = BinNetAddr[24:32]
    FirstOctet = int(FirstOctet, 2)
    SecondOctet = int(SecondOctet, 2)
    ThirdOctet = int(ThirdOctet, 2)
    FourthOctet = int(FourthOctet, 2)

    # Arrange into dotted format.
    NetAddr = []
    NetAddr.append(str(FirstOctet))
    NetAddr.append(str(SecondOctet))
    NetAddr.append(str(ThirdOctet))
    NetAddr.append(str(FourthOctet))
    NetAddr = '.'.join(NetAddr)

    # Append network address to list
    LANInfo.append(NetAddr.strip())

    # Get link speeds
    TXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'txrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    RXLinkSp = (subprocess.check_output(["ethtool -S " + MAI + " | grep 'rxrate' | awk '{printf $2}'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    if TXLinkSp != '':
        TXLinkSp = float(TXLinkSp) / 1000000
        TXLinkSp = int(TXLinkSp)
        LANInfo.append(TXLinkSp)
    else:
        TXLinkSp = 'Unknown '
        LANInfo.append(TXLinkSp)

    if RXLinkSp != '':
        RXLinkSp = float(RXLinkSp) / 1000000
        RXLinkSp = int(RXLinkSp)
        LANInfo.append(RXLinkSp)
    else:
        RXLinkSp = 'Unknown '
        LANInfo.append(RXLinkSp)

    # Get WLAN info
    try:
        iwconf = (subprocess.check_output(["iwconfig " + MAI],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        # Get 802.11 protocol
        IEEEProt = (subprocess.check_output(["iwconfig " + MAI + " | grep 'IEEE' | awk '{printf $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(IEEEProt.strip())

        # Get associated ESSID
        ESSID = (subprocess.check_output(["iwconfig " + MAI + r" | grep ESSID | awk -F: '{print $2}' | sed 's/\"//g'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(ESSID.strip())

        # Get associated AP BSSID
        APMAC = (subprocess.check_output(["iwconfig " + MAI + " | grep 'Access Point' | awk '{print $6}'"],
                                         shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(APMAC.strip())

        # Get associated AP vendor
        from mac_vendor_lookup import MacLookup
        from mac_vendor_lookup import InvalidMacError
        from mac_vendor_lookup import VendorNotFoundError
        try:
            HostAPVendor = MacLookup().lookup(APMAC.strip())
            LANInfo.append(HostAPVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            HostAPVendor = "Unknown"
            LANInfo.append(HostAPVendor.strip())

        # Get operating frequency
        Freq = (subprocess.check_output(["iwconfig " + MAI + " | grep -o 'Frequency:.*GHz' | sed -e 's/[^0-9.]//g'"],
                                        shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(Freq.strip())

        # Get operating channel
        Channel = (subprocess.check_output(["iwlist " + MAI + " channel | grep 'Current Frequency' | awk '{printf $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Channel = Channel.replace(')', '')
        if Channel == '':
            Channel = "Channel not identified"
        else:
            pass
        LANInfo.append(Channel.strip())

        # Get link quality
        LinkQual = (subprocess.check_output(["iwconfig " + MAI + "| grep 'Signal level=' | awk '{print $4}' |  sed -e " 
                                                                 "'s/level=//'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        LANInfo.append(LinkQual.strip())
        if int(LinkQual) <= -80:
            Strength = "Poor"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= -55:
            Strength = "Good"
            LANInfo.append(str(Strength).strip())
        elif int(LinkQual) <= 0:
            Strength = "Excellent"
            LANInfo.append(str(Strength).strip())
    except subprocess.CalledProcessError:
        IEEEProt = "No wireless connection"
        LANInfo.append(IEEEProt.strip())
        ESSID = "N/A"
        LANInfo.append(ESSID.strip())
        APMAC = "N/A"
        LANInfo.append(APMAC.strip())
        APMACVendor = "N/A"
        LANInfo.append(APMACVendor.strip())
        Channel = "N/A"
        LANInfo.append(Channel.strip())
        Freq = "N/A "
        LANInfo.append(Freq.strip())
        LinkQual = "N/A "
        LANInfo.append(LinkQual.strip())
        Strength = " "
        LANInfo.append(Strength.strip())
    LANInfo.append(UsableHosts)
    LANInfo.append(HostMAC)

# Execute host discovery techniques
    # Execute Nmap ARP ping scan
    subprocess.run(["sudo -S nmap -PR -sn -T4 -n -oN /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Execute Nmap rDNS lookup scan
    subprocess.run(["sudo -S nmap -R -PR -sn -T5 -oN /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt " +
                    LANInfo[6] + LANInfo[5]],
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Retrieve required data from output
    # Retrieve total hosts
    ActiveIPs = []
    TotalUpHosts = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'Nmap done at' | awk '{print $14}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
    TotalUpHosts = TotalUpHosts.replace('(', '')
    TotalUpHosts = TotalUpHosts.replace('\n', ' ')

    # Retrieve host IP addresses from ARP Scan
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        IPAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        IPAddrs = IPAddrs.replace('\n', '')
        ActiveIPs.append(IPAddrs)

    # Retrieve hostnames from rDNS lookup
    ActiveHostnames = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Hostname = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/rDNS.txt "
                                             + "| grep 'Nmap scan report for' | awk 'NR==" + str(i) + "{print $5}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Hostname = Hostname.strip()
        Hostname = Hostname.replace('\n', '')
        try:
            IsChar = Hostname[0]
        except IndexError:
            IsChar = '1'
        if IsChar.isdigit() == True:
            Hostname = 'Unknown Hostname'
            ActiveHostnames.append(Hostname)
        elif IsChar.isdigit() == False:
            ActiveHostnames.append(Hostname)

    # Retrieve ARP reply latency from ARP Scan
    ResLatency = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        Latency = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                            + "| grep 'Host is up' | awk 'NR==" + str(i) + "{print $4}'"],
                                           shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        Latency = Latency.replace('(', '')
        Latency = Latency.replace('\n', '')
        ResLatency.append(Latency)

    # Retrieve host MAC address from ARP Scan
    ActiveMACAddr = []
    MACVendors = []
    Range = int(TotalUpHosts) + 1
    for i in range(1, Range):
        MACAddrs = (subprocess.check_output(["cat /home/" + username + "/Documents/NetScanner/Temp/ARPScan.txt "
                                             + "| grep 'MAC Address: ' | awk 'NR==" + str(i) + "{print $3}'"],
                                            shell=True, stderr=subprocess.DEVNULL).decode('utf-8'))
        MACAddrs = MACAddrs.replace('(', '')
        MACAddrs = MACAddrs.replace('\n', '')
        if MACAddrs == '':
            MACAddrs = 'Unknown'
            ActiveMACAddr.append(MACAddrs)
        else:
            ActiveMACAddr.append(MACAddrs)

    # Determine host NIC vendor
    from mac_vendor_lookup import MacLookup
    from mac_vendor_lookup import InvalidMacError
    from mac_vendor_lookup import VendorNotFoundError
    Range = int(TotalUpHosts)
    for i in range(0, Range):
        try:
            MACVendor = MacLookup().lookup(ActiveMACAddr[i].strip())
            MACVendors.append(MACVendor.strip())
        except (InvalidMacError, VendorNotFoundError):
            MACVendor = "Unknown"
            MACVendors.append(MACVendor.strip())

# Output data
    End = timeit.default_timer()
    TimeTaken = End - Start

    # Create output file
    filepath = "/home/" + username + "/Documents/NetScanner/"
    filename = filepath + str(datetime.datetime.now().astimezone().strftime('%d-%m-%Y_%H%M%S')) + '_Mode5.txt'
    sys.stdout = open(filename, 'w')

    # Print local interface details
    print(f"\
    \nNETSCANNER has completed on " + str(datetime.datetime.now().astimezone().strftime('%A %d %B %Y %H:%M:%S %Z')) + "\
    \n \
    \n=============================================== \
    \nDetected Local Host Network Characteristics \
    \n=============================================== \
    \nMost Active Interface: " + MAI + " \
    \nInterface MAC Address: " + str(LANInfo[0]) + " (" + str(LANInfo[18]) + ")\
    \nInterface IPv4 Address: " + str(LANInfo[1]) + " \
    \nNetwork: " + str(LANInfo[6]) + str(LANInfo[5]) + " \
    \nData Exchanged: Transmit: " + str(LANInfo[4]) + ", Received: " + str(LANInfo[3]) + " \
    \nLink Speed: Transmit: " + str(LANInfo[7]) + "Mbps, Receive: " + str(LANInfo[8]) + "Mbps \
    \nActive 802.11 Protocol: " + str(LANInfo[9]) + "\
    \nConnected ESSID: " + str(LANInfo[10]) + " \
    \nAssociated Access Point BSSID: " + str(LANInfo[11]) + " (" + str(LANInfo[12]) + ") \
    \nAccess Point Channel: " + str(LANInfo[14]))
    if (str(LANInfo[13])) == 'N/A':
        print("Operating Frequency: " + str(LANInfo[13]))
    else:
        print("Operating Frequency: " + str(LANInfo[13]) + "Ghz")
    if (str(LANInfo[15])) == 'N/A':
        print("Link Quality: " + str(LANInfo[15]))
    else:
        print("Link Quality: " + str(LANInfo[15]) + "dBm, " + str(LANInfo[16]))
    print("===============================================")

    # Print host details
    print("\n=============================================== \
        \nDiscovered Local Hosts: " + TotalUpHosts + " \
        \n===============================================")
    Range = int(TotalUpHosts)
    for i in range(Range):
        if ResLatency[i] == '':
            ResLatency[i] = 'Undetermined'
        else:
            pass
        print("Host " + ActiveIPs[i] + " (" + ActiveHostnames[i] + ") is up (" + ResLatency[i] + " latency)")
        print("MAC Address: " + ActiveMACAddr[i] + " (" + MACVendors[i] + ")")
        print("-----------------------------------------------")
    print(TotalUpHosts + "responsive hosts out of " + LANInfo[17] + " usable hosts ")
    print("-----------------------------------------------")

    # Print footer
    print("\n---------------------------------------------- \
    \nScan Complete - An export of this scan has been saved as " + filename + ". \
    \nTotal Scan Time: " + str(round(TimeTaken, 2)) + " Seconds \
    \n-----------------------------------------------")

    sys.stdout = sys.__stdout__

    output = (subprocess.check_output("cat " + filename,
                                      shell=True).decode('utf-8'))
    print(output)

    # Remove temp directory
    subprocess.run(["sudo rm -r /home/" + username + "/Documents/NetScanner/Temp"],
                   shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Run program
def RUN():
    print("\nPlease read the disclaimer before running this program.")
    time.sleep(1)
    print("\nYou have 10 seconds before the scan begins, press Ctrl+C to abort.")
    time.sleep(10)
    if args.nP:
        print('\nNO PORT SCAN SPECIFIED')
        time.sleep(1)
        NOPORTSCAN()
    elif args.w:
        print('\nWIRELESS SCAN ONLY SPECIFIED')
        time.sleep(1)
        WIRELESSONLY()
    elif args.l:
        print('\nLOCAL SCAN ONLY SPECIFIED')
        time.sleep(1)
        LOCALONLY()
    elif args.hD:
        print('\nHOST DISCOVERY ONLY SPECIFIED')
        time.sleep(1)
        HOSTDISCOVERYONLY()
    else:
        print('\nNO MODE SPECIFIED')
        time.sleep(1)
        MAIN()

RUN()