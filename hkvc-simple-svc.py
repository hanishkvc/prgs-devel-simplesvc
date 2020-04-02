#!/usr/bin/env python3
# A Simple Source Version Control
# v20200328IST1114, HanishKVC
#

import os
import sys
import time


"""
The core context includes
    files: The list of source files being tracked
        This list variable is used only at runtime. The disk
        store for this is the srcsFile specified below.
    baseDir: the base directory containing the ssvc repository
        It is normally a hidden directory at the root dir of the 
        files being tracked.
    copyDir: this contains a copy of the last commited instance
        of all the files being tracked.
        It mirrors the directory structure of the original files
    diffDir: Contains the history of the changes till date
        This consists of commit messages and corresponding diff
        files for all the tracked files.
        The files are timestamp prefixed. Also the directory
        path of the files are specified as part of the file
        name itself.
    cacheDir: directory containing files that require to be
        commited.
        It mirrors the directory structure of the original files
    srcsFile: the list of source files being tracked
"""
me = {
        'files': [],
        'baseDir': ".simpsvc",
        'copyDir': ".simpsvc/copy",
        'diffDir': ".simpsvc/diff",
        'cacheDir': ".simpsvc/cache",
        'srcsFile': ".simpsvc/srcs"
        }
gsCOMMITMSG_FILESUFFIX = "commitmsg"
gsTimeStampFormat="%Y%m%d%H%M%S"


gDBGLVL = 10
DLVL_ALWAYS = 0
DLVL_ERROR = 1
DLVL_DEFAULT=gDBGLVL
DLVL_DBUG = 11
def dprint(sMsg, dbgLvl=DLVL_DEFAULT):
    """ Debug print, which prints the given string, only if the
        debug level specified for the string, is lower than the
        current system debug level.
        """
    if (dbgLvl < gDBGLVL):
        print(sMsg)


def _commit_op(me, sOp, ts, sMsg):
    """ Helper which can be used by the different operations to
        generate a commitmsg file in the diffDir.
        To be used by those operations which want to convey the
        running of the corresponding operation by the user for
        future reference.
        sOp : the operation, by convention specified in CAPS.
        """
    tFile = "{}-OP_{}-{}".format(ts, sOp, gsCOMMITMSG_FILESUFFIX)
    theFile = os.path.join(me['diffDir'], tFile)
    os.system("echo '{}' > {}".format(sMsg, theFile))


def do_init(me):
    """ The operation which has to be called first before doing
        any other operation wrt ssvc repositories.
        This creates the ssvc repository folder within the current
        working directory from which the ssvc command is called
        by the user.
        """
    os.mkdir(me['baseDir'])
    os.mkdir(me['copyDir'])
    os.mkdir(me['diffDir'])
    os.mkdir(me['cacheDir'])
    ts = time.strftime(gsTimeStampFormat)
    _commit_op(me, "INIT", ts, "Initialised SSVC repository today")


def do_save(me):
    """ Internal operation called by the program at the end to
        transfer the current runtime context to the disk store
        of the repository.
        """
    f = open(me['srcsFile'],"wt+")
    for l in me['files']:
        f.write(l)
        f.write("\n")


def do_load(me):
    """ Internal operation called by the program at the beginning
        to load the current runtime context from the disk store of
        the repository.
        """
    try:
        f = open(me['srcsFile'])
        for l in f:
            l = l.strip()
            me['files'].append(l)
    except FileNotFoundError:
        print("WARN:load:No simpsvc repo found")


def do_dump(me):
    """ User can use the dump operation to get the current runtime
        context of the program.
        Mainly useful for basic debugging purpose and not required
        from normal usage perspective.
        """
    print(me)


def ssvc_mkdir(me, sBasePath, sDirs):
    """ Helper mkdir logic, which creates not just the leaf dir
        but also all the intermediate directories if required.

        It duplicates the sDirs directory | path heirarchy in
        the sBasePath directory.

        NOTE: Normally used when copying something into copyDir
        or to the cacheDir. As these maintain the directory
        hierarchy of the tracked files, when copied into them.
        """
    cPath = sBasePath
    for cDir in sDirs.split(os.sep):
        cPath += (os.sep + cDir)
        try:
            os.mkdir(cPath)
        except FileExistsError:
            None
    return cPath


def _cp(srcFile, destPath):
    """ helper file copy logic, which translates to the underlying
        os file copy command.
        """
    return os.system("cp {} {}".format(srcFile, destPath))


