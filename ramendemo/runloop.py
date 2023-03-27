#!/usr/bin/python
import json,sys,os,time,io,pyodbc,shortuuid
from subprocess import Popen, PIPE
from optparse import OptionParser
from random import seed
from random import randint
from time import sleep
from datetime import datetime

usage = "Usage: %prog -n jobname [-s sqlserver_address] [-f output_file]"
parser = OptionParser()
parser.add_option("-z", "--size", action="store_true",dest="blocksize",help="Block size to use for IOs",default=False)
parser.add_option("-s", "--server", action="store_true",dest="sqlserver",help="SQL server address is in SQL_SERVER environment variable",default=False)
parser.add_option("-p", "--port", action="store_true",dest="sqlport",help="SQL server port exposed through nodePort",default=False)
parser.add_option("-g", "--debug", action="store_true",dest="debugflag",help="Display debugging info",default=False)
parser.add_option("-f", "--file", action="store",dest="writetofile",help="Write output to file",default="/tmp/outfile")

global writetofile
global sqlserveraddress
global sqlport
global blocksize
global lastuuid
global last1
global last2
global sqlurl
global isprimarycluster
global issecondarycluster

(options, args) = parser.parse_args()

writetofile = options.writetofile
sqlurl=""
sqlport = ""
lastuuid = ""
last1 = 0
last2 = 0
isprimarycluster = 0
issecondarycluster = 0

if (options.blocksize == ""):
   printf("%s\n", usage)
   exit(1)

blocksize = options.blocksize

if (options.blocksize == True):
   blocksize = os.getenv('BLOCKSIZE')

if (options.sqlserver == True):
   sqlserveraddress = os.getenv('SQL_SERVER')

if (options.sqlport == True):
   sqlport = os.getenv('SQL_PORT')
   sqlserveraddress += ":"
   sqlserveraddress += sqlport
#
# See if for automation we are overriding the yaml environment variable
#
sqlurl = os.getenv('SQL_URL', 'ramendemo')
if sqlurl != "":
   print ("Overriding environment variable from URL content at "+sqlurl)
   tmpval = os.popen("curl "+sqlurl+" 2>/dev/null").read()
   if tmpval != "404: Not Found":
      sqlserveraddress = tmpval.strip()

print ("SQL Server Address = "+sqlserveraddress)

db = os.getenv('DB', 'ramendemo')
user = os.getenv('USER', 'root')
password = os.getenv('PASS', 'redhat')
myname = os.getenv('MYNAME', 'UNKNOWN')

conn = pyodbc.connect('Driver={MySQL ODBC 8.0 ANSI Driver};'
                      'Server='+sqlserveraddress+';'
                      'Database='+db+';'
                      'uid='+user+';'
                      'pwd='+password+';'
                      'Trusted_Connection=yes;')

conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
conn.setencoding(encoding='utf-8')

cursor = conn.cursor()
#sqlcmd = ("DROP TABLE IF EXISTS ramendemo;")
#cursor.execute(sqlcmd)
#
# Create the table to track the data we write
#
sqlcmd = ("CREATE TABLE IF NOT EXISTS ramendemo (id serial PRIMARY KEY, submit_time DATETIME, complete_time DATETIME, isprimary INT, issecondary INT, fsid VARCHAR(64), stampdate VARCHAR(8), stamptime VARCHAR(6), iosize VARCHAR(16));")
cursor.execute(sqlcmd)
conn.commit()
#
# Create the table to track the current fsid and the previous last stamp writtem
#
sqlcmd = ("CREATE TABLE IF NOT EXISTS ramenfsid (id serial PRIMARY KEY, submit_time DATETIME, cluster1 INT, cluster2 INT, fsid VARCHAR(64), prevdate VARCHAR(8), prevtime VARCHAR(6), gap VARCHAR(12));")
cursor.execute(sqlcmd)
#
# Retrieve the last fsid that was running prior to a failover or failback
#
#sqlcmd = ("SELECT * FROM ramendemo.ramenfsid WHERE id=(SELECT MAX(id) FROM ramendemo.ramenfsid);")
sqlcmd = ("SELECT * FROM ramendemo.ramenfsid;")
records = cursor.execute(sqlcmd).fetchall()
newramendemofsid = len(records)
#
# Check if table is empty (we are the first occurence of the pod)
#
if newramendemofsid != 0:
   print ("Table ramenfsid is NOT empty "+str(newramendemofsid))
   for r in records:
      print(str(r.id)+" "+str(r.fsid))
      lastuuid = str(r.fsid)
      last1 = int(r.cluster1)
      last2 = int(r.cluster2)
      print ("Saving "+str(lastuuid)+" for later C1="+str(last1)+" C2="+str(last2))
