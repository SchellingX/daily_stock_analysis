# -*- coding: utf-8 -*-
"""Regression tests for safe numeric env parsing outside Config._load_from_env."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import textwrap
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

try:
    import litellm  # noqa: F401
except ModuleNotFoundError:
    sys.modules["litellm"] = MagicMock()

import src.auth as auth
import webui
from api.v1.endpoints import auth as auth_endpoint


class EnvNumericFallbacksTestCase(unittest.TestCase):
    @staticmethod
    def _run_python(code: str, **env_overrides: str) -> str:
        repo_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env.update(env_overrides)
        result = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(code)],
            cwd=repo_root,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def test_invalid_provider_priority_env_values_fall_back_on_import(self) -> None:
        cases = [
            ("data_provider.akshare_fetcher", "AkshareFetcher", "AKSHARE_PRIORITY", 1),
            ("data_provider.efinance_fetcher", "EfinanceFetcher", "EFINANCE_PRIORITY", 0),
            ("data_provider.tushare_fetcher", "TushareFetcher", "TUSHARE_PRIORITY", 2),
            ("data_provider.pytdx_fetcher", "PytdxFetcher", "PYTDX_PRIORITY", 2),
            ("data_provider.baostock_fetcher", "BaostockFetcher", "BAOSTOCK_PRIORITY", 3),
            ("data_provider.yfinance_fetcher", "YfinanceFetcher", "YFINANCE_PRIORITY", 4),
            ("data_provider.longbridge_fetcher", "LongbridgeFetcher", "LONGBRIDGE_PRIORITY", 5),
        ]

        for module_name, class_name, env_key, expected in cases:
            with self.subTest(module=module_name):
                output = self._run_python(
                    f"""
                    import importlib
                    module = importlib.import_module("{module_name}")
                    print(getattr(module, "{class_name}").priority)
                    """,
                    **{env_key: "bad"},
                )
                self.assertEqual(output.splitlines()[-1], str(expected))

    def test_invalid_efinance_timeout_falls_back_on_import(self) -> None:
        output = self._run_python(
            """
            import importlib
            module = importlib.import_module("data_provider.efinance_fetcher")
            print(module._EF_CALL_TIMEOUT)
            """,
            EFINANCE_CALL_TIMEOUT="bad",
        )
        self.assertEqual(output.splitlines()[-1], "30")

    @patch("src.logging_config.setup_logging")
    @patch("src.config.setup_env")
    @patch("uvicorn.run")
    def test_webui_main_falls_back_to_default_port_when_env_invalid(
        self,
        run_mock,
        _setup_env_mock,
        _setup_logging_mock,
    ) -> None:
        with patch.dict(os.environ, {"WEBUI_PORT": "bad"}, clear=False):
            exit_code = webui.main()

        self.assertEqual(exit_code, 0)
        run_mock.assert_called_once()
        self.assertEqual(run_mock.call_args.kwargs["port"], 8000)

    def test_auth_paths_fall_back_to_default_session_age_when_env_invalid(self) -> None:
        request = SimpleNamespace(headers={}, url=SimpleNamespace(scheme="http"))

        with patch.dict(os.environ, {"ADMIN_SESSION_MAX_AGE_HOURS": "bad"}, clear=False), patch.object(
            auth,
            "_get_session_secret",
            return_value=b"x" * 32,
        ):
            token = auth.create_session()
            self.assertTrue(auth.verify_session(token))
            self.assertEqual(
                auth_endpoint._cookie_params(request)["max_age"],
                auth.SESSION_MAX_AGE_HOURS_DEFAULT * 3600,
            )


if __name__ == "__main__":
    unittest.main()
