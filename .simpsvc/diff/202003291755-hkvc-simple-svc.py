--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 17:40:28.209415175 +0530
+++ hkvc-simple-svc.py	2020-03-29 17:41:58.369413765 +0530
@@ -37,8 +37,9 @@
 gDBGLVL = 10
 DLVL_ALWAYS = 0
 DLVL_ERROR = 1
+DLVL_DEFAULT=gDBGLVL
 DLVL_DBUG = 11
-def dprint(sMsg, dbgLvl):
+def dprint(sMsg, dbgLvl=DLVL_DEFAULT):
     if (dbgLvl < gDBGLVL):
         print(sMsg)
 
