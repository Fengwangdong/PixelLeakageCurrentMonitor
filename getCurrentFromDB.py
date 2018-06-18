#!/bin/env python
import sqlite3 as sql
import cx_Oracle
import datetime

connection = cx_Oracle.connect('cms_trk_r/1A3C5E7G:FIN@cms_omds_adg')
cursor = connection.cursor()

start_time = "2018-06-11 20:45:00"
stop_time = "2018-06-11 22:30:00"

option = "PixelBarrel"
#query = "select dpe_name, alias, id from cms_trk_dcs_pvss_cond.aliases join cms_trk_dcs_pvss_cond.dp_name2id on (dpname || '.' = dpe_name) where alias like '%%/%s'" % (option + "%%channel%%")

query = """select distinct substr(lal.alias,INSTR(lal.alias,  '/', -1, 2)+1), id, lal.dpe_name, cd from
    (select max(since) as cd, alias from  cms_trk_dcs_pvss_cond.aliases group by alias) md, cms_trk_dcs_pvss_cond.aliases lal
    join cms_trk_dcs_pvss_cond.dp_name2id on dpe_name=concat(dpname,'.')
    where md.alias=lal.alias and lal.since=cd
    and (lal.alias like '%%/%s')""" % (option + "%%channel%%")

print "start executing query 1..."
cursor.execute(query)
dpid_rows = cursor.fetchall()
print "finish query 1 execution!"

outputFile = "currentsFromDB.txt"
fcur = open(outputFile, "w+")

for k in xrange(len(dpid_rows)):
    query2 = """select actual_Imon, change_date from cms_trk_dcs_pvss_cond.fwcaenchannel
    where change_date between TO_TIMESTAMP('%s', 'RRRR-MM-DD HH24:MI:SS.FF') and TO_TIMESTAMP('%s', 'RRRR-MM-DD HH24:MI:SS.FF')
    and dpid='%s' and actual_Imon is not NULL
            order by change_date""" % (start_time, stop_time, dpid_rows[k][1])

    print "executing query 2..."
    cursor.execute(query2)
    result = cursor.fetchall()
    print "finish query 2 execution!"
    print "writing output..."

    dpid = str(dpid_rows[k][0])

    if len(result) > 0:

        if ("channel000" in dpid) or ("channel001" in dpid):
            continue

        if ("LAY14" in dpid) or ("LAY23" in dpid):
            continue

        else:
            recordValue = result[0][0]
            fcur.write(dpid + "   " + str(result[0][0]) + "   " + str(result[0][1]) + "\n")

    for i in xrange(len(result)):

        if ("channel000" in dpid) or ("channel001" in dpid):
            continue

        if ("LAY14" in dpid) or ("LAY23" in dpid):
            continue

        if (abs(recordValue - result[i][0]) <= 3.0):
            continue

        else:
            recordValue = result[i][0]
            fcur.write(dpid + "   " + str(result[i][0]) + "   " + str(result[i][1]) + "\n")

print "finish output!"

fcur.close()
connection.close()
