--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 21:09:14.986128592 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 21:20:33.854142958 +0530
@@ -475,6 +475,21 @@
     return grp[index]
 
 
+def diff_args(sArg, iArg):
+    if (sArg == None):
+        sArg = "CA-WD"
+    elif sArg.startswith("--"):
+        sArg = sArg[2:]
+        if (sArg == "cached"):
+            sArg = "LC-CA"
+        elif (sArg == "commit"):
+            sArg = "LC-WD"
+        iArg += 1
+    else:
+        sArg = "CA-WD"
+    return sArg, iArg
+
+
 def process_args(args):
     """ Logic to process the arguments passed to the ssvc program
         """
@@ -490,13 +505,7 @@
         elif args[iArg] == "diff":
             # can have 1 optional argument
             sArg = peek_ingroup(args, iArg+1)
-            if (sArg == None):
-                sArg = "LC-WD"
-            elif sArg.startswith("--"):
-                sArg = sArg[2:]
-                iArg += 1
-            else:
-                sArg = "LC-WD"
+            sArg, iArg = diff_args(sArg, iArg)
             do_diff(me, sMode=sArg)
             iArg += 1
         elif args[iArg] == "dump":
@@ -532,15 +541,15 @@
 
 
 if len(sys.argv) == 1:
-    print("{}, v20200331IST1557, HanishKVC".format(sys.argv[0]))
+    print("{}, v20200401IST2117, HanishKVC".format(sys.argv[0]))
     print("usage: ssvc [<cmd> [args]] [<cmd> [args]]...")
     print("\t the <cmd> can be one of init|dump|add|diff|commit|log")
     print("\t rare <cmd>'s are editcmsg")
     print("\t optional args")
     print("\t <log> --patch : also print the patchs associated with each commit")
-    print("\t <diff> --LC-WD : print diff between last commit and working dir")
-    print("\t <diff> --LC-CA : print diff between last commit and cache dir")
-    print("\t <diff> --CA-WD : print diff between cache dir and working dir")
+    print("\t <diff> --CA-WD(default) : print diff between cache dir and working dir")
+    print("\t <diff> --LC-WD|--commit : print diff between last commit and working dir")
+    print("\t <diff> --LC-CA|--cached : print diff between last commit and cache dir")
     exit()
 
 
