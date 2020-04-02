--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 17:04:33.623586777 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 19:50:31.279028636 +0530
@@ -27,6 +27,7 @@
         name itself.
     cacheDir: directory containing files that require to be
         commited.
+        It mirrors the directory structure of the original files
     srcsFile: the list of source files being tracked
 """
 me = {
@@ -47,6 +48,10 @@
 DLVL_DEFAULT=gDBGLVL
 DLVL_DBUG = 11
 def dprint(sMsg, dbgLvl=DLVL_DEFAULT):
+    """ Debug print, which prints the given string, only if the
+        debug level specified for the string, is lower than the
+        current system debug level.
+        """
     if (dbgLvl < gDBGLVL):
         print(sMsg)
 
@@ -117,6 +122,9 @@
     """ Helper mkdir logic, which creates not just the leaf dir
         but also all the intermediate directories if required.
 
+        It duplicates the sDirs directory | path heirarchy in
+        the sBasePath directory.
+
         NOTE: Normally used when copying something into copyDir
         or to the cacheDir. As these maintain the directory
         hierarchy of the tracked files, when copied into them.
@@ -139,8 +147,19 @@
 
 
 def ssvc_cp(me, srcFile, sBaseSrcPath, sBaseDestPath):
-    """ copy specified file into a mirrored directory heirarchy
-        in the specified folder.
+    """ copy specified file from the specified source directory
+        into a mirrored directory heirarchy in the specified
+        destination folder.
+
+        srcFile : the given file can also contain a relative
+        path info as part of it. In which case it is copied
+        to the same path within the specified destination dir.
+
+        sBaseSrcPath : the source directory which contains the
+        specified srcFile (including srcFile's relative path).
+
+        sBaseDestPath : the destination directory.
+
         It is normally used to copy files either into cacheDir
         or to the copyDir of ssvc repository, based on whether
         it is a add operation or commit operation.
@@ -156,8 +175,10 @@
 
 def do_add(me, sFile):
     """ The add operation of the ssvc repository.
+
         It adds the specified file to the runtime list of files
-        that are tracked by ssvc, if not already there.
+        that are tracked by ssvc, if its not already there.
+
         It inturn copies the file to cacheDir, so that it can
         be commited when requested later.
         TOTHINK: Should I generate a OP commit message.
@@ -167,10 +188,7 @@
     else:
         me['files'].append(sFile)
         print("INFO:add: [{}] new file being added to repo".format(sFile))
-    ts = time.strftime(gsTimeStampFormat)
-    # _commit_filediff needs to occur b4 ssvccopy_cp
-    # bcas otherwise ssvccopy_cp will copy the file into copyDir
-    # and filediff wont be able to generate the diff file
+    #ts = time.strftime(gsTimeStampFormat)
     sDir = os.path.dirname(sFile)
     pathDest = ssvc_mkdir(me, me['cacheDir'], sDir)
     ssvc_cp(me, sFile, ".", me['cacheDir'])
@@ -181,9 +199,10 @@
 def _do_difffile(me, tCur, sOldBasePath, sNewBasePath, bInteractive=False):
     """ The helper logic which does the actual low level diff
         operation, using the systems diff command.
-        Given the file to diff, it automatically identifies the
-        corresponding last commited copy of the same file in
-        the ssvc repository and compares against it.
+
+        Given the file to diff, and its old-copy path and the
+        new-copy path, it compares the two versions of the file
+        and returns true, if there is any difference between them.
         """
     bDiff = False
     tOld = os.path.join(sOldBasePath, tCur)
@@ -191,7 +210,7 @@
     diffOk = os.system("diff --unidirectional-new-file -ub {} {}".format(tOld, tNew))
     if diffOk != 0:
         if bInteractive:
-            input("WARN:diff:Changes:{}\nPress any key to continue...".format(tCur))
+            input("WARN:diff:Changes or Error?:{}\nPress any key to continue...".format(tCur))
         bDiff = True
     else:
         if bInteractive:
@@ -204,19 +223,19 @@
         It will go throu all the files being tracked by ssvc and
         cross checks if 
         
-        CopyDir & WorkingDir (default):
+        LC-WD i.e CopyDir & WorkingDir (default):
         the last commited copy of the file within ssvc (i.e copyDir) 
         and the copy in the users working dir
 
-        CacheDir & WorkingDir:
+        CA-WD i.e CacheDir & WorkingDir:
         the copy of the file within ssvc's cacheDir and the copy
         in the users working dir
         
-        CopyDir & CacheDir:
+        LC-CA i.e CopyDir & CacheDir:
         the last commited copy of the file within ssvc (i.e copyDir) 
         and the copy of the file within ssvc's cacheDir and the copy
 
-        match or else what is the difference.
+        match or else show what is the difference.
         """
     # Setup paths
     if sMode == "CA-WD":
@@ -507,6 +526,9 @@
     print("\t rare <cmd>'s are editcmsg")
     print("\t optional args")
     print("\t <log> --patch : also print the patchs associated with each commit")
+    print("\t <diff> --LC-WD : print diff between last commit and working dir")
+    print("\t <diff> --LC-CA : print diff between last commit and cache dir")
+    print("\t <diff> --CA-WD : print diff between cache dir and working dir")
     exit()
 
 
