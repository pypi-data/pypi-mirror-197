from __future__ import annotations

import contextlib
import functools
import logging
import pathlib
import time
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from subprocess import CompletedProcess
from typing import Generator
from typing import Literal

from me_setups.boards.types import BoardType
from me_setups.components.eqs import CoreType
from me_setups.components.eqs import EyeQ5
from me_setups.components.eqs import OSType
from me_setups.components.mcs import Mcs
from me_setups.components.mcu import Mcu
from me_setups.components.mcu import McuType


DEFAULT_PBCM_PORTS = {
    "0000": "/dev/EQ5_PBCM_0000",
    "0001": "/dev/EQ5_PBCM_0001",
    "0010": "/dev/EQ5_PBCM_0010",
    "0011": "/dev/EQ5_PBCM_0011",
}


class Gas52Board:
    eqs: list[EyeQ5]
    mcu: Mcu

    def __init__(
        self,
        eqs: list[EyeQ5] | None = None,
        mcu: Mcu | None = None,
        board_type: BoardType = BoardType.GAS52,
        board_name: str = "GAS52-B4",
        board_rev: str = "0x3",
    ) -> None:
        """\
            Gas52 Board, the board has 4 Mid EQs (2*High) and Mcu.
            If there is an MCS connected it will also be a part of the board.
            If no eqs or mcu provided creates from default (using farm standart).

        Args:
            eqs (list[EyeQ5] | None, optional): list of EQs. Defaults to None.
            mcu (Mcu | None, optional): _description_. Defaults to None.
            board_type (BoardType, optional): type of board.
              Defaults to BoardType.GAS52.
            board_name (str, optional): name of the board.
              Defaults to "GAS52-B4".
            board_rev (str, optional): rev of the board.
              Defaults to "0x3".
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.eqs = eqs if eqs else self.create_eqs()
        self.mcu = mcu if mcu else self.create_mcu()
        self.board_type = board_type
        self.board_name = board_name
        self.board_rev = board_rev
        self._sniffing = False

    @functools.cached_property
    def conns(self) -> list[EyeQ5 | Mcu | Mcs] | list[EyeQ5 | Mcu]:
        """get all connections

        Returns:
            list[EyeQ5 | Mcu | Mcs] | list[EyeQ5 | Mcu]: All serial connections
        """
        conns: list[EyeQ5 | Mcu | Mcs] | list[EyeQ5 | Mcu]
        conns = self.eqs + [self.mcu]
        if self.mcs is not None:
            conns = conns + [self.mcs]
        return conns

    @functools.cached_property
    def shiq(self) -> EyeQ5:
        """get the ShiQ"""
        return self.eqs[1]

    @functools.cached_property
    def mcs(self) -> Mcs | None:
        """get the MCS

        Returns:
            Mcs | None: MCS if mcs is connected, (if `/dev/MCS` exists)
        """
        if pathlib.Path("/dev/MCS").exists():
            return Mcs("MCS", "/dev/MCS")
        else:
            return None

    @contextlib.contextmanager
    def sniff(
        self,
        log_folder: pathlib.Path | str,
        mode: Literal["a", "w"] = "a",
    ) -> Generator[None, None, None]:
        """\
            contextmanager for sniffing all conns.
            This will create a log folder and log file for each conn inside.

        Args:
            log_folder (pathlib.Path | str): path to log folder.
            mode (Literal['a', 'w'], optional): the mode of file (like open()).
              Defaults to 'a'.
        """
        self.config_log_files(log_folder, mode)
        try:
            self.start_sniffing()
            yield
        finally:
            if self._sniffing:
                self.stop_sniffing()

    def start_sniffing(self) -> None:
        """start the sniffing thread for each conn"""
        if self._sniffing:
            return None

        self._sniffing = True
        for conn in self.conns:
            conn.serial.start_sniffing()

    def stop_sniffing(self) -> None:
        """stop the sniffing thread for each conn"""
        if not self._sniffing:
            return None

        for conn in self.conns:
            conn.serial.stop_sniffing()
        self._sniffing = False

    def get_eyeq(self, chip: int, mid: int) -> EyeQ5:
        """get eq using chip and mid

        Args:
            chip (int): the chip index of the eq
            mid (int): the mid index of the eq

        Returns:
            EyeQ5: eq PB<chip><mid>
        """
        return self.eqs[chip * 2 + mid]

    def config_log_files(
        self,
        log_folder: pathlib.Path | str,
        mode: Literal["w", "a"] = "a",
    ) -> None:
        """config log files for every conn in specific log_folder

        Args:
            log_folder (pathlib.Path | str): path to log folder.
            mode (Literal['a', 'w'], optional): the mode of file (like open()).
              Defaults to 'a'.
        """
        self.logger.debug(f"configuring log folder - {str(log_folder)!r}")
        log_folder = pathlib.Path(log_folder)
        for conn in self.conns:
            conn.config_serial_log_file(log_folder / f"{conn.name}.log", mode)

    def close_serials(self) -> None:
        """close all serials conns"""
        for conn in self.conns:
            conn.logger.debug("closing serial")
            conn.serial.close()

    def open_serials(self) -> None:
        """opening all serials conns"""
        for conn in self.conns:
            if not conn.serial.is_open:
                conn.logger.debug("opening serial")
                conn.serial.open()

    def restart_serials(self) -> None:
        """restart all serials conns, close and open"""
        self.close_serials()
        self.open_serials()

    def run_ssh_cmd_all(self, cmd: str) -> list[CompletedProcess[str]]:
        """run ssh command on all eqs.

        Args:
            cmd (str): the command to run

        Returns:
            list[CompletedProcess[str]]: list off all commands proccesses
        """
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            fs = [executor.submit(eq.run_ssh_cmd, cmd) for eq in self.eqs]
            results = [f.result() for f in as_completed(fs)]
        return results

    def run_serial_cmd_all(self, cmd: str) -> None:
        """run serial command on all eqs.

        Args:
            cmd (str): the command to run
        """
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            fs = [executor.submit(eq.run_serial_cmd, cmd) for eq in self.eqs]
            results = [f.result() for f in as_completed(fs)]
        for _ in results:
            pass
        return None

    def wait_for_msg_all(self, msg: bytes, timeout: float) -> list[bytes]:
        """wait for serial msg on all eqs.

        Args:
            msg (bytes): the message to wait for
            timeout (float): timeout to wait for

        Returns:
            list[bool]: list of read success.
        """
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            fs = [executor.submit(eq.wait_for_msg, msg, timeout) for eq in self.eqs]
            results = [f.result() for f in as_completed(fs)]
        return list(results)

    def wait_for_linux_boot(self) -> list[bool]:
        """wait for linux boot on all eqs.

        Returns:
            list[bool]: list of boot success
        """
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            fs = [executor.submit(eq.wait_for_linux_boot) for eq in self.eqs]
            results = [f.result() for f in as_completed(fs)]
        return list(results)

    def wait_for_core_write(
        self,
        core_type: CoreType,
        timeout: float = 180,
    ) -> list[bool]:
        """wait for core to be write to all EQs

        Args:
            core_type (CoreType): The type of core to wait for

        Returns:
            list[bool]: list of success core write
        """
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            fs = [
                executor.submit(eq.wait_for_core_write, core_type, timeout)
                for eq in self.eqs
            ]
            results = [f.result() for f in as_completed(fs)]
        return list(results)

    def reboot(self, *, sleep_after: int = 0) -> None:
        """reboots the board, if MCS in setup reset MCS as well.

        Args:
            sleep_after (int, optional): sleep after reset parameter. Defaults to 0.

        Raises:
            NotImplementedError: if reboot is not supported for the board.
        """
        if self.board_type == BoardType.EVO:
            raise NotImplementedError("reboot is not support on EVO")

        self.logger.info("rebooting platform...")

        if self.mcs is not None:
            self.logger.debug("rebooting MCS")
            self.mcs.run_serial_cmd("reboot")

        self.logger.debug("rebooting board")
        self.mcu.run_serial_cmd("reboot")

        if sleep_after > 0:
            self.logger.info(f"sleeping for {sleep_after} seconds.")
            time.sleep(sleep_after)

    @staticmethod
    def create_eqs(
        pbcm_ports: dict[str, str] = DEFAULT_PBCM_PORTS,
        os_type: OSType = OSType.LINUX,
    ) -> list[EyeQ5]:
        return [EyeQ5(pbcm, port, os_type) for pbcm, port in pbcm_ports.items()]

    @staticmethod
    def create_mcu(
        pbc: str = "000",
        port: str = "/dev/MCUE_PBC_000",
        mcu_type: McuType = McuType.ADAM,
    ) -> Mcu:
        return Mcu(pbc, port, mcu_type)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(eqs={self.eqs}, mcu={self.mcu})"
