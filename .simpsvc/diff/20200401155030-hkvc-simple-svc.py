--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 14:32:22.622393559 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 14:42:55.498406951 +0530
@@ -195,7 +195,7 @@
     return bDiff
 
 
-def do_diff(me, sMode = "LC-WD", bIndebInteractive=False):
+def do_diff(me, sMode = "LC-WD", bInteractive=False):
     """ The diff operation of ssvc.
         It will go throu all the files being tracked by ssvc and
         cross checks if 
@@ -218,7 +218,7 @@
     if sMode == "CA-WD":
         oldBase = me['cacheDir']
         newBase = "."
-    elif sMode == "LC-CA"
+    elif sMode == "LC-CA":
         oldBase = me['copyDir']
         newBase = me['cacheDir']
     elif sMode == "LC-WD":
@@ -277,8 +277,10 @@
 
 def do_commit(me):
     """ The commit command | operation of ssvc.
-        It goes throu all the tracked files specified to ssvc,
-        and cross checks if there is any difference or not.
+        It goes throu all the tracked files in ssvc, which have
+        been added to the cache dir and cross checks if there 
+        is any difference or not.
+
         If any differences are found then
         1. user is asked to provide a commit message
         2. the differences of the tracked files are captured 
@@ -287,6 +289,11 @@
            files are backed up into copyDir, making them the
            last commited copy for those files.
         """
+    lFiles = list(map(lambda x: os.path.join(me['cacheDir'], x), me['files']))
+    print(lFiles)
+    lFiles = list(filter(os.path.exists, lFiles))
+    print(lFiles)
+    exit()
     if not do_diff(me, bInteractive=True):
         print("WARN:commit: No changes identified, so skipping commit...")
         return