def ssvc_cp(me, srcFile, sBaseSrcPath, sBaseDestPath):
    """ copy specified file from the specified source directory
        into a mirrored directory heirarchy in the specified
        destination folder.

        srcFile : the given file can also contain a relative
        path info as part of it. In which case it is copied
        to the same path within the specified destination dir.

        sBaseSrcPath : the source directory which contains the
        specified srcFile (including srcFile's relative path).

        sBaseDestPath : the destination directory.

        It is normally used to copy files either into cacheDir
        or to the copyDir of ssvc repository, based on whether
        it is a add operation or commit operation.
        """
    sDir = os.path.dirname(srcFile)
    destPath = os.path.join(sBaseDestPath, sDir)
    theSrcFile = os.path.join(sBaseSrcPath, srcFile)
    if _cp(theSrcFile, destPath) == 0:
        return True
    else:
        return False


def ssvc_fileexists_list(me, sBaseDir, lInFiles):
    """ Get list of files which exist in the given BaseDir from 
        the list of given files.
        """
    lOut = list(filter(lambda x: os.path.exists(os.path.join(sBaseDir, x)), lInFiles))
    return lOut


def do_add(me, sFile):
    """ The add operation of the ssvc repository.

        It adds the specified file to the runtime list of files
        that are tracked by ssvc, if its not already there.

        It inturn copies the file to cacheDir, so that it can
        be commited when requested later.
        TOTHINK: Should I generate a OP commit message.
        """
    if sFile in me['files']:
        print("INFO:add: [{}] already in repo".format(sFile))
    else:
        me['files'].append(sFile)
        print("INFO:add: [{}] new file being added to repo".format(sFile))
    #ts = time.strftime(gsTimeStampFormat)
    sDir = os.path.dirname(sFile)
    pathDest = ssvc_mkdir(me, me['cacheDir'], sDir)
    ssvc_cp(me, sFile, ".", me['cacheDir'])
    #sCommitMsg = 'Added file [{}]'.format(sFile)
    #_commit_op(me, "ADD", ts, sCommitMsg)


def _do_difffile(me, tCur, sOldBasePath, sNewBasePath, bInteractive=False):
    """ The helper logic which does the actual low level diff
        operation, using the systems diff command.

        Given the file to diff, and its old-copy path and the
        new-copy path, it compares the two versions of the file
        and returns true, if there is any difference between them.
        """
    bDiff = False
    tOld = os.path.join(sOldBasePath, tCur)
    tNew = os.path.join(sNewBasePath, tCur)
    diffOk = os.system("diff --unidirectional-new-file -ub {} {}".format(tOld, tNew))
    if diffOk != 0:
        if bInteractive:
            input("WARN:diff:Changes or Error?:{}\nPress any key to continue...".format(tCur))
        bDiff = True
    else:
        if bInteractive:
            input("INFO:diff:NoChange:{}\nPress any key to continue...".format(tCur))
    return bDiff


def do_diff(me, lFiles = me['files'], sMode = "LC-WD", bInteractive=False):
    """ The diff operation of ssvc.
        It will go throu all the files being tracked by ssvc and
        cross checks if 
        
        LC-WD i.e CopyDir & WorkingDir (default):
        the last commited copy of the file within ssvc (i.e copyDir) 
        and the copy in the users working dir

        CA-WD i.e CacheDir & WorkingDir:
        the copy of the file within ssvc's cacheDir and the copy
        in the users working dir
        
        LC-CA i.e CopyDir & CacheDir:
        the last commited copy of the file within ssvc (i.e copyDir) 
        and the copy of the file within ssvc's cacheDir and the copy

        match or else show what is the difference.

        If oldBase is cacheDir, then the given file list is filtered
        to cross check that those files actually exist in cacheDir.
        Parallely if there are no files in cacheDir, then automatically
        switch to testing between copyDir and working dir.
        """
    # Setup paths
    if sMode == "CA-WD":
        oldBase = me['cacheDir']
        newBase = "."
    elif sMode == "LC-CA":
        oldBase = me['copyDir']
        newBase = me['cacheDir']
    elif sMode == "LC-WD":
        oldBase = me['copyDir']
        newBase = "."
    else:
        return
    # Cross check files exist, if oldBase is cacheDir
    if oldBase == me['cacheDir']:
        tlFiles = ssvc_fileexists_list(me, oldBase, lFiles)
        if len(tlFiles) != 0:
            lFiles = tlFiles
        else:
            input("INFO:diff:Change from cacheDir to copyDir, Press any key...")
            oldBase = me['copyDir']
    # Do the logic
    bDiffs = False
    for tCur in lFiles:
        if _do_difffile(me, tCur, oldBase, newBase, bInteractive):
            bDiffs = True
    return bDiffs


