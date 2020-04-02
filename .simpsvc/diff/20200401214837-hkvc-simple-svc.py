--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 21:34:41.183160888 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 21:48:17.739178166 +0530
@@ -244,6 +244,11 @@
         and the copy of the file within ssvc's cacheDir and the copy
 
         match or else show what is the difference.
+
+        If oldBase is cacheDir, then the given file list is filtered
+        to cross check that those files actually exist in cacheDir.
+        Parallely if there are no files in cacheDir, then automatically
+        switch to testing between copyDir and working dir.
         """
     # Setup paths
     if sMode == "CA-WD":
@@ -259,7 +264,12 @@
         return
     # Cross check files exist, if oldBase is cacheDir
     if oldBase == me['cacheDir']:
-        lFiles = ssvc_fileexists_list(me, oldBase, lFiles)
+        tlFiles = ssvc_fileexists_list(me, oldBase, lFiles)
+        if len(tlFiles) != 0:
+            lFiles = tlFiles
+        else:
+            input("INFO:diff:Change from cacheDir to copyDir, Press any key...")
+            oldBase = me['copyDir']
     # Do the logic
     bDiffs = False
     for tCur in lFiles:
