import subprocess
import sys
import io
from contextlib import redirect_stdout
from typing import List, Optional, Type, Dict, Any

from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
import pandas as pd
import numpy as np


# schema remains the same
class NotebookCodeExecutorSchema(BaseModel):
    code: str = Field(description="The Python code to execute.")
    required_libraries: Optional[List[str]] = Field(
        default=None,
        description="A list of Python library names that need to be installed using pip before executing the code. Example: ['seaborn', 'pandas']",
    )


# define the custom tool
class NotebookCodeExecutor(BaseTool):
    name: str = "Notebook Code Executor"
    description: str = (
        "Executes Python code directly using a provided execution namespace (like the notebook's globals) and installs required libraries using pip. "
        "IMPORTANT: Allows access and modification of variables in the provided namespace. "
        "Use this for data analysis, preprocessing, modeling, etc. "
        "Input must be the Python code string and an optional list of libraries to install. "
        "Include print() statements in your code to see results. Returns stdout/stderr."
    )
    args_schema: Type[BaseModel] = NotebookCodeExecutorSchema

    # initialize with a default empty dict
    _execution_namespace: Dict[str, Any] = PrivateAttr(default_factory=dict)

    # modified __init__
    def __init__(self, namespace: Dict[str, Any] = None, **kwargs):
        # pass **kwargs FIRST to Pydantic/BaseTool initializer
        super().__init__(**kwargs)
        # now handle our custom attribute AFTER standard initialization
        if namespace is not None:
            self._execution_namespace = namespace
            # ensure essential modules are available
            self._execution_namespace.setdefault("pd", pd)
            self._execution_namespace.setdefault("np", np)

    def _run(self, code: str, required_libraries: Optional[List[str]] = None) -> str:
        """Executes the code in the tool's configured namespace and installs libraries."""

        installation_log = ""
        # install required libraries
        if required_libraries:
            installation_log += "--- Installing Libraries ---\n"
            python_executable = sys.executable
            for lib in required_libraries:
                installation_log += f"Attempting to install {lib}...\n"
                try:
                    process = subprocess.run(
                        [python_executable, "-m", "pip", "install", lib],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=120,
                    )
                    if process.returncode == 0:
                        installation_log += f"Successfully installed {lib}.\n"
                    else:
                        installation_log += (
                            f"Failed to install {lib}. RetCode: {process.returncode}\nStderr: {process.stderr}\n"
                        )
                except Exception as e:
                    installation_log += f"Error installing {lib}: {e}\n"
            installation_log += "--- Library Installation Finished ---\n\n"

        # execute the code
        execution_log = "--- Executing Code ---\n"
        output_buffer = io.StringIO()
        try:
            with redirect_stdout(output_buffer):
                # use the private attribute name 
                exec(code, self._execution_namespace)

            execution_output = output_buffer.getvalue()
            execution_log += (
                f"Code executed successfully. Output:\n```output\n{execution_output or '[No Print Output]'}\n```\n"
            )
            return installation_log + execution_log

        except Exception as e:
            error_message = f"Error executing code: {type(e).__name__}: {e}\n"
            partial_output = output_buffer.getvalue()
            if partial_output:
                error_message += f"Captured output before error:\n```output\n{partial_output}\n```\n"
            execution_log += error_message
            return installation_log + execution_log
