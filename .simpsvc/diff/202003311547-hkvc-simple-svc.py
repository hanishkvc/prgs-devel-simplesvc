--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-31 15:15:48.940031736 +0530
+++ hkvc-simple-svc.py	2020-03-31 15:42:22.937065466 +0530
@@ -48,7 +48,7 @@
         print(sMsg)
 
 
-def _commit_op(me, sOp, sMsg):
+def _commit_op(me, sOp, ts, sMsg):
     """ Helper which can be used by the different operations to
         generate a commitmsg file in the diffDir.
         To be used by those operations which want to convey the
@@ -56,7 +56,6 @@
         future reference.
         sOp : the operation, by convention specified in CAPS.
         """
-    ts = time.strftime(gsTimeStampFormat)
     tFile = "{}-OP_{}-{}".format(ts, sOp, gsCOMMITMSG_FILESUFFIX)
     theFile = os.path.join(me['diffDir'], tFile)
     os.system("echo '{}' > {}".format(sMsg, theFile))
@@ -72,7 +71,8 @@
     os.mkdir(me['baseDir'])
     os.mkdir(me['copyDir'])
     os.mkdir(me['diffDir'])
-    _commit_op(me, "INIT", "Initialised SSVC repository today")
+    ts = time.strftime(gsTimeStampFormat)
+    _commit_op(me, "INIT", ts, "Initialised SSVC repository today")
 
 
 def do_save(me):
@@ -149,6 +149,7 @@
     """ The add operation of the ssvc repository.
         It adds the specified file to the runtime list of files
         that are tracked by ssvc.
+        It creates a diff file for the file content in diffDir.
         It inturn copies the file to the copyDir, as the official
         commited reference for the file.
         It also generates a OP commit message.
@@ -158,12 +159,15 @@
         return
     me['files'].append(sFile)
     ts = time.strftime(gsTimeStampFormat)
+    # _commit_filediff needs to occur b4 ssvccopy_cp
+    # bcas otherwise ssvccopy_cp will copy the file into copyDir
+    # and filediff wont be able to generate the diff file
     _commit_filediff(me, ts, sFile)
     sDir = os.path.dirname(sFile)
     pathDest = ssvccopy_mkdir(me, sDir)
     ssvccopy_cp(me, sFile)
     sCommitMsg = 'Added file [{}]'.format(sFile)
-    _commit_op(me, "ADD", sCommitMsg)
+    _commit_op(me, "ADD", ts, sCommitMsg)
 
 
 def _do_diff(me, tCur, bInteractive=False):
