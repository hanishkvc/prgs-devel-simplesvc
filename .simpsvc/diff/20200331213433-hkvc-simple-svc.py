--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-31 15:52:28.832078287 +0530
+++ hkvc-simple-svc.py	2020-03-31 15:57:47.289085026 +0530
@@ -35,7 +35,7 @@
         'srcsFile': ".simpsvc/srcs"
         }
 gsCOMMITMSG_FILESUFFIX = "commitmsg"
-gsTimeStampFormat="%Y%m%d%H%M"
+gsTimeStampFormat="%Y%m%d%H%M%S"
 
 
 gDBGLVL = 10
@@ -395,7 +395,7 @@
 
 
 if len(sys.argv) == 1:
-    print("{}, v20200329IST1535, HanishKVC".format(sys.argv[0]))
+    print("{}, v20200331IST1557, HanishKVC".format(sys.argv[0]))
     print("usage: ssvc [<cmd> [args]] [<cmd> [args]]...")
     print("\t the <cmd> can be one of init|dump|add|diff|commit|log")
     print("\t optional args")
