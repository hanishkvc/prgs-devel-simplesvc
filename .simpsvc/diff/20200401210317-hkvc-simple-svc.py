--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 19:53:18.769032180 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 21:01:53.996119261 +0530
@@ -173,6 +173,14 @@
         return False
 
 
+def ssvc_fileexists_list(me, sBaseDir, lInFiles):
+    """ Get list of files which exist in the given BaseDir from 
+        the list of given files.
+        """
+    lOut = list(filter(lambda x: os.path.exists(os.path.join(sBaseDir, x)), lInFiles))
+    return lOut
+
+
 def do_add(me, sFile):
     """ The add operation of the ssvc repository.
 
@@ -249,6 +257,9 @@
         newBase = "."
     else:
         return
+    # Cross check files exist, if oldBase is cacheDir
+    if oldBase == me['cacheDir']:
+        lFiles = ssvc_fileexists_list(me, oldBase, lFiles)
     # Do the logic
     bDiffs = False
     for tCur in lFiles:
@@ -303,12 +314,13 @@
 
 
 def _commit_fileexists_list(me, lIn):
-    lOut = []
-    for f in lIn:
-        sFile = os.path.join(me['cacheDir'], f)
-        if os.path.exists(sFile):
-            lOut.append(f)
-    return lOut
+    #lOut = []
+    #for f in lIn:
+    #    sFile = os.path.join(me['cacheDir'], f)
+    #    if os.path.exists(sFile):
+    #        lOut.append(f)
+    #return lOut
+    return ssvc_fileexists_list(me, me['cacheDir'], lIn)
 
 
 def do_commit(me):