else:
   print ("Table ramenfsid is empty")
#
# Generate uuid for this new occurence
#
tmyuuid = os.popen("cat /proc/sys/kernel/random/uuid").read()
myuuid = tmyuuid.strip()
#
# Now check on disk what is the latest file we have from previous run time
#
tprevious = os.popen("ls -1 -t /mnt/test/file_"+lastuuid+"_* | head -1").read()
lastprevious = tprevious.strip()
print ("Current="+myuuid+" Previous run last file="+lastprevious)
#
# Insert one more row for current fsid
#
if newramendemofsid == 0:
   isprimarycluster = 1
   issecondarycluster = 0
   sqlcmd = ("INSERT INTO ramendemo.ramenfsid (id, submit_time, cluster1, cluster2, fsid, prevdate, prevtime, gap) VALUES (?, NOW(), 1, 0, ?, ?, ?, ?);")
   values = [ str((int(newramendemofsid) + 1)), str(myuuid), "", "", "None" ]
else:
#
# If last1 is non zero we failed over from Cluster1 to Cluster2
#
   if last1 == 1:
      isprimarycluster = 0
      issecondarycluster = 1
      sqlcmd = ("INSERT INTO ramendemo.ramenfsid (id, submit_time, cluster1, cluster2, fsid, prevdate, prevtime, gap) VALUES (?, NOW(), 0, 1, ?, ?, ?, ?);")
   else:
      isprimarycluster = 1
      issecondarycluster = 0
      sqlcmd = ("INSERT INTO ramendemo.ramenfsid (id, submit_time, cluster1, cluster2, fsid, prevdate, prevtime, gap) VALUES (?, NOW(), 1, 0, ?, ?, ?, ?);")
   workstring=lastprevious[-15:-7]+" "+lastprevious[-6:]
   previousrun=datetime.strptime(workstring, "%Y%m%d %H%M%S")
   currentrun=datetime.now()
   gap=currentrun - previousrun
   seconds = gap.total_seconds()
   hours = seconds // 3600
   minutes = (seconds % 3600) // 60
   seconds = seconds % 60
   formattedgap="{0:02.0f}:{1:02.0f}:{2:02.0f}".format(hours, minutes, seconds)

   values = [ str((int(newramendemofsid) + 1)), str(myuuid), lastprevious[-15:-7], lastprevious[-6:], formattedgap ]
cursor.execute(sqlcmd, values)
#
# Then loop until the pod if failed over or failed back
#
while True:
   tdatestamp = os.popen("date +%Y%m%d_%H%M%S").read()
   tfilenumber = os.popen("ls /mnt/test/file_* | wc -l").read()

   datestamp = tdatestamp.strip()
   filenumber = tfilenumber.strip()

   sqlcmd = ("INSERT INTO ramendemo.ramendemo (submit_time, isprimary, issecondary, fsid, stampdate, stamptime, iosize) VALUES (NOW(), ?, ?, ?, ?, ?, ?);")
   values = [ str(isprimarycluster), str(issecondarycluster), str(myuuid), datestamp[0:8], datestamp[-6:], str(blocksize) ]
   cursor.execute(sqlcmd, values)

   conn.commit()

   #cmd = "while true; do dd if=/dev/urandom of=/mnt/test/file_"+myuuid+"_"+datestamp+" bs="+blocksize+" count=1 oflag=direct &>/dev/null; echo "+str(int(filenumber) + 1)+","+blocksize+",/mnt/test/file_+"+myuuid+"_"+datestamp+" | tee -a "+writetofile+"; done"

   cmd = "dd if=/dev/urandom of=/mnt/test/file_"+myuuid+"_"+datestamp+" bs="+blocksize+" count=1 oflag=direct &>/dev/null; echo "+str(int(filenumber) + 1)+","+blocksize+",/mnt/test/file_+"+myuuid+"_"+datestamp+" | tee -a "+writetofile

   outputline = os.popen(cmd).read().strip()
   #print (outputline)

#   sqlcmd = ("UPDATE ramendemo SET complete_time = NOW() WHERE ID = ?;")
#   values = [ int(filenumber) + 1 ]
#   cursor.execute(sqlcmd, values)

   conn.commit()

