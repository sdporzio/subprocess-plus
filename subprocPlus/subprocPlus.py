# -*- coding: utf-8 -*-

import os
import datetime
from subprocess import call, Popen
from __sample.__sample import _Notifier, _Temp2Perm

firstRun = True
procs = []

def ProcSeries(cmd,i,njobs,email=False,inName='logIn.log',outName='logOut.log',errName='logErr.log'):
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
    print '\033[1;33m-> %s\033[0m [%i of %i]' %(cmd,i+1,njobs)
    start = datetime.datetime.now()
    if email==False:
        proc = call(cmd,shell=True,stdin=inl,stdout=outl,stderr=errl)
    else:
        proc = call(_Notifier(cmd,i+1,njobs,email),shell=True,stdin=inl,stdout=outl,stderr=errl)
    end = datetime.datetime.now()
    print 'Process %i of %i completed. Time: %s' %(i+1,njobs,end-start)
    _Temp2Perm(inl,logIn,cmd,start,end)
    _Temp2Perm(outl,logOut,cmd,start,end)
    if errl.tell() != 0:
        _Temp2Perm(errl,logErr,cmd,start,end)
    if i==njobs-1:
        firstRun = True



def ProcParallel(cmd,i,njobs,email=False,inName='logIn.log',outName='logOut.log',errName='logErr.log'):
    global firstRun
    global procs
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
    print '\033[1;33m-> %s\033[0m [%i of %i]' %(cmd,i+1,njobs)
    start = datetime.datetime.now()
    if email==False:
        proc = Popen(cmd,shell=True,stdin=inl,stdout=outl,stderr=errl)
    else:
        proc = Popen(_Notifier(cmd,i+1,njobs,email),shell=True,stdin=inl,stdout=outl,stderr=errl)
    procs.append((start,cmd,proc,inl,outl,errl))

    if i==njobs-1:
        for j, (start, name, proc, inl, outl, errl) in enumerate(procs):
            proc.wait()
            end = datetime.datetime.now()
            print 'Process %i of %i completed. Time: %s' %(j+1,njobs,end-start)
            _Temp2Perm(inl,logIn,name,start,end)
            _Temp2Perm(outl,logOut,name,start,end)
            if errl.tell() != 0:
                _Temp2Perm(errl,logErr,cmd,start,end)
        firstRun = True
        procs = []
