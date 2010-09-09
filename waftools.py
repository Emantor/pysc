#***********************************************************************#
#* Project:    HW-SW SystemC Co-Simulation SoC Validation Platform     *#
#*                                                                     *#
#* File:       waftools.py                                             *#
#*             python file containing filesystem search helpers        *#
#*             to easiefy the wscript configuration routine.           *#
#*                                                                     *#
#* Modified on $Date$   *#
#*          at $Revision$                                         *#
#*                                                                     *#
#* Principal:  European Space Agency                                   *#
#* Author:     VLSI working group @ IDA @ TUBS                         *#
#* Maintainer: Rolf Meyer                                              *#
#***********************************************************************#

import os
import os.path
import fnmatch
import Utils, Environment, Options, Build

#
# Find all project targets:
# ./waf list
#
def set_options(opt): 
  conf = opt.get_option_group("--prefix")
  conf.set_title("Common Configuration Options")
  cpp = opt.get_option_group("--check-cxx-compiler")
  cpp.set_title("C++ Compiler Configuration Options")
  inst = opt.get_option_group("--force")
  inst.remove_option("--destdir")
  inst.remove_option("--force")
  inst.set_title("Configuration Options")
  inst.set_description("""All following options can be provided to the configure rule.""")
  

def target_list(ctx): 
  """returns a list of all targets"""

  bld = Build.BuildContext() 
  proj = Environment.Environment(Options.lockfile) 
  bld.load_dirs(proj['srcdir'], proj['blddir']) 
  bld.load_envs()

  bld.add_subdirs([os.path.split(Utils.g_module.root_path)[0]]) 

  names = set([])
  for x in bld.all_task_gen: 
    try:
      names.add(x.name or x.target)
    except AttributeError:
      pass

  lst = list(names)
  lst.sort()
  print "All targets:"
  for name in lst:
    print " ", name

def target_docs(bld):
  """build source code documentation"""
  import subprocess
  subprocess.call(["doxygen", "Doxyfile"]) 

## Nice to have to set svn props:
## It's maybe wothy to make a target out of it
def setprops(bld):
  """set svn properties for all files (searches for $Date$)"""
  import subprocess
  # grep --exclude=**.svn** -rn '\$Date\$' tlmsignals models | cut -f1 -d: | xargs -I {} svn propset svn:keywords "Date Revision" {}
  grep = subprocess.Popen(["grep", "--exclude=**.svn**", "-rn", "\$Date\$", "signalkit", "models", "tests"], stdout=subprocess.PIPE)
  cut = subprocess.Popen(["cut", "-f1", "-d:"], stdin=grep.stdout, stdout=subprocess.PIPE)
  xargs = subprocess.Popen(["xargs", "-I", "{}", "svn", "propset", "svn:keywords", "Date Revision", "{}"], stdin=cut.stdout, stdout=subprocess.PIPE)
  print xargs.communicate()[0]        

Utils.g_module.__dict__['list'] = target_list
Utils.g_module.__dict__['docs'] = target_docs
Utils.g_module.__dict__['setprops'] = setprops

#
# For external resources
#

def getdirs(base = '.', excludes = []):
    """Return recursively all subdirectories of base, exept directories matching excludes."""
    result = []
    for root, dirs, files in os.walk(base):
        if any([fnmatch.fnmatchcase(root, exc) for exc in excludes]):
            continue
        result.append(root)
    return result

def getfiles(base, ext, excludes):
    """Return recursively all files in base with an extension in ext excluding all who matching excludes"""
    result = []
    for root, dirs, files in os.walk(base):
        for cdir in dirs:
            if any([fnmatch.fnmatchcase(os.path.join(root, cdir), exc) for exc in excludes]):
                del(cdir)
        
        for cfile in files:
            if any([fnmatch.fnmatchcase(os.path.join(root, cfile), exc) for exc in excludes]):
                continue
            if any([fnmatch.fnmatchcase(os.path.join(root, cfile), e) for e in ext]): 
                result.append(os.path.join(root, cfile))
            
    return result

if __name__ == "__main__":
    """simple test"""
    for dirs in getdirs('/home/hwswsim/tools/greensocs-4.0.0/greenreg', ['*test*','*example*']):
        print dirs

    for cxx in getfiles('/home/hwswsim/tools/greensocs-4.0.0/greenreg', ['*.cpp'], ['*test*', '*example*']):
        print cxx
