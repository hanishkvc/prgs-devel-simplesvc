--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 15:48:25.852520312 +0530
+++ hkvc-simple-svc.py	2020-03-29 15:58:18.274511047 +0530
@@ -176,6 +176,12 @@
             os.system("{} {}".format(theCmd, theFile))
 
 
+def peek_nextarg(args, iNextArg):
+    if iNextArg >= len(args):
+        return None
+    return args[iNextArg]
+
+
 def process_args(args):
     iArg = 0
     while iArg < len(args):
@@ -195,7 +201,7 @@
             do_commit(me)
             iArg += 1
         elif args[iArg] == "log":
-            if args[iArg+1] == "--patch":
+            if peek_nextarg(args, iArg+1) == "--patch":
                 bPatch=True
                 iArg += 1
             else:
@@ -209,9 +215,13 @@
 
 if len(sys.argv) == 1:
     print("{}, v20200329IST1535, HanishKVC".format(sys.argv[0]))
-    print("usage: ssvc [init|dump|add|diff|commit|log] [args]")
+    print("usage: ssvc [<cmd> [args]] [<cmd> [args]]...")
+    print("\t the <cmd> can be one of init|dump|add|diff|commit|log")
+    print("\t optional args")
+    print("\t <log> --patch : also print the patchs associated with each commit")
     exit()
 
+
 do_load(me)
 process_args(sys.argv[1:])
 do_save(me)
