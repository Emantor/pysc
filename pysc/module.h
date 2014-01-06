#ifndef PYSC_MODULE_H
#define PYSC_MODULE_H

#include <Python.h>

class PyScModule {
  public:
    typedef void (*init_f)(void);
    PyScModule(init_f funct = NULL);
    operator PyThreadState*() { return module_thread; };
    operator PyInterpreterState*() { return module_thread->interp; };
    static void registerEmbedded();
    bool embedded;
  private:
    static PyScModule *reg;
    void initModule();

    PyThreadState *module_thread;
    init_f funct;
    PyScModule *next;
};

#define PyScRegisterSWIGModule(name) \
  extern "C" { \
    void init_##name(void); \
  }; \
  static PyScModule __pysc_module(init_##name); \
  volatile PyScModule *__pysc_module_##name = &__pysc_module;

#define PyScThisModule() \
  (__pysc_module)

#define PyScRegisterEmbeddedModules() \
  PyScModule::registerEmbedded();

#define PyScIncludeModule(name) \
  extern PyScModule *__pysc_module_##name; \
  __pysc_module_##name->embedded = true;

#endif // Registry