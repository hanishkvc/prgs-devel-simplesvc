--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 01:36:59.243275426 +0530
+++ hkvc-simple-svc.py	2020-03-29 14:16:05.432606965 +0530
@@ -8,6 +8,21 @@
 import time
 
 
+# The core context includes
+# files:runtime_only:The list of source files being tracked
+# baseDir: the base directory containing the ssvc repository
+#   It is normally a hidden directory at the root dir of the 
+#   files being tracked.
+# copyDir: this contains a copy of the last commited instance
+#   of all the files being tracked.
+#   It mirrors the directory structure of the original files
+# diffDir: Contains the history of the changes till date
+#   This consists of commit messages and corresponding diff
+#   files for all the tracked files.
+#   The files are timestamp prefixed. Also the directory
+#   path of the files are specified as part of the file
+#   name itself.
+# srcsFile: the list of source files being tracked
 me = {
         'files': [],
         'baseDir': ".simpsvc",
@@ -46,7 +61,7 @@
     print(me)
 
 
-def sgcopy_mkdir(me, sDirs):
+def ssvccopy_mkdir(me, sDirs):
     cPath = me['copyDir']
     for cDir in sDirs.split(os.sep):
         cPath += (os.sep + cDir)
@@ -61,7 +76,7 @@
     os.system("cp {} {}".format(srcFile, destPath))
 
 
-def sgcopy_cp(me, srcFile):
+def ssvccopy_cp(me, srcFile):
     sDir = os.path.dirname(srcFile)
     destPath = os.path.join(me['copyDir'],sDir)
     _cp(srcFile, destPath)
@@ -73,8 +88,8 @@
         return
     me['files'].append(sFile)
     sDir = os.path.dirname(sFile)
-    pathDest = sgcopy_mkdir(me, sDir)
-    sgcopy_cp(me, sFile)
+    pathDest = ssvccopy_mkdir(me, sDir)
+    ssvccopy_cp(me, sFile)
     ts = time.strftime(gsTimeStampFormat)
     tFile = "{}-OP-{}".format(ts, gsCOMMITMSG_FILESUFFIX)
     theFile = os.path.join(me['diffDir'], tFile)
@@ -104,7 +119,7 @@
 
 
 def _commit_filecopy(me,tCur):
-    sgcopy_cp(me, tCur)
+    ssvccopy_cp(me, tCur)
 
 
 def do_commit(me):
