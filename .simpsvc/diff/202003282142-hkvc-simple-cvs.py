--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 13:50:48.013378825 +0530
+++ hkvc-simple-cvs.py	2020-03-28 21:40:27.705975124 +0530
@@ -101,12 +101,13 @@
     sgcopy_cp(me, tCur)
 
 
+gsCOMMITMSG_FILESUFFIX = "commitmsg"
 def do_commit(me):
     if not do_diff(me, bInteractive=True):
         print("WARN:commit: No changes identified, so skipping commit...")
         return
     ts = time.strftime("%Y%m%d%H%M")
-    fnCommitMsg = "/tmp/{}-commitmsg".format(ts)
+    fnCommitMsg = "/tmp/{}-{}".format(ts, gsCOMMITMSG_FILESUFFIX)
     os.system("vim {}".format(fnCommitMsg))
     cmSize = os.path.getsize(fnCommitMsg)
     if (cmSize < 5):
@@ -119,6 +120,21 @@
         _commit_filecopy(me, tCur)
 
 
+def do_log(me, bLess=False):
+    lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
+    for tFile in lFiles:
+        if tFile.endswith(gsCOMMITMSG_FILESUFFIX):
+            theFile = os.path.join(me['diffDir'], tFile)
+            #print("\n\nINFO:log: #### {} #### \n".format(tFile))
+            sPrefix = "\n\nINFO:log: #### {} #### \n".format(tFile)
+            if bLess:
+                theCmd = "less"
+            else:
+                theCmd = "cat"
+            os.system("echo '{}'".format(sPrefix))
+            os.system("{} {}".format(theCmd, theFile))
+
+
 def process_args(args):
     iArg = 0
     while iArg < len(args):
@@ -137,6 +153,9 @@
         elif args[iArg] == "commit":
             do_commit(me)
             iArg += 1
+        elif args[iArg] == "log":
+            do_log(me)
+            iArg += 1
         else:
             print("WARN: Skipping unknown arg[{}]".format(args[iArg]))
             iArg += 1
