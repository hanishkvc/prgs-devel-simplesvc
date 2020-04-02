--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 12:43:40.694293604 +0530
+++ hkvc-simple-cvs.py	2020-03-28 13:29:38.245351956 +0530
@@ -75,10 +75,21 @@
     sgcopy_cp(me, sFile)
 
 
-def do_diff(me):
+def do_diff(me, bInteractive=False):
+    bDiffs = False
     for tCur in me['files']:
         tOld = os.path.join(me['copyDir'], tCur)
-        os.system("diff -ub {} {}".format(tOld, tCur))
+        diffOk = os.system("diff -ub {} {}".format(tOld, tCur))
+        if bInteractive:
+            print("INFO:diff:File:{}".format(tCur))
+        if diffOk != 0:
+            if bInteractive:
+                input("WARN:diff:Changes:Press any key to continue...")
+            bDiffs = True
+        else:
+            if bInteractive:
+                input("INFO:diff:NoChange:Press any key to continue...")
+    return bDiffs
 
 
 def _commit_filediff(me, ts, tCur):
