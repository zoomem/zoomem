DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/gdb.py"
DIR2="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.gdbinit"
rm  /usr/share/gdb/python/gdb/zoomem
rm ~/.gdbinit

mkdir /usr/share/gdb/python/gdb/zoomem
cp $DIR /usr/share/gdb/python/gdb/zoomem
cp $DIR2 ~/
