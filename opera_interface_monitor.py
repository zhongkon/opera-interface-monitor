import cx_Oracle
import requests
import sys

def send_line(msg,token):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url, headers=headers , data = {'message':msg})
    #print (r.text)

try:
    con = cx_Oracle.connect('opera/opera@192.168.0.157/opera')
    #print(con.version)
    cur = con.cursor()

except cx_Oracle.DatabaseError as e:
    errorObj, = e.args
    send_line(errorObj.message,'youre token hear')
    sys.exit()
    
try:
    #cur = con.cursor()
    cur.execute('SELECT OPERA.IFC_CTRL.NAME,OPERA.IFC_CTRL.ACTIVE,OPERA.IFC_CTRL.IFC_STATUS FROM OPERA.IFC_CTRL WHERE OPERA.IFC_CTRL.ACTIVE = 1')
    for result in cur:
        #print(result[2])
            if result[2] == 'STOPPED':
                send_line(result[0] +' has been ' + result[2],'Your token hear')
    cur.close()
    con.close()
except cx_Oracle.DatabaseError as e:
    errorObj, = e.args
    send_line(errorObj.message,'Your token hear')
