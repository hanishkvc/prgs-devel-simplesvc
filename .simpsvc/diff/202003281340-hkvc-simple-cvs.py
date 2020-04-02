--- .simpcvs/copy/hkvc-simple-cvs.py	2020-03-28 13:35:50.427359831 +0530
+++ hkvc-simple-cvs.py	2020-03-28 13:39:30.794364494 +0530
@@ -104,6 +104,9 @@
 
 
 def do_commit(me):
+    if not do_diff(me, bInteractive=True):
+        print("WARN:commit: No changes identified, so skipping commit...")
+        return
     ts = time.strftime("%Y%m%d%H%M")
     fnCommitMsg = "/tmp/{}-commitmsg".format(ts)
     os.system("vim {}".format(fnCommitMsg))
