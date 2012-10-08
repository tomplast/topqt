pkgname=topqt-git
pkgver=20121008
pkgrel=1
pkgdesc="A simple process listing tool written in Python with a daemon and a cli client. "
arch=('i686 x86_64')
url="git://github.com/tomplast/topqt.git"
license=('MIT')
depends=('pyqt')
makedepends=('git')

_gitroot=git://github.com/tomplast/topqt.git
_gitname=topqt


build() {

    cd $startdir/src

    msg "Connecting to GIT server...."

    if [ -d $startdir/src/$_gitname ] ; then
        cd $_gitname && git pull origin
        msg "The local files are updated."
    else
        git clone $_gitroot
        cd $_gitname
    fi

mkdir -p $startdir/pkg/usr/{bin,share}
install -D -m755 $startdir/src/$_gitname/topqt.py $startdir/pkg/usr/bin/topqt.py
}
