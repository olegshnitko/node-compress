import Options
from os import unlink, symlink, popen
from os.path import exists 

srcdir = "."
blddir = "build"
VERSION = "0.1.5"

def set_options(opt):
  opt.tool_options("compiler_cxx")

  opt.add_option('--with-gzip', dest='gzip', action='store_true', default=True)
  opt.add_option('--no-gzip', dest='gzip', action='store_false')
  opt.add_option('--with-bzip', dest='bzip', action='store_true', default=False)
  opt.add_option('--no-bzip', dest='bzip', action='store_false')

def configure(conf):
  conf.check_tool("compiler_cxx")
  conf.check_tool("node_addon")

  conf.env.DEFINES = []
  conf.env.USELIB = []

  if Options.options.gzip:
    conf.check_cxx(lib='z',
                   uselib_store='ZLIB',
                   mandatory=True)
    conf.env.DEFINES += [ 'WITH_GZIP' ]
    conf.env.USELIB += [ 'ZLIB' ]

  if Options.options.bzip:
    conf.check_cxx(lib='bz2',
                   uselib_store='BZLIB',
                   mandatory=True)
    conf.env.DEFINES += [ 'WITH_BZIP' ]
    conf.env.USELIB += [ 'BZLIB' ]

def build(bld):
  obj = bld.new_task_gen("cxx", "shlib", "node_addon")
  obj.cxxflags = ["-D_FILE_OFFSET_BITS=64", "-D_LARGEFILE_SOURCE", "-Wall"]
  obj.target = "compress-bindings"
  obj.source = "src/compress.cc"
  obj.defines = bld.env.DEFINES
  obj.uselib = bld.env.USELIB
  

def shutdown():
  # HACK to get compress.node out of build directory.
  # better way to do this?
  if Options.commands['clean']:
    if exists('compress-bindings.node'): unlink('compress-bindings.node')
    if exists('compress.js'): unlink('compress.js')
  else:
    if (exists('build/default/compress-bindings.node') and
        not exists('compress-bindings.node')):
      symlink('build/default/compress-bindings.node', 'compress-bindings.node')
    if not exists('compress.js'):
      symlink('lib/compress.js', 'compress.js')
