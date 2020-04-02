--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 11:38:25.071210747 +0530
+++ hkvc-simple-cvs.py	2020-03-28 11:52:52.703229107 +0530
@@ -5,11 +5,14 @@
 
 import os
 import sys
+import time
+
 
 me = {
         'files': [],
         'baseDir': ".simpcvs",
         'copyDir': ".simpcvs/copy",
+        'diffDir': ".simpcvs/diff",
         'srcsFile': ".simpcvs/srcs"
         }
 
@@ -17,6 +20,7 @@
 def do_init(me):
     os.mkdir(me['baseDir'])
     os.mkdir(me['copyDir'])
+    os.mkdir(me['diffDir'])
 
 
 def do_save(me):
@@ -71,6 +75,16 @@
         os.system("diff -ub {} {}".format(tOld, tCur))
 
 
+def do_commit(me):
+    ts = time.strftime("%Y%m%d%H%M")
+    for tCur in me['files']:
+        tOld = os.path.join(me['copyDir'], tCur)
+        tDiffFN = "{}-{}".format(ts,tCur.replace(os.sep,"-"))
+        tDiff = os.path.join(me['diffDir'], tDiffFN)
+        os.system("diff -ub {} {} > {}".format(tOld, tCur, tDiff))
+
+
+
 def process_args(args):
     iArg = 0
     while iArg < len(args):
@@ -86,6 +100,9 @@
         elif args[iArg] == "dump":
             do_dump(me)
             iArg += 1
+        elif args[iArg] == "commit":
+            do_commit(me)
+            iArg += 1
         else:
             print("WARN: Skipping unknown arg[{}]".format(args[iArg]))
             iArg += 1
