--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 12:22:04.191266170 +0530
+++ hkvc-simple-cvs.py	2020-03-28 12:38:17.863286773 +0530
@@ -55,10 +55,16 @@
     return cPath
 
 
-def sgcopy_cp(srcFile, destPath):
+def _cp(srcFile, destPath):
     os.system("cp {} {}".format(srcFile, destPath))
 
 
+def sgcopy_cp(me, srcFile):
+    sDir = os.path.dirname(srcFile)
+    destPath = os.path.join(me['copyDir'],sDir)
+    _cp(srcFile, destPath)
+
+
 def do_add(me, sFile):
     if sFile in me['files']:
         print("WARN:add: [{}] already in repo".format(sFile))
@@ -66,7 +72,7 @@
     me['files'].append(sFile)
     sDir = os.path.dirname(sFile)
     pathDest = sgcopy_mkdir(me, sDir)
-    sgcopy_cp(sFile, pathDest)
+    sgcopy_cp(me, sFile)
 
 
 def do_diff(me):
@@ -83,7 +89,7 @@
 
 
 def _commit_filecopy(me,tCur):
-    None
+    sgcopy_cp(me, tCur)
 
 
 def do_commit(me):
