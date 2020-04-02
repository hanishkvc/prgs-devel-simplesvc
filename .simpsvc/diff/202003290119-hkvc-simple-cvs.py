--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 21:44:14.988979934 +0530
+++ hkvc-simple-cvs.py	2020-03-29 01:10:22.317241634 +0530
@@ -15,6 +15,8 @@
         'diffDir': ".simpcvs/diff",
         'srcsFile': ".simpcvs/srcs"
         }
+gsCOMMITMSG_FILESUFFIX = "commitmsg"
+gsTimeStampFormat="%Y%m%d%H%M"
 
 
 def do_init(me):
@@ -73,6 +75,10 @@
     sDir = os.path.dirname(sFile)
     pathDest = sgcopy_mkdir(me, sDir)
     sgcopy_cp(me, sFile)
+    ts = time.strftime(gsTimeStampFormat)
+    tFile = "{}-OP-{}".format(ts, gsCOMMITMSG_FILESUFFIX)
+    theFile = os.path.join(me['diffDir'], tFile)
+    os.system("echo 'Added file [{}]' > {}".format(sFile, theFile))
 
 
 def do_diff(me, bInteractive=False):
@@ -101,12 +107,11 @@
     sgcopy_cp(me, tCur)
 
 
-gsCOMMITMSG_FILESUFFIX = "commitmsg"
 def do_commit(me):
     if not do_diff(me, bInteractive=True):
         print("WARN:commit: No changes identified, so skipping commit...")
         return
-    ts = time.strftime("%Y%m%d%H%M")
+    ts = time.strftime(gsTimeStampFormat)
     fnCommitMsg = "/tmp/{}-{}".format(ts, gsCOMMITMSG_FILESUFFIX)
     os.system("vim {}".format(fnCommitMsg))
     cmSize = os.path.getsize(fnCommitMsg)
