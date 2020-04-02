--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-31 21:37:44.546167900 +0530
+++ hkvc-simple-svc.py	2020-04-01 09:30:06.493009788 +0530
@@ -351,6 +351,18 @@
             os.system("{} {}".format(theCmd, theFile))
 
 
+def do_edit(me, index):
+    """ Edit index specified commit message 
+        index starts from 0, with 0 being the latest commit.
+        one can use -1 for the last item, -2 for last but one
+        and so on.
+        """
+    lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
+    print(lFiles)
+    lFiles = filter(lambda x: x.endswith(gsCOMMITMSG_FILESUFFIX), lFiles)
+    print(lFiles)
+
+
 def peek_ingroup(grp, index):
     """ Helper to get item at a specified location in a given list.
         If the specified location is invalid, then returns None
@@ -370,6 +382,7 @@
             do_init(me)
             iArg += 1
         elif args[iArg] == "add":
+            # requires 1 additional argument
             do_add(me, args[iArg+1])
             iArg += 2
         elif args[iArg] == "diff":
@@ -382,6 +395,7 @@
             do_commit(me)
             iArg += 1
         elif args[iArg] == "log":
+            # can have 1 optional argument
             if peek_ingroup(args, iArg+1) == "--patch":
                 bPatch=True
                 iArg += 1
@@ -389,6 +403,18 @@
                 bPatch=False
             do_log(me,bPatch)
             iArg += 1
+        elif args[iArg] == "editcmsg":
+            # this command consumes 1 adjacent arg, if any,
+            # irrespective of whether it is related or not
+            sOffset = peek_ingroup(args, iArg+1)
+            if (sOffset == None):
+                iOffset = 0
+            elif sOffset[0].isalpha():
+                iOffset = 0
+            else:
+                iOffset = int(sOffset)
+            do_edit(me, iOffset)
+            iArg += 2
         else:
             print("WARN: Skipping unknown arg[{}]".format(args[iArg]))
             iArg += 1
@@ -398,6 +424,7 @@
     print("{}, v20200331IST1557, HanishKVC".format(sys.argv[0]))
     print("usage: ssvc [<cmd> [args]] [<cmd> [args]]...")
     print("\t the <cmd> can be one of init|dump|add|diff|commit|log")
+    print("\t rare <cmd>'s are editcmsg")
     print("\t optional args")
     print("\t <log> --patch : also print the patchs associated with each commit")
     exit()
