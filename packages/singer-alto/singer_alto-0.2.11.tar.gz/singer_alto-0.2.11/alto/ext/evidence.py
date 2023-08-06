# MIT License
# Copyright (c) 2023 Alex Butler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
"""This module implements the Evidence.dev extension."""
import json
import os
import typing as t
from contextlib import contextmanager

from doit.cmd_base import CmdAction
from doit.tools import LongRunning
from dynaconf import Validator

from alto.engine import AltoExtension
from alto.models import AltoTask

ENV_VARS = (
    "EVIDENCE_DATABASE",
    # duckdb
    "EVIDENCE_CREDENTIALS_FILENAME",
    "EVIDENCE_CREDENTIALS_GITIGNORE_DUCKDB",
    # bigquery
    "EVIDENCE_CREDENTIALS_CLIENT_EMAIL",
    "EVIDENCE_CREDENTIALS_PRIVATE_KEY",
)


def register():
    """Register the extension."""
    return Evidence


class Evidence(AltoExtension):
    """Evidence.dev extension."""

    def init_hook(self) -> None:
        """Initialize the extension."""
        _path = os.path.expanduser(self.spec.config.home)
        if _path.startswith("/"):
            self.spec.config.home = _path
        else:
            self.spec.config.home = os.path.join(self.filesystem.root_dir, _path)
        self._config_file = os.path.join(
            self.spec.config.home,
            ".evidence",
            "template",
            "evidence.settings.json",
        )
        self.database = os.environ.get("EVIDENCE_DATABASE")

    @staticmethod
    def get_validators() -> t.List["Validator"]:
        return [
            Validator(
                "UTILITIES.evidence.config.home",
                default="./reports",
                cast=str,
                apply_default_on_none=True,
                description="Evidence home directory.",
            ),
            Validator(
                "UTILITIES.evidence.config.strict",
                default=False,
                cast=bool,
                apply_default_on_none=True,
                description="Run Evidence in strict mode.",
            ),
        ]

    def initialize(self):
        """Run 'npx degit' to generate Evidence project from template."""
        return (
            AltoTask(name="initialize")
            .set_actions(
                f"mkdir -p {self.spec.config.home}",
                f"npx --yes degit evidence-dev/template {self.spec.config.home}",
            )
            .set_doc("Generate Evidence project from template.")
            .set_clean(f"rm -rf {self.spec.config.home}")
            .set_uptodate(f"test -f {self.spec.config.home}/package.json")
            .set_targets(f"{self.spec.config.home}/package.json")
            .set_verbosity(2)
            .data
        )

    def build(self):
        """Run 'npm run build' in the Evidence home dir."""
        task = (
            AltoTask(name="build")
            .set_actions(f"npm --prefix {self.spec.config.home} install")
            .set_file_dep(f"{self.spec.config.home}/package.json")
            .set_doc("Build the Evidence dev reports.")
            .set_clean(f"rm -rf {self.spec.config.home}/build")
            .set_verbosity(2)
        )
        if self.spec.config.get("strict", False):
            task.set_actions(
                _EvidenceCmdWrapper(
                    f"npm --prefix {self.spec.config.home} run build:strict",
                    _config_file=self._config_file,
                )
            )
        else:
            task.set_actions(
                _EvidenceCmdWrapper(
                    f"npm --prefix {self.spec.config.home} run build",
                    _config_file=self._config_file,
                )
            )
        return task.data

    def dev(self):
        """Run 'npm run dev' in the Evidence home dir."""
        return (
            AltoTask(name="dev")
            .set_actions(
                f"npm --prefix {self.spec.config.home} install",
                f"npm --prefix {self.spec.config.home} run dev",
            )
            .set_file_dep(f"{self.spec.config.home}/package.json")
            .set_doc("Run the Evidence dev server.")
            .set_verbosity(2)
            .data
        )

    def tasks(self):
        """Yields tasks."""
        yield self.initialize()
        yield self.build()
        yield self.dev()


class _EvidenceServerWrapper(LongRunning):
    """Wrapper for Evidence server to suppress config file."""

    def execute(self, out=None, err=None):
        with suppress_config_file(self.pkwargs.pop("_config_file")):
            super().execute(out, err)


class _EvidenceCmdWrapper(CmdAction):
    """Wrapper for Evidence commands to suppress config file."""

    def execute(self, out=None, err=None):
        with suppress_config_file(self.pkwargs.pop("_config_file")):
            super().execute(out, err)


@contextmanager
def suppress_config_file(self, config_file) -> t.Iterator[None]:
    """Suppress Evidence config file.

    As evidence checks its config file _before_ env vars,
    we need to remove it before run and replace it after (if it exists).
    """
    config = None
    if os.path.exists(config_file):
        with open(config_file, "r") as cfg:
            config = json.load(cfg)
        os.remove(config_file)
    try:
        yield
    finally:
        if config:
            with open(config_file, "w", encoding="utf-8") as cfg:
                json.dump(config, cfg)
