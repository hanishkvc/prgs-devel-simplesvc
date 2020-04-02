--- .simpsvc/copy/hkvc-simple-svc.py	2020-04-01 16:31:47.995545183 +0530
+++ .simpsvc/cache/hkvc-simple-svc.py	2020-04-01 16:47:19.334564890 +0530
@@ -371,6 +371,17 @@
     return lOut
 
 
+def _cat(sFile, sHeader = None, bLess=False):
+    if sHeader != None:
+        print(sHeader)
+    f = open(sFile)
+    i = 0
+    for l in f:
+        print(l)
+        if bLess and ((i%25) == 0):
+            input("Press any key...")
+
+
 def do_log(me, bPatch=False, bLess=False):
     """ Generate a log of all commits till date.
         By default it only contains the contents of the commit messages.
@@ -396,12 +407,7 @@
             theFile = os.path.join(me['diffDir'], tFile)
             #print("\n\nINFO:log: #### {} #### \n".format(tFile))
             sPrefix = "\n\nINFO:{}: #### {} #### \n".format(sType, tFile)
-            if bLess:
-                theCmd = "less"
-            else:
-                theCmd = "cat"
-            os.system("echo '{}'".format(sPrefix))
-            os.system("{} {}".format(theCmd, theFile))
+            _cat(theFile, sPrefix, bLess)
 
 
 def do_edit(me, index):
