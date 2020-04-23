--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-02 03:24:32.000000000 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-23 16:57:44.351174832 +0530
@@ -192,10 +192,10 @@
         TOTHINK: Should I generate a OP commit message.
         """
     if sFile in me['files']:
-        print("INFO:add: [{}] already in repo".format(sFile))
+        print("INFO:add: [{}] in repo, to cacheDir".format(sFile))
     else:
         me['files'].append(sFile)
-        print("INFO:add: [{}] new file being added to repo".format(sFile))
+        print("INFO:add: [{}] new file to repo and cacheDir".format(sFile))
     #ts = time.strftime(gsTimeStampFormat)
     sDir = os.path.dirname(sFile)
     pathDest = ssvc_mkdir(me, me['cacheDir'], sDir)
@@ -215,7 +215,7 @@
     bDiff = False
     tOld = os.path.join(sOldBasePath, tCur)
     tNew = os.path.join(sNewBasePath, tCur)
-    diffOk = os.system("diff --unidirectional-new-file -ub {} {}".format(tOld, tNew))
+    diffOk = os.system("diff --color --unidirectional-new-file -ub {} {}".format(tOld, tNew))
     if diffOk != 0:
         if bInteractive:
             input("WARN:diff:Changes or Error?:{}\nPress any key to continue...".format(tCur))
