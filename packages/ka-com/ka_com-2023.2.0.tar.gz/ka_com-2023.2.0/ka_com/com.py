# coding=utf-8

import calendar
import logging
import logging.config
import os
# import pkg_resources
import time

from typing import Any, Dict

from ka_com.ioc import Yaml
from ka_com.ioc import Jinja2
from ka_com.pacmod import Pacmod


class Com:

    """Communication Class
    """
    sw_init = False
    # cfg: Dict = {}
    pid = None
    Log = None
    pacmod_curr: Dict = {}
    ts_start = None
    ts_end = None
    ts_etime = None
    d_timer: Dict = {}

    class Main:

        class Log:

            sw_init = False
            cfg: Dict = {}
            log = None

            @classmethod
            def read(
                    cls, pacmod: Dict) -> Any:
                path = Pacmod.Path.Log.sh_cfg(filename='log.main.tenant.yml')
                print("==================================")
                print(f"path = {path}")
                print("==================================")
                log_main = Jinja2.read(
                    path,
                    tenant=pacmod['tenant'],
                    package=pacmod['package'],
                    module=pacmod['module'],
                    pid=Com.pid,
                    ts=Com.ts_start)
                return log_main

            @classmethod
            def init_handler(cls, handler, key, value):
                cls.cfg['handlers'][handler][key] = value

            @classmethod
            def set_level(cls, sw_debug):
                if sw_debug:
                    cls.init_handler(
                      'main_debug_console', 'level', logging.DEBUG)
                    cls.init_handler(
                      'main_debug_file', 'level', logging.DEBUG)
                else:
                    cls.init_handler(
                      'main_debug_console', 'level', logging.INFO)
                    cls.init_handler(
                      'main_debug_file', 'level', logging.INFO)

            @classmethod
            def init(
                    cls, **kwargs) -> None:
                sw_debug = kwargs.get('sw_debug')
                if cls.sw_init:
                    return
                cls.sw_init = True

                cls.cfg = cls.read(Com.pacmod_curr)
                cls.set_level(sw_debug)

                logging.config.dictConfig(cls.cfg)
                cls.log = logging.getLogger('main')
                Com.Log = cls.log

    class Mgo:

        client = None

    class Person:

        class Log:

            cfg: Dict = {}
            log = None

            @classmethod
            def read(
                    cls, pacmod: Dict, person: Any) -> Any:
                path = Pacmod.Path.Log.sh_cfg(filename='log.person.yml')
                return Jinja2.read(
                    path,
                    package=pacmod['package'],
                    module=pacmod['module'],
                    person=person,
                    pid=Com.pid,
                    ts=Com.ts_start)

            @classmethod
            def init_handler(cls, handler, key, value):
                cls.cfg['handlers'][handler][key] = value

            @classmethod
            def set_level(cls, person, sw_debug):
                if sw_debug:
                    cls.init_handler(
                      f'{person}_debug_console', 'level', logging.DEBUG)
                    cls.init_handler(
                      f'{person}_debug_file', 'level', logging.DEBUG)
                else:
                    cls.init_handler(
                      f'{person}_debug_console', 'level', logging.INFO)
                    cls.init_handler(
                      f'{person}_debug_file', 'level', logging.INFO)

            @classmethod
            def init(cls, pacmod: Dict, person, sw_debug) -> None:
                # if cls.log is not None:
                #     return
                cls.cfg = cls.read(pacmod, person)
                cls.set_level(person, sw_debug)

                logging.config.dictConfig(cls.cfg)
                cls.log = logging.getLogger(person)
                Com.Log = cls.log

    class App:

        sw_init = False
        httpmod = None
        sw_replace_keys = None
        keys = None
        reqs: dict = {}
        app: dict = {}

        @classmethod
        def init(
                cls, **kwargs: Any) -> None:
            if cls.sw_init:
                return
            cls.sw_init = True

            cls.httpmod = kwargs.get('httpmod')
            cls.sw_replace_keys = kwargs.get('sw_replace_keys', False)

            try:
                if cls.sw_replace_keys:
                    pacmod = kwargs.get('pacmod_curr')
                    cls.keys = Yaml.read(Pacmod.Pmd.sh_path_keys(pacmod))
            except Exception as e:
                if Com.Log is not None:
                    Com.Log.error(e, exc_info=True)
                raise

    class Cfg:

        @classmethod
        def init(cls, pacmod):
            """ the package data directory has to contain a __init__.py
                file otherwise the objects notation {package}.data to
                locate the package data directory is invalid
            """
            return Yaml.read(Pacmod.Cfg.sh_path(pacmod))

    class Exit:

        sw_critical = False
        sw_stop = False
        sw_interactive = False

    @classmethod
    def init(cls, **kwargs):
        """ set log and application (module) configuration
        """
        if cls.sw_init:
            return
        cls.sw_init = True

        cls.pacmod_curr = kwargs.get('pacmod_curr')
        cls.ts_start = calendar.timegm(time.gmtime())
        cls.pid = os.getpid()

        cls.cfg = cls.Cfg.init(cls.pacmod_curr)
        cls.Main.Log.init(**kwargs)
        cls.App.init(**kwargs)

    @classmethod
    def terminate(cls):
        """ set log and application (module) configuration
        """
        cls.Log = cls.Main.Log.log
        cls.ts_end = calendar.timegm(time.gmtime())
        cls.ts_etime = cls.ts_end - cls.ts_start
