--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 17:56:07.475400484 +0530
+++ hkvc-simple-svc.py	2020-03-29 18:27:37.880370919 +0530
@@ -111,18 +111,25 @@
     _commit_op(me, "ADD", sCommitMsg)
 
 
-def do_diff(me, bInteractive=False):
-    bDiffs = False
-    for tCur in me['files']:
+def _do_diff(me, tCur, bInteractive=False):
+    bDiff = False
         tOld = os.path.join(me['copyDir'], tCur)
         diffOk = os.system("diff -ub {} {}".format(tOld, tCur))
         if diffOk != 0:
             if bInteractive:
                 input("WARN:diff:Changes:{}\nPress any key to continue...".format(tCur))
-            bDiffs = True
+        bDiff = True
         else:
             if bInteractive:
                 input("INFO:diff:NoChange:{}\nPress any key to continue...".format(tCur))
+    return bDiff
+
+
+def do_diff(me, bInteractive=False):
+    bDiffs = False
+    for tCur in me['files']:
+        if _do_diff(me, tCur, bInteractive):
+            bDiffs = True
     return bDiffs
 
 
