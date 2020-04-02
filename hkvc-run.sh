
PRGFILE=hkvc-simple-svc.py
INSTALLPATH=~/bin

function check_install() {
	md5sum $INSTALLPATH/$PRGFILE
	md5sum $PRGFILE
}

function install() {
	check_install
	cp $PRGFILE $INSTALLPATH/
	echo "installed"
	check_install
}

echo "$@"
$@