def _commit_filediff(me, ts, tCur):
    """ file diff helper for commit command
        It generates the diff file for the specified file, which
            relates to this commit.
            The same is copied into the diffDir.
            NOTE: The diffDir follows a flattened directory approach.
            i.e there are no sub directories to mirror the working 
            directory structure of the file. Instead the file path 
            is stored as part of the file name itself by prefixing
            it to the actual file name (dir seperator is replaced
            with ^ for now).
        It also tells if there was a diff/change wrt the file
            being looked at, in the working directory or else
            if the working and last commited copy are the same.
            If there is a change it returns True
        me: the context
        ts: the time stamp to use
        tCur: the file (including the path) being looked at.
        """
    tOld = os.path.join(me['copyDir'], tCur)
    tNew = os.path.join(me['cacheDir'], tCur)
    tDiffFN = "{}-{}".format(ts,tCur.replace(os.sep,"^"))
    tDiff = os.path.join(me['diffDir'], tDiffFN)
    res = os.system("diff --unidirectional-new-file -ub {} {} > {}".format(tOld, tNew, tDiff))
    if res != 0:
        #print("DBUG:_commit_filediff: diff of {} says {}".format(tCur, res))
        return True
    if os.path.getsize(tDiff) == 0:
        os.remove(tDiff)
    return False


def _commit_filecopy(me,tCur):
    """ file copy helper for commit command.
        It copies the current version of the specified file in
        the working directory into the copyDir of ssvc. Thus
        making it the last commited copy of that file from ssvc
        perspective.
        """
    if ssvc_cp(me, tCur, me['cacheDir'], me['copyDir']):
        os.remove(os.path.join(me['cacheDir'], tCur))
    else:
        input("ERRR:commit:filecopy: failed for [%s]" %(tCur))


def _commit_fileexists_list(me, lIn):
    #lOut = []
    #for f in lIn:
    #    sFile = os.path.join(me['cacheDir'], f)
    #    if os.path.exists(sFile):
    #        lOut.append(f)
    #return lOut
    return ssvc_fileexists_list(me, me['cacheDir'], lIn)


def do_commit(me):
    """ The commit command | operation of ssvc.
        It goes throu all the tracked files in ssvc, which have
        been added to the cache dir and cross checks if there 
        is any difference or not.

        If any differences are found then
        1. user is asked to provide a commit message
        2. the differences of the tracked files are captured 
           into the diffDir folder.
        3. the current working directory version of the changed
           files are backed up into copyDir, making them the
           last commited copy for those files.
        """
    #lFiles = list(map(lambda x: os.path.join(me['cacheDir'], x), me['files']))
    #lFiles = list(filter(os.path.exists, lFiles))
    lFiles = _commit_fileexists_list(me, me['files'])
    print(lFiles)
    if not do_diff(me, lFiles, "LC-CA", bInteractive=True):
        print("WARN:commit: No changes identified, so skipping commit...")
        return
    ts = time.strftime(gsTimeStampFormat)
    fnCommitMsg = "/tmp/{}-{}".format(ts, gsCOMMITMSG_FILESUFFIX)
    os.system("vim {}".format(fnCommitMsg))
    cmSize = os.path.getsize(fnCommitMsg)
    if (cmSize < 5):
        print("WARN:commit: Skipping commit bcas No commit msg")
        return
    else:
        os.system("cp {} {}".format(fnCommitMsg, me['diffDir']))
    for tCur in lFiles:
        if _commit_filediff(me, ts, tCur):
            _commit_filecopy(me, tCur)


def sort_diffDir(lIn):
    """ helper logic to sort the list of file names given according
        to ssvc convention for diffDir log output.
        When one is viewing the details of all the commits done till
        date or a given subset of commits or a specific commit,
        one will ideally want to look at the commit message first 
        followed by the contents of the tracked files which changed
        as part of that commit. This helper logic helps sort the
        list of file names, to achieve this goal.
        i.e For any given commit, it puts the commitmsg file first
        followed by the files which form part of that commit.
        """
    lOut = []
    lTmp = []
    sTmpCMsg = None
    sPrevTS = ""
    for l in lIn:
        sCurTS = l.split('-')[0]
        if sCurTS != sPrevTS:
            if sTmpCMsg != None:
                lOut.append(sTmpCMsg)
                sTmpCMsg = None
                for m in lTmp:
                    lOut.append(m)
                lTmp = []
            sPrevTS = sCurTS
        if l.endswith(gsCOMMITMSG_FILESUFFIX):
            sTmpCMsg = l
        else:
            lTmp.append(l)
    if sTmpCMsg != None:
        lOut.append(sTmpCMsg)
    for m in lTmp:
        lOut.append(m)
    lenIn = len(lIn)
    lenOut = len(lOut)
    if (lenIn != lenOut):
        dprint("DBUG:sort_diffdir: size of given {} & sorted {} list dont match".format(lenIn, lenOut), DLVL_ERROR)
        exit()
    for i in range(lenIn):
        dprint("DBUG:sort_diffdir:{:50}, {:50}".format(lIn[i], lOut[i]), DLVL_DBUG)
    return lOut


def _cat(sFile, sHeader = None, bLess=False):
    if sHeader != None:
        print(sHeader)
    f = open(sFile)
    i = 0
    for l in f:
        print(l, end="")
        if bLess and ((i%25) == 0):
            input("Press any key...")


