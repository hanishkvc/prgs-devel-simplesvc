--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 16:26:11.202484882 +0530
+++ hkvc-simple-svc.py	2020-03-29 16:42:44.558469346 +0530
@@ -161,8 +161,31 @@
             _commit_filecopy(me, tCur)
 
 
+def sort_diffDir(lIn):
+    lOut = []
+    lTmp = []
+    for l in lIn:
+        if l.endswith(gsCOMMITMSG_FILESUFFIX):
+            lOut.append(l)
+            for m in lTmp:
+                lOut.append(m)
+            lTmp = []
+        else:
+            lTmp.append(l)
+    for m in lTmp:
+        lOut.append(m)
+    lenIn = len(lIn)
+    lenOut = len(lOut)
+    if (lenIn != lenOut):
+        print("DBUG:sort_diffdir: size of given {} & sorted {} list dont match".format(lenIn, lenOut))
+        exit()
+    for i in range(lenIn):
+        print("{:50}, {:50}".format(lIn[i], lOut[i]))
+    exit()
+
 def do_log(me, bPatch=False, bLess=False):
     lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
+    lFiles = sort_diffDir(lFiles)
     for tFile in lFiles:
         bPrint = False
         sType = "NOTME_FIXME"
