--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 18:31:25.957367351 +0530
+++ hkvc-simple-svc.py	2020-03-31 09:57:36.963627739 +0530
@@ -8,21 +8,25 @@
 import time
 
 
-# The core context includes
-# files:runtime_only:The list of source files being tracked
-# baseDir: the base directory containing the ssvc repository
-#   It is normally a hidden directory at the root dir of the 
-#   files being tracked.
-# copyDir: this contains a copy of the last commited instance
-#   of all the files being tracked.
-#   It mirrors the directory structure of the original files
-# diffDir: Contains the history of the changes till date
-#   This consists of commit messages and corresponding diff
-#   files for all the tracked files.
-#   The files are timestamp prefixed. Also the directory
-#   path of the files are specified as part of the file
-#   name itself.
-# srcsFile: the list of source files being tracked
+"""
+The core context includes
+    files: The list of source files being tracked
+        This list variable is used only at runtime. The disk
+        store for this is the srcsFile specified below.
+    baseDir: the base directory containing the ssvc repository
+        It is normally a hidden directory at the root dir of the 
+        files being tracked.
+    copyDir: this contains a copy of the last commited instance
+        of all the files being tracked.
+        It mirrors the directory structure of the original files
+    diffDir: Contains the history of the changes till date
+        This consists of commit messages and corresponding diff
+        files for all the tracked files.
+        The files are timestamp prefixed. Also the directory
+        path of the files are specified as part of the file
+        name itself.
+    srcsFile: the list of source files being tracked
+"""
 me = {
         'files': [],
         'baseDir': ".simpsvc",
@@ -44,13 +48,38 @@
         print(sMsg)
 
 
+def _commit_op(me, sOp, sMsg):
+    """ Helper which can be used by the different operations to
+        generate a commitmsg file in the diffDir.
+        To be used by those operations which want to convey the
+        running of the corresponding operation by the user for
+        future reference.
+        sOp : the operation, by convention specified in CAPS.
+        """
+    ts = time.strftime(gsTimeStampFormat)
+    tFile = "{}-OP_{}-{}".format(ts, sOp, gsCOMMITMSG_FILESUFFIX)
+    theFile = os.path.join(me['diffDir'], tFile)
+    os.system("echo '{}' > {}".format(sMsg, theFile))
+
+
 def do_init(me):
+    """ The operation which has to be called first before doing
+        any other operation wrt ssvc repositories.
+        This creates the ssvc repository folder within the current
+        working directory from which the ssvc command is called
+        by the user.
+        """
     os.mkdir(me['baseDir'])
     os.mkdir(me['copyDir'])
     os.mkdir(me['diffDir'])
+    _commit_op(me, "INIT", "Initialised SSVC repository today")
 
 
 def do_save(me):
+    """ Internal operation called by the program at the end to
+        transfer the current runtime context to the disk store
+        of the repository.
+        """
     f = open(me['srcsFile'],"wt+")
     for l in me['files']:
         f.write(l)
@@ -58,6 +87,10 @@
 
 
 def do_load(me):
+    """ Internal operation called by the program at the beginning
+        to load the current runtime context from the disk store of
+        the repository.
+        """
     try:
         f = open(me['srcsFile'])
         for l in f:
@@ -68,10 +101,21 @@
 
 
 def do_dump(me):
+    """ User can use the dump operation to get the current runtime
+        context of the program.
+        Mainly useful for basic debugging purpose and not required
+        from normal usage perspective.
+        """
     print(me)
 
 
 def ssvccopy_mkdir(me, sDirs):
+    """ Helper mkdir logic, which creates not just the leaf dir
+        but also all the intermediate directories if required.
+
+        TOTHINK: As currently only copyDir maintains a directory
+        heirarchy within itself, its hardcoded for the same.
+        """
     cPath = me['copyDir']
     for cDir in sDirs.split(os.sep):
         cPath += (os.sep + cDir)
@@ -83,23 +127,32 @@
 
 
 def _cp(srcFile, destPath):
+    """ helper file copy logic, which translates to the underlying
+        os file copy command.
+        """
     os.system("cp {} {}".format(srcFile, destPath))
 
 
 def ssvccopy_cp(me, srcFile):
+    """ copy specified file into a mirrored directory heirarchy
+        in the copyDir folder of ssvc repository
+
+        TOTHINK: As currently only copyDir maintains a directory
+        heirarchy within itself, its hardcoded for the same.
+        """
     sDir = os.path.dirname(srcFile)
     destPath = os.path.join(me['copyDir'],sDir)
     _cp(srcFile, destPath)
 
 
-def _commit_op(me, sOp, sMsg):
-    ts = time.strftime(gsTimeStampFormat)
-    tFile = "{}-OP_{}-{}".format(ts, sOp, gsCOMMITMSG_FILESUFFIX)
-    theFile = os.path.join(me['diffDir'], tFile)
-    os.system("echo '{}' > {}".format(sMsg, theFile))
-
-
 def do_add(me, sFile):
+    """ The add operation of the ssvc repository.
+        It adds the specified file to the runtime list of files
+        that are tracked by ssvc.
+        It inturn copies the file to the copyDir, as the official
+        commited reference for the file.
+        It also generates a OP commit message.
+        """
     if sFile in me['files']:
         print("WARN:add: [{}] already in repo".format(sFile))
         return
@@ -112,6 +165,12 @@
 
 
 def _do_diff(me, tCur, bInteractive=False):
+    """ The helper logic which does the actual low level diff
+        operation, using the systems diff command.
+        Given the file to diff, it automatically identifies the
+        corresponding last commited copy of the same file in
+        the ssvc repository and compares against it.
+        """
     bDiff = False
     tOld = os.path.join(me['copyDir'], tCur)
     diffOk = os.system("diff -ub {} {}".format(tOld, tCur))
@@ -126,6 +185,12 @@
 
 
 def do_diff(me, bInteractive=False):
+    """ The diff operation of ssvc.
+        It will go throu all the files being tracked by ssvc and
+        cross checks if the last commited copy of the file within
+        ssvc (i.e copyDir) and the copy in the users working dir
+        match or else what is the difference.
+        """
     bDiffs = False
     for tCur in me['files']:
         if _do_diff(me, tCur, bInteractive):
@@ -135,10 +200,18 @@
 
 def _commit_filediff(me, ts, tCur):
     """ file diff helper for commit command
-        It generates the diff file related to commit.
-        It also tells if there was a diff/change wrt
-            the file being looked at, in the working directory
-            or if the working and saved copy are the same.
+        It generates the diff file for the specified file, which
+            relates to this commit.
+            The same is copied into the copyDir.
+            NOTE: The copyDir follows a flattened directory approach.
+            i.e there are no sub directories to mirror the working 
+            directory structure of the file. Instead the file path 
+            is stored as part of the file name itself by prefixing
+            it to the actual file name (dir seperator is replaced
+            with ^ for now).
+        It also tells if there was a diff/change wrt the file
+            being looked at, in the working directory or else
+            if the working and last commited copy are the same.
             If there is a change it returns True
         me: the context
         ts: the time stamp to use
@@ -157,10 +230,27 @@
 
 
 def _commit_filecopy(me,tCur):
+    """ file copy helper for commit command.
+        It copies the current version of the specified file in
+        the working directory into the copyDir of ssvc. Thus
+        making it the last commited copy of that file from ssvc
+        perspective.
+        """
     ssvccopy_cp(me, tCur)
 
 
 def do_commit(me):
+    """ The commit command | operation of ssvc.
+        It goes throu all the tracked files specified to ssvc,
+        and cross checks if there is any difference or not.
+        If any differences are found then
+        1. user is asked to provide a commit message
+        2. the differences of the tracked files are captured 
+           into the diffDir folder.
+        3. the current working directory version of the changed
+           files are backed up into copyDir, making them the
+           last commited copy for those files.
+        """
     if not do_diff(me, bInteractive=True):
         print("WARN:commit: No changes identified, so skipping commit...")
         return
