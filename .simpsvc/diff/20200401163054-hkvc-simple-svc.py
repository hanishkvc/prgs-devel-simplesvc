--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 15:50:38.373492924 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 16:30:41.807543782 +0530
@@ -135,10 +135,10 @@
     """ helper file copy logic, which translates to the underlying
         os file copy command.
         """
-    os.system("cp {} {}".format(srcFile, destPath))
+    return os.system("cp {} {}".format(srcFile, destPath))
 
 
-def ssvc_cp(me, srcFile, sBaseDestPath):
+def ssvc_cp(me, srcFile, sBaseSrcPath, sBaseDestPath):
     """ copy specified file into a mirrored directory heirarchy
         in the specified folder.
         It is normally used to copy files either into cacheDir
@@ -147,7 +147,11 @@
         """
     sDir = os.path.dirname(srcFile)
     destPath = os.path.join(sBaseDestPath, sDir)
-    _cp(srcFile, destPath)
+    theSrcFile = os.path.join(sBaseSrcPath, srcFile)
+    if _cp(theSrcFile, destPath) == 0:
+        return True
+    else:
+        return False
 
 
 def do_add(me, sFile):
@@ -169,12 +173,12 @@
     # and filediff wont be able to generate the diff file
     sDir = os.path.dirname(sFile)
     pathDest = ssvc_mkdir(me, me['cacheDir'], sDir)
-    ssvc_cp(me, sFile, me['cacheDir'])
+    ssvc_cp(me, sFile, ".", me['cacheDir'])
     #sCommitMsg = 'Added file [{}]'.format(sFile)
     #_commit_op(me, "ADD", ts, sCommitMsg)
 
 
-def _do_diff(me, tCur, sOldBasePath, sNewBasePath, bInteractive=False):
+def _do_difffile(me, tCur, sOldBasePath, sNewBasePath, bInteractive=False):
     """ The helper logic which does the actual low level diff
         operation, using the systems diff command.
         Given the file to diff, it automatically identifies the
@@ -195,7 +199,7 @@
     return bDiff
 
 
-def do_diff(me, sMode = "LC-WD", bInteractive=False):
+def do_diff(me, lFiles = me['files'], sMode = "LC-WD", bInteractive=False):
     """ The diff operation of ssvc.
         It will go throu all the files being tracked by ssvc and
         cross checks if 
@@ -228,8 +232,8 @@
         return
     # Do the logic
     bDiffs = False
-    for tCur in me['files']:
-        if _do_diff(me, tCur, oldBase, newBase, bInteractive):
+    for tCur in lFiles:
+        if _do_difffile(me, tCur, oldBase, newBase, bInteractive):
             bDiffs = True
     return bDiffs
 
@@ -254,9 +258,10 @@
         tCur: the file (including the path) being looked at.
         """
     tOld = os.path.join(me['copyDir'], tCur)
+    tNew = os.path.join(me['cacheDir'], tCur)
     tDiffFN = "{}-{}".format(ts,tCur.replace(os.sep,"^"))
     tDiff = os.path.join(me['diffDir'], tDiffFN)
-    res = os.system("diff --unidirectional-new-file -ub {} {} > {}".format(tOld, tCur, tDiff))
+    res = os.system("diff --unidirectional-new-file -ub {} {} > {}".format(tOld, tNew, tDiff))
     if res != 0:
         #print("DBUG:_commit_filediff: diff of {} says {}".format(tCur, res))
         return True
@@ -272,7 +277,19 @@
         making it the last commited copy of that file from ssvc
         perspective.
         """
-    ssvccopy_cp(me, tCur)
+    if ssvc_cp(me, tCur, me['cacheDir'], me['copyDir']):
+        os.remove(os.path.join(me['cacheDir'], tCur))
+    else:
+        input("ERRR:commit:filecopy: failed for [%s]" %(tCur))
+
+
+def _commit_fileexists_list(me, lIn):
+    lOut = []
+    for f in lIn:
+        sFile = os.path.join(me['cacheDir'], f)
+        if os.path.exists(sFile):
+            lOut.append(f)
+    return lOut
 
 
 def do_commit(me):
@@ -289,12 +306,11 @@
            files are backed up into copyDir, making them the
            last commited copy for those files.
         """
-    lFiles = list(map(lambda x: os.path.join(me['cacheDir'], x), me['files']))
-    print(lFiles)
-    lFiles = list(filter(os.path.exists, lFiles))
+    #lFiles = list(map(lambda x: os.path.join(me['cacheDir'], x), me['files']))
+    #lFiles = list(filter(os.path.exists, lFiles))
+    lFiles = _commit_fileexists_list(me, me['files'])
     print(lFiles)
-    exit()
-    if not do_diff(me, bInteractive=True):
+    if not do_diff(me, lFiles, "LC-CA", bInteractive=True):
         print("WARN:commit: No changes identified, so skipping commit...")
         return
     ts = time.strftime(gsTimeStampFormat)
@@ -306,7 +322,7 @@
         return
     else:
         os.system("cp {} {}".format(fnCommitMsg, me['diffDir']))
-    for tCur in me['files']:
+    for tCur in lFiles:
         if _commit_filediff(me, ts, tCur):
             _commit_filecopy(me, tCur)
 
