--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 16:47:54.980565645 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 16:59:30.350580359 +0530
@@ -377,7 +377,7 @@
     f = open(sFile)
     i = 0
     for l in f:
-        print(l)
+        print(l, end="")
         if bLess and ((i%25) == 0):
             input("Press any key...")
 
@@ -457,7 +457,16 @@
             do_add(me, args[iArg+1])
             iArg += 2
         elif args[iArg] == "diff":
-            do_diff(me)
+            # can have 1 optional argument
+            sArg = peek_ingroup(args, iArg+1)
+            if (sArg == None):
+                sArg = "LC-WD"
+            elif sArg.startswith("--"):
+                sArg = sArg[2:]
+                iArg += 1
+            else:
+                sArg = "LC-WD"
+            do_diff(me, sMode=sArg)
             iArg += 1
         elif args[iArg] == "dump":
             do_dump(me)
