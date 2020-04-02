--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-31 10:02:41.210634177 +0530
+++ hkvc-simple-svc.py	2020-03-31 12:19:06.783807388 +0530
@@ -269,6 +269,17 @@
 
 
 def sort_diffDir(lIn):
+    """ helper logic to sort the list of file names given according
+        to ssvc convention for diffDir log output.
+        When one is viewing the details of all the commits done till
+        date or a given subset of commits or a specific commit,
+        one will ideally want to look at the commit message first 
+        followed by the contents of the tracked files which changed
+        as part of that commit. This helper logic helps sort the
+        list of file names, to achieve this goal.
+        i.e For any given commit, it puts the commitmsg file first
+        followed by the files which form part of that commit.
+        """
     lOut = []
     lTmp = []
     sTmpCMsg = None
@@ -302,6 +313,15 @@
 
 
 def do_log(me, bPatch=False, bLess=False):
+    """ Generate a log of all commits till date.
+        By default it only contains the contents of the commit messages.
+        However by specifying bPatch as True, one can also include the
+        contents of the files associated with the commits.
+        NOTE1: commit command stores diffs of files in diffDir
+               add command stores content of new file in diffDir
+        NOTE2: This logic iterates through contents of diffDir, in a
+               sorted manner.
+        """
     lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
     lFiles = sort_diffDir(lFiles)
     for tFile in lFiles:
@@ -325,13 +345,19 @@
             os.system("{} {}".format(theCmd, theFile))
 
 
-def peek_nextarg(args, iNextArg):
-    if iNextArg >= len(args):
+def peek_ingroup(grp, index):
+    """ Helper to get item at a specified location in a given list.
+        If the specified location is invalid, then returns None
+        NOTE: This avoids raising a exception if the index is invalid.
+        """
+    if index >= len(grp):
         return None
-    return args[iNextArg]
+    return grp[index]
 
 
 def process_args(args):
+    """ Logic to process the arguments passed to the ssvc program
+        """
     iArg = 0
     while iArg < len(args):
         if args[iArg] == "init":
@@ -350,7 +376,7 @@
             do_commit(me)
             iArg += 1
         elif args[iArg] == "log":
-            if peek_nextarg(args, iArg+1) == "--patch":
+            if peek_ingroup(args, iArg+1) == "--patch":
                 bPatch=True
                 iArg += 1
             else:
@@ -371,6 +397,10 @@
     exit()
 
 
+# Load the context from disk
 do_load(me)
+# Process the given arguments
 process_args(sys.argv[1:])
+# Save the context to disk
 do_save(me)
+
