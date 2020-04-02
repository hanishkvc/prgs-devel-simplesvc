--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 09:59:19.782046888 +0530
+++ hkvc-simple-svc.py	2020-04-01 12:39:22.520250088 +0530
@@ -25,6 +25,8 @@
         The files are timestamp prefixed. Also the directory
         path of the files are specified as part of the file
         name itself.
+    cacheDir: directory containing files that require to be
+        commited.
     srcsFile: the list of source files being tracked
 """
 me = {
@@ -32,6 +34,7 @@
         'baseDir': ".simpsvc",
         'copyDir': ".simpsvc/copy",
         'diffDir': ".simpsvc/diff",
+        'cacheDir': ".simpsvc/cache",
         'srcsFile': ".simpsvc/srcs"
         }
 gsCOMMITMSG_FILESUFFIX = "commitmsg"
@@ -71,6 +74,7 @@
     os.mkdir(me['baseDir'])
     os.mkdir(me['copyDir'])
     os.mkdir(me['diffDir'])
+    os.mkdir(me['cacheDir'])
     ts = time.strftime(gsTimeStampFormat)
     _commit_op(me, "INIT", ts, "Initialised SSVC repository today")
 
@@ -109,14 +113,15 @@
     print(me)
 
 
-def ssvccopy_mkdir(me, sDirs):
+def ssvc_mkdir(me, sBasePath, sDirs):
     """ Helper mkdir logic, which creates not just the leaf dir
         but also all the intermediate directories if required.
 
-        TOTHINK: As currently only copyDir maintains a directory
-        heirarchy within itself, its hardcoded for the same.
+        NOTE: Normally used when copying something into copyDir
+        or to the cacheDir. As these maintain the directory
+        hierarchy of the tracked files, when copied into them.
         """
-    cPath = me['copyDir']
+    cPath = sBasePath
     for cDir in sDirs.split(os.sep):
         cPath += (os.sep + cDir)
         try:
@@ -133,41 +138,40 @@
     os.system("cp {} {}".format(srcFile, destPath))
 
 
-def ssvccopy_cp(me, srcFile):
+def ssvc_cp(me, srcFile, sBaseDestPath):
     """ copy specified file into a mirrored directory heirarchy
-        in the copyDir folder of ssvc repository
-
-        TOTHINK: As currently only copyDir maintains a directory
-        heirarchy within itself, its hardcoded for the same.
+        in the specified folder.
+        It is normally used to copy files either into cacheDir
+        or to the copyDir of ssvc repository, based on whether
+        it is a add operation or commit operation.
         """
     sDir = os.path.dirname(srcFile)
-    destPath = os.path.join(me['copyDir'],sDir)
+    destPath = os.path.join(sBaseDestPath, sDir)
     _cp(srcFile, destPath)
 
 
 def do_add(me, sFile):
     """ The add operation of the ssvc repository.
         It adds the specified file to the runtime list of files
-        that are tracked by ssvc.
-        It creates a diff file for the file content in diffDir.
-        It inturn copies the file to the copyDir, as the official
-        commited reference for the file.
-        It also generates a OP commit message.
+        that are tracked by ssvc, if not already there.
+        It inturn copies the file to cacheDir, so that it can
+        be commited when requested later.
+        TOTHINK: Should I generate a OP commit message.
         """
     if sFile in me['files']:
-        print("WARN:add: [{}] already in repo".format(sFile))
-        return
+        print("INFO:add: [{}] already in repo".format(sFile))
+    else:
     me['files'].append(sFile)
+        print("INFO:add: [{}] new file being added to repo".format(sFile))
     ts = time.strftime(gsTimeStampFormat)
     # _commit_filediff needs to occur b4 ssvccopy_cp
     # bcas otherwise ssvccopy_cp will copy the file into copyDir
     # and filediff wont be able to generate the diff file
-    _commit_filediff(me, ts, sFile)
     sDir = os.path.dirname(sFile)
-    pathDest = ssvccopy_mkdir(me, sDir)
-    ssvccopy_cp(me, sFile)
-    sCommitMsg = 'Added file [{}]'.format(sFile)
-    _commit_op(me, "ADD", ts, sCommitMsg)
+    pathDest = ssvc_mkdir(me, me['cacheDir'], sDir)
+    ssvc_cp(me, sFile, me['cacheDir'])
+    #sCommitMsg = 'Added file [{}]'.format(sFile)
+    #_commit_op(me, "ADD", ts, sCommitMsg)
 
 
 def _do_diff(me, tCur, bInteractive=False):
