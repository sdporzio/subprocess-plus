# -*- coding: utf-8 -*-

def _Notifier(cmd,curr,tot,email):
    cmd += '; echo "Job \'%s\' has finished." | mail -s "Job %i of %i finished" "%s"' %(cmd,curr,tot,email)
    return cmd

def _Temp2Perm(temp,perm,name,start,end):
    temp.seek(0)
    perm.write('%s\n%s -> %s [Time: %s]\n' %(name,start,end,end-start))
    perm.write(temp.read())
    perm.write('\n')
    temp.close()
