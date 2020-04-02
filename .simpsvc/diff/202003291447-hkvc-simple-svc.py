--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 14:19:26.506603820 +0530
+++ hkvc-simple-svc.py	2020-03-29 14:46:48.763578135 +0530
@@ -112,10 +112,26 @@
 
 
 def _commit_filediff(me, ts, tCur):
+    """ file diff helper for commit command
+        It generates the diff file related to commit.
+        It also tells if there was a diff/change wrt
+            the file being looked at, in the working directory
+            or if the working and saved copy are the same.
+            If there is a change it returns True
+        me: the context
+        ts: the time stamp to use
+        tCur: the file (including the path) being looked at.
+        """
     tOld = os.path.join(me['copyDir'], tCur)
     tDiffFN = "{}-{}".format(ts,tCur.replace(os.sep,"^"))
     tDiff = os.path.join(me['diffDir'], tDiffFN)
-    os.system("diff -ub {} {} > {}".format(tOld, tCur, tDiff))
+    res = os.system("diff -ub {} {} > {}".format(tOld, tCur, tDiff))
+    if res != 0:
+        print("DBUG:_commit_filediff: diff of {} says {}".format(tCur, res))
+        return True
+    if os.path.getsize(tDiff) == 0:
+        os.remove(tDiff)
+    return False
 
 
 def _commit_filecopy(me,tCur):
@@ -136,7 +152,7 @@
     else:
         os.system("cp {} {}".format(fnCommitMsg, me['diffDir']))
     for tCur in me['files']:
-        _commit_filediff(me, ts, tCur)
+        if _commit_filediff(me, ts, tCur):
         _commit_filecopy(me, tCur)
 
 
