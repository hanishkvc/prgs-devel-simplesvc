--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 12:52:15.064266436 +0530
+++ hkvc-simple-svc.py	2020-04-01 13:46:21.279335127 +0530
@@ -174,7 +174,7 @@
     #_commit_op(me, "ADD", ts, sCommitMsg)
 
 
-def _do_diff(me, tCur, bInteractive=False):
+def _do_diff(me, tCur, sOldBasePath, sNewBasePath, bInteractive=False):
     """ The helper logic which does the actual low level diff
         operation, using the systems diff command.
         Given the file to diff, it automatically identifies the
@@ -182,8 +182,9 @@
         the ssvc repository and compares against it.
         """
     bDiff = False
-    tOld = os.path.join(me['copyDir'], tCur)
-    diffOk = os.system("diff --unidirectional-new-file -ub {} {}".format(tOld, tCur))
+    tOld = os.path.join(sOldBasePath, tCur)
+    tNew = os.path.join(sNewBasePath, tCur)
+    diffOk = os.system("diff --unidirectional-new-file -ub {} {}".format(tOld, tNew))
     if diffOk != 0:
         if bInteractive:
             input("WARN:diff:Changes:{}\nPress any key to continue...".format(tCur))
@@ -194,16 +195,41 @@
     return bDiff
 
 
-def do_diff(me, bInteractive=False):
+def do_diff(me, sMode = "LC-WD", bIndebInteractive=False):
     """ The diff operation of ssvc.
         It will go throu all the files being tracked by ssvc and
-        cross checks if the last commited copy of the file within
-        ssvc (i.e copyDir) and the copy in the users working dir
+        cross checks if 
+        
+        CopyDir & WorkingDir (default):
+        the last commited copy of the file within ssvc (i.e copyDir) 
+        and the copy in the users working dir
+
+        CacheDir & WorkingDir:
+        the copy of the file within ssvc's cacheDir and the copy
+        in the users working dir
+        
+        CopyDir & CacheDir:
+        the last commited copy of the file within ssvc (i.e copyDir) 
+        and the copy of the file within ssvc's cacheDir and the copy
+
         match or else what is the difference.
         """
+    # Setup paths
+    if sMode == "CA-WD":
+        oldBase = me['cacheDir']
+        newBase = "."
+    elif sMode == "LC-CA"
+        oldBase = me['copyDir']
+        newBase = me['cacheDir']
+    elif sMode == "LC-WD":
+        oldBase = me['copyDir']
+        newBase = "."
+    else:
+        return
+    # Do the logic
     bDiffs = False
     for tCur in me['files']:
-        if _do_diff(me, tCur, bInteractive):
+        if _do_diff(me, tCur, oldBase, newBase, bInteractive):
             bDiffs = True
     return bDiffs
 
