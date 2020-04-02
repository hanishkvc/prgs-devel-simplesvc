--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 13:40:46.948366106 +0530
+++ hkvc-simple-cvs.py	2020-03-28 13:45:18.155371845 +0530
@@ -80,15 +80,13 @@
     for tCur in me['files']:
         tOld = os.path.join(me['copyDir'], tCur)
         diffOk = os.system("diff -ub {} {}".format(tOld, tCur))
-        if bInteractive:
-            print("INFO:diff:File:{}".format(tCur))
         if diffOk != 0:
             if bInteractive:
-                input("WARN:diff:Changes:Press any key to continue...")
+                input("WARN:diff:Changes:{}\nPress any key to continue...".format(tCur))
             bDiffs = True
         else:
             if bInteractive:
-                input("INFO:diff:NoChange:Press any key to continue...")
+                input("INFO:diff:NoChange:{}\nPress any key to continue...".format(tCur))
     return bDiffs
 
 
