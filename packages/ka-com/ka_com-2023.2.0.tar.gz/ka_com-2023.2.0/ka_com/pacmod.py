# coding=utf-8

# import os
from os import path as os_path
import pkg_resources

from typing import Any, Dict


class Pacmod:
    """ Package Module Management
    """
    def sh(root_cls, tenant) -> Dict:
        """ Show Pacmod Dictionary
        """
        a_pacmod = root_cls.__module__.split(".")
        package = a_pacmod[0]
        module = a_pacmod[1]
        d_pacmod = {}
        d_pacmod['tenant'] = tenant
        d_pacmod['package'] = package
        d_pacmod['module'] = module
        # print(f"d_pacmod = {d_pacmod}")
        return d_pacmod

    class Cfg:
        """ Configuration Sub Class of Package Module Class
        """
        @staticmethod
        def sh_path(pacmod: Dict) -> str:
            """ show directory
            """
            package = pacmod['package']
            module = pacmod['module']
            dir = f"{package}.data"
            return pkg_resources.resource_filename(dir, f"{module}.yml")

    class Pmd:
        """ Package Sub Class of Package Module Class
        """
        @staticmethod
        def sh_path_keys(
                pacmod: Any,
                filename: str = 'keys.yml') -> str:
            """ show directory
            """
            package = pacmod['package']
            dir = f"{package}.data"
            return pkg_resources.resource_filename(dir, filename)

    class Path:
        class Data:
            class Dir:
                """ Data Directory Sub Class
                """
                @staticmethod
                def sh(pacmod: Dict, type: str) -> str:
                    """ show Data File Path
                    """
                    package = pacmod['package']
                    module = pacmod['module']
                    return f"/data/{package}/{module}/{type}"

        @classmethod
        def sh(
                cls, pacmod: Dict,
                type: str,
                suffix: str,
                pid,
                ts,
                **kwargs) -> str:
            """ show type specific path
            """
            filename = kwargs.get('filename')
            if filename is not None:
                filename_ = filename
            else:
                filename_ = type

            sw_filename_pid_ts = kwargs.get('sw_filename_pid_ts', True)
            if sw_filename_pid_ts is None:
                sw_filename_pid_ts = True

            dir = cls.Data.Dir.sh(pacmod, type)
            if sw_filename_pid_ts:
                # pid = str(Com.pid)
                # ts = str(Com.ts_start)
                file_path = os_path.join(
                    dir, f"{filename_}_{pid}_{ts}.{suffix}")
            else:
                file_path = os_path.join(dir, f"{filename_}.{suffix}")
            return file_path

        @classmethod
        def sh_pattern(
                cls,
                pacmod: Dict,
                type: str,
                suffix: str,
                **kwargs) -> str:
            """ show type specific path
            """
            filename = kwargs.get('filename')
            dir = cls.Data.Dir.sh(pacmod, type)
            return os_path.join(dir, f"{filename}*.{suffix}")

        class Log:

            @staticmethod
            def sh_cfg(pacmod=None, filename='log.yml'):
                """ show directory
                """
                if pacmod is None:
                    pacmod = {'package': 'ka_utg', 'module': 'com'}
                return pkg_resources.resource_filename(
                    f"{pacmod['package']}.data", filename
                )
