--- .simpsvc/copy/hkvc-simple-svc.py	2020-03-29 15:19:14.741547700 +0530
+++ hkvc-simple-svc.py	2020-03-29 15:23:20.758543852 +0530
@@ -202,6 +202,11 @@
             iArg += 1
 
 
+if len(sys.argv) == 1:
+    print("{}, v20200329IST1522, HanishKVC".format(sys.argv[0]))
+    print("usage: ssvc [init|dump|add|diff|commit|log] [args]")
+    exit()
+
 do_load(me)
 process_args(sys.argv[1:])
 do_save(me)
