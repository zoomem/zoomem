DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/gdb.py"
DIR2="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.gdbinit"
DIR3="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/python"
rm -R /usr/share/gdb/python/gdb/zoomem
rm ~/.gdbinit

mkdir /usr/share/gdb/python/gdb/zoomem
cp $DIR /usr/share/gdb/python/gdb/zoomem
cp $DIR2 ~/
cp -r $DIR3 /usr/share/gdb/python/gdb
