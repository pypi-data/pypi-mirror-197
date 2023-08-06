"""A wrapper around {py:class}`pyaedt.hfss.Hfss`
to manage the lifecycle of the AEDT application
in a custom way.
"""

# %% Import
from __future__ import annotations
from enum import Enum
from os import getcwd, mkdir, path
from typing import cast
from loguru import logger
import pyaedt
from pyaedt.application.Variables import VariableManager
from pyaedt.desktop import Desktop
from pyaedt.generic.general_methods import remove_project_lock
from pyaedt.hfss import Hfss
from pyaedt.modeler.modeler3d import Modeler3D
from pyaedt.modules.AdvancedPostProcessing import PostProcessor
from pyaedt.modules.MaterialLib import Materials


# %% Class
class SOLUTIONS:
    """Provides the names of default solution types
    as a enum. Created because
    {py:class}`pyaedt.generic.constants.SOLUTIONS`
    is not a enum."""

    class Hfss(Enum):
        """Provides HFSS solution types.
        Copied from PyAEDT definition.
        """

        DrivenModal = "Modal"
        DrivenTerminal = "Terminal"
        EigenMode = "Eigenmode"
        Transient = "Transient Network"
        SBR = "SBR+"
        Characteristic = "Characteristic"


class AEDTDesktop:
    """Represents a AEDT desktop session."""

    def __init__(
        self,
        specified_version: str | None = None,
        non_graphical: bool = True,
        new_desktop_session: bool = True,
        close_on_exit: bool = True,
        student_version: bool = False,
    ) -> None:
        """Create a new AEDT desktop.

        :param str | None specified_version: defaults to None
        :param bool non_graphical: defaults to True
        :param bool new_desktop_session: defaults to True
        :param bool close_on_exit: defaults to True
        :param bool student_version: defaults to False
        """

        logger.info("Initializing AEDT...")
        self._desktop = Desktop(
            specified_version=specified_version,
            non_graphical=non_graphical,
            new_desktop_session=new_desktop_session,
            close_on_exit=close_on_exit,
            student_version=student_version,
        )
        logger.info(f"AEDT initialized. ")

    def __enter__(self) -> AEDTDesktop:
        """
        :return AEDTDesktop: The object itself.
        """
        return self
    
    def __exit__(self) -> None:
        """Release AEDT."""
        res = self.desktop.release_desktop()
        if res:
            logger.info("[antcal.application.]")
    
    def __del__(self) -> None:
        """Destructor."""
        self.__exit__()

    @property
    def desktop(self) -> Desktop:
        """
        :return Desktop: The AEDT application
        """
        return self._desktop

    @property
    def process_id(self) -> int:
        """
        :return int: AEDT process ID
        """
        # pyright: reportOptionalMemberAccess = false
        return self.desktop.odesktop.GetProcessID()


class HFSS:
    """Represents the Pyaedt HFSS application."""

    def __init__(
        self,
        non_graphical: bool,
        design_name: str,
        solution_type: SOLUTIONS.Hfss,
        project_name: str = "project.aedt",
        project_dir: str = "projectfiles",
    ) -> None:
        """Initialize HFSS.

        :param bool non_graphical: Start without GUI or not.
        :param str design_name: Default design name.
        :param SOLUTIONS.Hfss solution_type: Solution type.
        :param str project_name: Project file name, defaults to "project.aedt"
        :param str project_dir: Project file path, defaults to "projectfiles"
        """
        self._project_dir = path.join(getcwd(), project_dir)
        if not path.exists(self._project_dir):
            mkdir(self._project_dir)
        self._project_path = path.join(self._project_dir, project_name)
        remove_project_lock(self._project_path)
        self._hfss = Hfss(
            self._project_path,
            design_name,
            solution_type,
            non_graphical=non_graphical,
            close_on_exit=True,
        )
        self.hfss.autosave_enable()
        self.hfss.change_material_override()
        print("[antcal.design.HFSS] HFSS initialized.")

    def __enter__(self) -> HFSS:
        """Return self in the context manager.

        :return HFSS: The object itself.
        """
        return self

    def __exit__(self) -> None:
        """Release HFSS when leaving the context manager."""
        print("[antcal.design.HFSS] Releasing HFSS...")
        res = self.release()
        if res:
            print("[antcal.design.HFSS] HFSS released successfully.")
        else:
            print("[antcal.design.HFSS] Failed releasing HFSS")
        return None

    def __del__(self) -> None:
        """Release HFSS when there's no more reference."""
        self.__exit__()

    def release(self) -> bool:
        """`release_desktop()` in PyAEDT."""
        return self.hfss.release_desktop()

    @property
    def hfss(self) -> Hfss:
        """Return the HFSS application."""
        return self._hfss

    @property
    def name(self) -> str:
        """Return the current HFSS design name."""
        return cast(str, self.hfss.design_name)

    @property
    def setup_name(self) -> str:
        """Return the current setup name"""
        return cast(str, self.hfss.analysis_setup)

    @property
    def variables(self) -> dict[str, str]:
        """Return the design variables.

        :Example:
        ```py
        {"xl_gnd": "10 mm"}
        ```
        """
        return {
            k: v.evaluated_value
            for k, v in self.variable_manager.design_variables.items()
        }

    @variables.setter
    def variables(self, variables: dict[str, str]) -> None:
        """Assign the design variables."""
        for item in variables.items():
            self.variable_manager.set_variable(*item)

    @property
    def modeler(self) -> Modeler3D:
        """Return the modeler."""
        return cast(Modeler3D, self.hfss.modeler)

    @property
    def materials(self) -> Materials:
        """Return the materials."""
        return self.hfss.modeler.materials

    @property
    def post(self) -> PostProcessor:
        """Return the post processor."""
        return cast(PostProcessor, self.hfss.post)

    @property
    def variable_manager(self) -> VariableManager:
        variable_manager = self.hfss.variable_manager
        if not variable_manager:
            raise AttributeError(variable_manager)
        return variable_manager

    def solve(self, setup_name: str) -> None:
        """Solve the current setup.

        :param str setup_name: The name of the setup to solve."""
        self.hfss.save_project()
        assert self.hfss.validate_simple()
        self.hfss.analyze_setup(setup_name)
