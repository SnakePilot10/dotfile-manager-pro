# Maintainer: SnakePilot10 <SnakePilot10@users.noreply.github.com>
pkgname=dotfile-manager-pro
pkgver=2.0.0
pkgrel=1
pkgdesc="Professional Dotfile Manager with TUI and Git integration"
arch=('any')
url="https://github.com/SnakePilot10/dotfile-manager-pro"
license=('MIT')
depends=('python' 'python-typer' 'python-rich' 'python-textual')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("git+$url.git")
sha256sums=('SKIP')

build() {
    cd "$pkgname"
    python -m build --wheel --no-isolation
}

package() {
    cd "$pkgname"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
