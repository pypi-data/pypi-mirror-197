from setuptools import setup, Extension
from ctypes import c_uint64, c_double, sizeof
from tempfile import mkstemp
from distutils.ccompiler import new_compiler
from distutils.sysconfig import customize_compiler
import subprocess
import os

# I tried to set-up this package according to PEP 517, but that
# as yet can't handle the building of extensions [1] so we need
# to do that here, possibly that changes later
# [1] https://stackoverflow.com/questions/66157987/

# librtree usually includes a config,h which defines various
# constants which configure the package, there's not much support
# for that in setuptools so we hack something together ourselves
# and use the 'define_macros' options to pass those values to the
# compile

defines = []

def defines_append(key, value=None):
    defines.append((key, value))

# The C-types used here must agree with the types hard-coded in
# types.h from librtree

defines_append('SIZEOF_RTREE_ID_T', str(sizeof(c_uint64)))
defines_append('SIZEOF_RTREE_COORD_T', str(sizeof(c_double)))

# these are weak replacements for the autoconf tests

cc = new_compiler()
customize_compiler(cc)
cc_path = cc.compiler[0]

def have_header(header):
    '''
    shellout to the c-compiler to see whether we can find
    the header
    '''
    print('checking for %s' % header, end=' ..')
    _, input_path = mkstemp(suffix='.h')
    with open(input_path, 'w') as st:
        st.write('#include <%s>' % header)
    command = [cc_path, '-E', input_path]
    result = subprocess.run(command, capture_output=True).returncode
    os.remove(input_path)
    if result == 0:
        print('. yes')
        return True
    else:
        print('. no')
        return False

def check_header(header):
    result = have_header(header)
    if result:
        variable = header.replace('/', '_').replace('.', '_').upper()
        defines_append('HAVE_%s' % variable, '1')
    return result

if have_header('jansson.h'):
    defines_append('WITH_JSON')

if (
        check_header('endian.h') or
        check_header('sys/endian.h') or
        check_header('libkern/OSByteOrder.h') or
        check_header('winsock2.h')
):
    defines_append('WITH_BSRT')

check_header('features.h')
if check_header('unistd.h'):
    # FIXME - need to actually test this available
    defines_append('HAVE_GETPAGESIZE')

# now back to regular setup.py

setup_args = dict(
    ext_package = 'librtree',
    ext_modules = [
        Extension(
            'pyrtree',
            [
                'src/librtree/bindex.c',
                'src/librtree/branch.c',
                'src/librtree/branches.c',
                'src/librtree/bsrt.c',
                'src/librtree/csv.c',
                'src/librtree/error.c',
                'src/librtree/json.c',
                'src/librtree/node.c',
                'src/librtree/package.c',
                'src/librtree/page.c',
                'src/librtree/postscript.c',
                'src/librtree/rect.c',
                'src/librtree/rectf.c',
                'src/librtree/rtree.c',
                'src/librtree/search.c',
                'src/librtree/split.c',
                'src/librtree/spvol.c',
                'src/librtree/state.c',
                'src/librtree/pyrtree.c'
            ],
            include_dirs = ['src/librtree'],
            libraries = ['jansson'],
            define_macros = defines
        )
    ]
)

setup(**setup_args)
