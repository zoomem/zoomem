source /usr/share/gdb/python/gdb/zoomem/gdb.py

python
import sys
sys.path.insert(0, '/usr/share/gdb/python/gdb/python')
from libstdcxx.v6.printers import register_libstdcxx_printers
register_libstdcxx_printers (None)
end
