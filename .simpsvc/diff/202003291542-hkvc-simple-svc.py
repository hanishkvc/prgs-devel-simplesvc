--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 15:24:31.229542750 +0530
+++ hkvc-simple-svc.py	2020-03-29 15:40:47.120527487 +0530
@@ -161,10 +161,10 @@
             _commit_filecopy(me, tCur)
 
 
-def do_log(me, bLess=False):
+def do_log(me, bPatch=False, bLess=False):
     lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
     for tFile in lFiles:
-        if tFile.endswith(gsCOMMITMSG_FILESUFFIX):
+        if tFile.endswith(gsCOMMITMSG_FILESUFFIX) or bPatch:
             theFile = os.path.join(me['diffDir'], tFile)
             #print("\n\nINFO:log: #### {} #### \n".format(tFile))
             sPrefix = "\n\nINFO:log: #### {} #### \n".format(tFile)
@@ -195,7 +195,12 @@
             do_commit(me)
             iArg += 1
         elif args[iArg] == "log":
-            do_log(me)
+            if args[iArg+1] == "--patch":
+                bPatch=True
+                iArg += 1
+            else:
+                bPatch=False
+            do_log(me,bPatch)
             iArg += 1
         else:
             print("WARN: Skipping unknown arg[{}]".format(args[iArg]))
@@ -203,7 +208,7 @@
 
 
 if len(sys.argv) == 1:
-    print("{}, v20200329IST1522, HanishKVC".format(sys.argv[0]))
+    print("{}, v20200329IST1535, HanishKVC".format(sys.argv[0]))
     print("usage: ssvc [init|dump|add|diff|commit|log] [args]")
     exit()
 
