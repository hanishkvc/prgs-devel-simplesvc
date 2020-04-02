--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 17:24:42.906429959 +0530
+++ hkvc-simple-svc.py	2020-03-29 17:28:52.211426060 +0530
@@ -34,6 +34,15 @@
 gsTimeStampFormat="%Y%m%d%H%M"
 
 
+gDBGLVL = 10
+DLVL_ALWAYS = 0
+DLVL_ERROR = 1
+DLVL_DBUG = 11
+def dprint(sMsg, dbgLvl):
+    if (dbgLvl < gDBGLVL):
+        print(sMsg)
+
+
 def do_init(me):
     os.mkdir(me['baseDir'])
     os.mkdir(me['copyDir'])
@@ -191,6 +200,7 @@
         exit()
     for i in range(lenIn):
         dprint("DBUG:sort_diffdir:{:50}, {:50}".format(lIn[i], lOut[i]), DLVL_DBUG)
+    return lOut
 
 
 def do_log(me, bPatch=False, bLess=False):
