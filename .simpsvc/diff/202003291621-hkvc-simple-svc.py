--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 16:09:13.723500796 +0530
+++ hkvc-simple-svc.py	2020-03-29 16:16:01.634494416 +0530
@@ -164,10 +164,18 @@
 def do_log(me, bPatch=False, bLess=False):
     lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
     for tFile in lFiles:
-        if tFile.endswith(gsCOMMITMSG_FILESUFFIX) or bPatch:
+        bPrint = False
+        sType = "NOTME_FIXME"
+        if bPatch:
+            sType = "diff"
+            bPrint = True
+        if tFile.endswith(gsCOMMITMSG_FILESUFFIX):
+            sType = "log"
+            bPrint = True
+        if bPrint:
             theFile = os.path.join(me['diffDir'], tFile)
             #print("\n\nINFO:log: #### {} #### \n".format(tFile))
-            sPrefix = "\n\nINFO:log: #### {} #### \n".format(tFile)
+            sPrefix = "\n\nINFO:{}: #### {} #### \n".format(sType, tFile)
             if bLess:
                 theCmd = "less"
             else:
