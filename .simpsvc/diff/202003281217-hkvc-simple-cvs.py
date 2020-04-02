--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 11:38:25.071210747 +0530
+++ hkvc-simple-cvs.py	2020-03-28 12:15:55.936258377 +0530
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
@@ -71,6 +75,32 @@
         os.system("diff -ub {} {}".format(tOld, tCur))
 
 
+def _commit_filediff(me, ts, tCur):
+    tOld = os.path.join(me['copyDir'], tCur)
+    tDiffFN = "{}-{}".format(ts,tCur.replace(os.sep,"^"))
+    tDiff = os.path.join(me['diffDir'], tDiffFN)
+    os.system("diff -ub {} {} > {}".format(tOld, tCur, tDiff))
+
+
+def _commit_filecopy(me,tCur):
+    None
+
+
+def do_commit(me):
+    ts = time.strftime("%Y%m%d%H%M")
+    fnCommitMsg = "/tmp/{}-commitmsg".format(ts)
+    os.system("vim {}".format(fnCommitMsg))
+    cmSize = os.path.getsize(fnCommitMsg)
+    if (cmSize < 5):
+        print("WARN:commit: Skipping commit bcas No commit msg")
+        return
+    else:
+        os.system("cp {} {}".format(fnCommitMsg, me['diffDir']))
+    for tCur in me['files']:
+        _commit_filediff(me, ts, tCur)
+        _commit_filecopy(me, tCur)
+
+
 def process_args(args):
     iArg = 0
     while iArg < len(args):
@@ -86,6 +116,9 @@
         elif args[iArg] == "dump":
             do_dump(me)
             iArg += 1
+        elif args[iArg] == "commit":
+            do_commit(me)
+            iArg += 1
         else:
             print("WARN: Skipping unknown arg[{}]".format(args[iArg]))
             iArg += 1
