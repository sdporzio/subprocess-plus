import os
import datetime
import numpy as np
from subprocess import call, Popen

firstRun = True

def Notifier(cmd,curr,tot,email):
    """ Append at the end of the command, an extra command to notify the user by mail when the job has finished. """
    cmd += '; echo "Job \'%s\' has finished." | mail -s "Job %i of %i finished" "%s"' %(cmd,curr,tot,email)
    return cmd

def Temp2Perm(temp,perm,name,start,end):
    """ Saves temporary (temp) log files in permanent (perm) log files. """
    temp.seek(0)
    perm.write('%s\n%s -> %s\n' %(name,start,end))
    perm.write(temp.read())
    perm.write('\n')
    temp.close()

def FancySeries(cmd,i,njobs,email=False,inName='logIn.log',outName='logOut.log',errName='logErr.log'):
    """ Runs a series of jobs in series.

    Parameters
    ----------
    cmd : string
        The command to execute.
    i : int
        The looping index of the current job
    njobs : int
        The number of jobs to execute.
    email : bool or string, optional (default=False)
        The email address of the user at which the notification that the job has ended is sent.
    inName : string
        The name of the log file containing the stdIn.
    outName : string
        The name of the log file containing the stdOut.
    errName : string
        The name of the log file containing the stdErr.
    """

    global firstRun
    if firstRun:
        logIn = open(inName, 'w')
        logOut = open(outName, 'w')
        logErr = open(errName, 'w')
        firstRun = False
    else:
        logIn = open(inName, 'a')
        logOut = open(outName, 'a')
        logErr = open(errName, 'a')

    inl = os.tmpfile()
    outl = os.tmpfile()
    errl = os.tmpfile()
    print '\033[1;33m-> %s\033[0m' %(cmd)
    start = datetime.datetime.now()
    if email==False:
        proc = call(cmd,shell=True,stdin=inl,stdout=outl,stderr=errl)
    else:
        proc = call(Notifier(cmd,i+1,njobs,email),shell=True,stdin=inl,stdout=outl,stderr=errl)
    end = datetime.datetime.now()
    print 'Process %i of %i completed. Time: %s' %(i+1,njobs,end-start)
    Temp2Perm(inl,logIn,cmd,start,end)
    Temp2Perm(outl,logOut,cmd,start,end)
    Temp2Perm(errl,logErr,cmd,start,end)

def FancyParallel(cmd,i,njobs,procs,email=False,inName='logIn.log',outName='logOut.log',errName='logErr.log'):
    """ Runs a series of jobs in parallel.

    Parameters
    ----------
    cmd : string
        The command to execute.
    i : int
        The looping index of the current job
    njobs : int
        The number of jobs to execute.
    procs : array
        The array containing all the informations to be processed at the end of the jobs
        (necessary to maintain the correct order in the log files).
    email : bool or string, optional (default=False)
        The email address of the user at which the notification that the job has ended is sent.
    inName : string
        The name of the log file containing the stdIn.
    outName : string
        The name of the log file containing the stdOut.
    errName : string
        The name of the log file containing the stdErr.
    """
    global firstRun
    if firstRun:
        logIn = open(inName, 'w')
        logOut = open(outName, 'w')
        logErr = open(errName, 'w')
        firstRun = False
    else:
        logIn = open(inName, 'a')
        logOut = open(outName, 'a')
        logErr = open(errName, 'a')

    inl = os.tmpfile()
    outl = os.tmpfile()
    errl = os.tmpfile()
    start = datetime.datetime.now()
    if email==False:
        proc = Popen(cmd,shell=True,stdin=inl,stdout=outl,stderr=errl)
    else:
        proc = Popen(Notifier(cmd,i+1,njobs,email),shell=True,stdin=inl,stdout=outl,stderr=errl)
    procs.append((start,cmd,proc,inl,outl,errl))

    if i==njobs-1:
        for start, name, proc, inl, outl, errl in procs:
            proc.wait()
            end = datetime.datetime.now()
            Temp2Perm(inl,logIn,name,start,end)
            Temp2Perm(outl,logOut,name,start,end)
            Temp2Perm(errl,logErr,name,start,end)
