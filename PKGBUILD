pkgname=mmo-launcher
pkgver=1.0.0
pkgrel=1
pkgdesc="Custom MMO game launcher using PyQt6 + UMU"
arch=('any')
depends=('python-pyqt6' 'faugus' 'umu')
source=('gui.py' 'installer.py' 'launcher.py' 'config.yaml')
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
  mkdir -p "$pkgdir/usr/share/mmo-launcher"
  cp gui.py installer.py launcher.py config.yaml "$pkgdir/usr/share/mmo-launcher/"

  mkdir -p "$pkgdir/usr/bin"
  echo -e '#!/bin/sh\npython /usr/share/mmo-launcher/gui.py' > "$pkgdir/usr/bin/mmo-launcher"
  chmod +x "$pkgdir/usr/bin/mmo-launcher"
}
