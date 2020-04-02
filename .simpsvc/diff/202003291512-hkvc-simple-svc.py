--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 14:49:29.235575625 +0530
+++ hkvc-simple-svc.py	2020-03-29 15:10:44.398555682 +0530
@@ -82,6 +82,13 @@
     _cp(srcFile, destPath)
 
 
+def _commit_op(me, sOp, sMsg):
+    ts = time.strftime(gsTimeStampFormat)
+    tFile = "{}-OP_{}-{}".format(ts, sOp, gsCOMMITMSG_FILESUFFIX)
+    theFile = os.path.join(me['diffDir'], tFile)
+    os.system("echo '{}' > {}".format(sMsg, theFile))
+
+
 def do_add(me, sFile):
     if sFile in me['files']:
         print("WARN:add: [{}] already in repo".format(sFile))
@@ -90,10 +97,8 @@
     sDir = os.path.dirname(sFile)
     pathDest = ssvccopy_mkdir(me, sDir)
     ssvccopy_cp(me, sFile)
-    ts = time.strftime(gsTimeStampFormat)
-    tFile = "{}-OP-{}".format(ts, gsCOMMITMSG_FILESUFFIX)
-    theFile = os.path.join(me['diffDir'], tFile)
-    os.system("echo 'Added file [{}]' > {}".format(sFile, theFile))
+    sCommitMsg = 'Added file [{}]'.format(sFile)
+    _commit_op(me, "ADD", sCommitMsg)
 
 
 def do_diff(me, bInteractive=False):
@@ -127,7 +132,7 @@
     tDiff = os.path.join(me['diffDir'], tDiffFN)
     res = os.system("diff -ub {} {} > {}".format(tOld, tCur, tDiff))
     if res != 0:
-        print("DBUG:_commit_filediff: diff of {} says {}".format(tCur, res))
+        #print("DBUG:_commit_filediff: diff of {} says {}".format(tCur, res))
         return True
     if os.path.getsize(tDiff) == 0:
         os.remove(tDiff)
