# sudo docker run -it --rm -v $(pwd):/src quay.io/pypa/manylinux2014_x86_64 /bin/bash

# CentOS 7 (glibc 2.17) or later
TARGET=manylinux2014_x86_64
SRCDIR=/src
cd $SRCDIR
rm -rf $SRCDIR/dist

for dir in /opt/python/*/; do
    rm -rf $SRCDIR/_skbuild $SRCDIR/build $SRCDIR/pyhanja.egg-info
    $dir/bin/python -m build --wheel
done

for file in $SRCDIR/dist/*; do
    /usr/local/bin/auditwheel repair --wheel-dir $SRCDIR/dist/manylinux --plat $TARGET $file
done
