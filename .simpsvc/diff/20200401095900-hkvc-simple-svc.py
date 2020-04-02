--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 09:32:52.034013291 +0530
+++ hkvc-simple-svc.py	2020-04-01 09:58:47.594046207 +0530
@@ -353,14 +353,26 @@
 
 def do_edit(me, index):
     """ Edit index specified commit message 
-        index starts from 0, with 0 being the latest commit.
-        one can use -1 for the last item, -2 for last but one
+
+        index starts from 0, with 
+        0 being the latest commit,
+        1 being the previous-to-latest commit 
+        and so on.
+    
+        One can even use -ve index. In which case 
+        -1 is oldest (i.e 1st) commit, 
+        -2 is one-after-oldest (2nd) commit
         and so on.
         """
     lFiles = sorted(os.listdir(me['diffDir']), reverse=True)
-    print(lFiles)
-    lFiles = filter(lambda x: x.endswith(gsCOMMITMSG_FILESUFFIX), lFiles)
-    print(lFiles)
+    dprint(lFiles)
+    lFiles = list(filter(lambda x: x.endswith(gsCOMMITMSG_FILESUFFIX), lFiles))
+    dprint(lFiles)
+    try:
+        theFile = os.path.join(me['diffDir'], lFiles[index])
+        os.system("vim {}".format(theFile))
+    except IndexError:
+        print("WARN:edit: specify a valid index")
 
 
 def peek_ingroup(grp, index):