def do_log(me, bPatch=False, bLess=False):
    """ Generate a log of all commits till date.
        By default it only contains the contents of the commit messages.
        However by specifying bPatch as True, one can also include the
        contents of the files associated with the commits.
        NOTE1: commit command stores diffs of files in diffDir
               add command stores content of new file in diffDir
        NOTE2: This logic iterates through contents of diffDir, in a
               sorted manner.
        """
    lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
    lFiles = sort_diffDir(lFiles)
    for tFile in lFiles:
        bPrint = False
        sType = "NOTME_FIXME"
        if bPatch:
            sType = "diff"
            bPrint = True
        if tFile.endswith(gsCOMMITMSG_FILESUFFIX):
            sType = "log"
            bPrint = True
        if bPrint:
            theFile = os.path.join(me['diffDir'], tFile)
            #print("\n\nINFO:log: #### {} #### \n".format(tFile))
            sPrefix = "\n\nINFO:{}: #### {} #### \n".format(sType, tFile)
            _cat(theFile, sPrefix, bLess)


def do_edit(me, index):
    """ Edit index specified commit message 

        index starts from 0, with 
        0 being the latest commit,
        1 being the previous-to-latest commit 
        and so on.
    
        One can even use -ve index. In which case 
        -1 is oldest (i.e 1st) commit, 
        -2 is one-after-oldest (2nd) commit
        and so on.
        """
    lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
    dprint(lFiles)
    lFiles = list(filter(lambda x: x.endswith(gsCOMMITMSG_FILESUFFIX), lFiles))
    dprint(lFiles)
    try:
        theFile = os.path.join(me['diffDir'], lFiles[index])
        os.system("vim {}".format(theFile))
    except IndexError:
        print("WARN:edit: specify a valid index")


def peek_ingroup(grp, index):
    """ Helper to get item at a specified location in a given list.
        If the specified location is invalid, then returns None
        NOTE: This avoids raising a exception if the index is invalid.
        """
    if index >= len(grp):
        return None
    return grp[index]


def diff_args(sArg, iArg):
    if (sArg == None):
        sArg = "CA-WD"
    elif sArg.startswith("--"):
        sArg = sArg[2:]
        if (sArg == "cached"):
            sArg = "LC-CA"
        elif (sArg == "commit"):
            sArg = "LC-WD"
        iArg += 1
    else:
        sArg = "CA-WD"
    return sArg, iArg


def process_args(args):
    """ Logic to process the arguments passed to the ssvc program
        """
    iArg = 0
    while iArg < len(args):
        if args[iArg] == "init":
            do_init(me)
            iArg += 1
        elif args[iArg] == "add":
            # requires 1 additional argument
            do_add(me, args[iArg+1])
            iArg += 2
        elif args[iArg] == "diff":
            # can have 1 optional argument
            sArg = peek_ingroup(args, iArg+1)
            sArg, iArg = diff_args(sArg, iArg)
            do_diff(me, sMode=sArg)
            iArg += 1
        elif args[iArg] == "dump":
            do_dump(me)
            iArg += 1
        elif args[iArg] == "commit":
            do_commit(me)
            iArg += 1
        elif args[iArg] == "log":
            # can have 1 optional argument
            if peek_ingroup(args, iArg+1) == "--patch":
                bPatch=True
                iArg += 1
            else:
                bPatch=False
            do_log(me,bPatch)
            iArg += 1
        elif args[iArg] == "editcmsg":
            # this command consumes 1 adjacent arg, if any,
            # irrespective of whether it is related or not
            sOffset = peek_ingroup(args, iArg+1)
            if (sOffset == None):
                iOffset = 0
            elif sOffset[0].isalpha():
                iOffset = 0
            else:
                iOffset = int(sOffset)
            do_edit(me, iOffset)
            iArg += 2
        else:
            print("WARN: Skipping unknown arg[{}]".format(args[iArg]))
            iArg += 1


if len(sys.argv) == 1:
    print("{}, v20200401IST2117, HanishKVC".format(sys.argv[0]))
    print("usage: ssvc [<cmd> [args]] [<cmd> [args]]...")
    print("\t the <cmd> can be one of init|dump|add|diff|commit|log")
    print("\t rare <cmd>'s are editcmsg")
    print("\t optional args")
    print("\t <log> --patch : also print the patchs associated with each commit")
    print("\t <diff> --CA-WD(default) : print diff between cache dir and working dir")
    print("\t <diff> --LC-WD|--commit : print diff between last commit and working dir")
    print("\t <diff> --LC-CA|--cached : print diff between last commit and cache dir")
    exit()


# Load the context from disk
do_load(me)
# Process the given arguments
process_args(sys.argv[1:])
# Save the context to disk
do_save(me)

