--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 01:24:32.979259634 +0530
+++ hkvc-simple-svc.py	2020-03-29 01:29:20.666265722 +0530
@@ -1,5 +1,5 @@
 #!/usr/bin/env python3
-# A simple Code Version System
+# A Simple Source Version Control
 # v20200328IST1114, HanishKVC
 #
 
@@ -10,10 +10,10 @@
 
 me = {
         'files': [],
-        'baseDir': ".simpcvs",
-        'copyDir': ".simpcvs/copy",
-        'diffDir': ".simpcvs/diff",
-        'srcsFile': ".simpcvs/srcs"
+        'baseDir': ".simpsvc",
+        'copyDir': ".simpsvc/copy",
+        'diffDir': ".simpsvc/diff",
+        'srcsFile': ".simpsvc/srcs"
         }
 gsCOMMITMSG_FILESUFFIX = "commitmsg"
 gsTimeStampFormat="%Y%m%d%H%M"
@@ -39,7 +39,7 @@
             l = l.strip()
             me['files'].append(l)
     except FileNotFoundError:
-        print("WARN:load:No simpcvs repo found")
+        print("WARN:load:No simpsvc repo found")
 
 
 def do_dump(me):
