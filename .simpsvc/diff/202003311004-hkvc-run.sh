--- .simpsvc/copy/hkvc-run.sh	2020-03-29 18:03:42.939393361 +0530
+++ hkvc-run.sh	2020-03-31 10:03:58.018635802 +0530
@@ -8,7 +8,10 @@
 }
 
 function install() {
+	check_install
 	cp $PRGFILE $INSTALLPATH/
+	echo "installed"
+	check_install
 }
 
 echo "$@"
