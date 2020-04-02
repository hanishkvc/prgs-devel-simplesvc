--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-31 12:21:20.849810225 +0530
+++ hkvc-simple-svc.py	2020-03-31 14:56:08.444006756 +0530
@@ -157,6 +157,8 @@
         print("WARN:add: [{}] already in repo".format(sFile))
         return
     me['files'].append(sFile)
+    ts = time.strftime(gsTimeStampFormat)
+    _commit_filediff(me, ts, sFile)
     sDir = os.path.dirname(sFile)
     pathDest = ssvccopy_mkdir(me, sDir)
     ssvccopy_cp(me, sFile)
@@ -173,7 +175,7 @@
         """
     bDiff = False
     tOld = os.path.join(me['copyDir'], tCur)
-    diffOk = os.system("diff -ub {} {}".format(tOld, tCur))
+    diffOk = os.system("diff --unidirectional-new-file -ub {} {}".format(tOld, tCur))
     if diffOk != 0:
         if bInteractive:
             input("WARN:diff:Changes:{}\nPress any key to continue...".format(tCur))
@@ -202,8 +204,8 @@
     """ file diff helper for commit command
         It generates the diff file for the specified file, which
             relates to this commit.
-            The same is copied into the copyDir.
-            NOTE: The copyDir follows a flattened directory approach.
+            The same is copied into the diffDir.
+            NOTE: The diffDir follows a flattened directory approach.
             i.e there are no sub directories to mirror the working 
             directory structure of the file. Instead the file path 
             is stored as part of the file name itself by prefixing
@@ -220,7 +222,7 @@
     tOld = os.path.join(me['copyDir'], tCur)
     tDiffFN = "{}-{}".format(ts,tCur.replace(os.sep,"^"))
     tDiff = os.path.join(me['diffDir'], tDiffFN)
-    res = os.system("diff -ub {} {} > {}".format(tOld, tCur, tDiff))
+    res = os.system("diff --unidirectional-new-file -ub {} {} > {}".format(tOld, tCur, tDiff))
     if res != 0:
         #print("DBUG:_commit_filediff: diff of {} says {}".format(tCur, res))
         return True
