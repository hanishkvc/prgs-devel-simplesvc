--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 16:53:34.593459180 +0530
+++ hkvc-simple-svc.py	2020-03-29 17:17:48.531436440 +0530
@@ -164,24 +164,34 @@
 def sort_diffDir(lIn):
     lOut = []
     lTmp = []
+    sTmpCMsg = None
+    sPrevTS = ""
     for l in lIn:
-        if l.endswith(gsCOMMITMSG_FILESUFFIX):
-            lOut.append(l)
+        sCurTS = l.split('-')[0]
+        if sCurTS != sPrevTS:
+            if sTmpCMsg != None:
+                lOut.append(sTmpCMsg)
+                sTmpCMsg = None
             for m in lTmp:
                 lOut.append(m)
             lTmp = []
+            sPrevTS = sCurTS
+        if l.endswith(gsCOMMITMSG_FILESUFFIX):
+            sTmpCMsg = l
         else:
             lTmp.append(l)
+    if sTmpCMsg != None:
+        lOut.append(sTmpCMsg)
     for m in lTmp:
         lOut.append(m)
     lenIn = len(lIn)
     lenOut = len(lOut)
     if (lenIn != lenOut):
-        print("DBUG:sort_diffdir: size of given {} & sorted {} list dont match".format(lenIn, lenOut))
+        dprint("DBUG:sort_diffdir: size of given {} & sorted {} list dont match".format(lenIn, lenOut), DLVL_ERROR)
         exit()
     for i in range(lenIn):
-        print("{:50}, {:50}".format(lIn[i], lOut[i]))
-    exit()
+        dprint("DBUG:sort_diffdir:{:50}, {:50}".format(lIn[i], lOut[i]), DLVL_DBUG)
+
 
 def do_log(me, bPatch=False, bLess=False):
     lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
