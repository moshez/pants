# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.core_tasks.bash_completion import BashCompletion
from pants.core_tasks.changed_target_tasks import CompileChanged, TestChanged
from pants.core_tasks.clean import Clean
from pants.core_tasks.deferred_sources_mapper import DeferredSourcesMapper
from pants.core_tasks.explain_options_task import ExplainOptionsTask
from pants.core_tasks.invalidate import Invalidate
from pants.core_tasks.list_goals import ListGoals
from pants.core_tasks.noop import NoopCompile, NoopTest
from pants.core_tasks.reporting_server_kill import ReportingServerKill
from pants.core_tasks.reporting_server_run import ReportingServerRun
from pants.core_tasks.roots import ListRoots
from pants.core_tasks.run_prep_command import RunPrepCommand
from pants.core_tasks.targets_help import TargetsHelp
from pants.core_tasks.what_changed import WhatChanged
from pants.goal.goal import Goal
from pants.goal.task_registrar import TaskRegistrar as task


def register_goals():
  # Register descriptions for the standard multiple-task goals.  Single-task goals get
  # their descriptions from their single task.
  Goal.register('buildgen', 'Automatically generate BUILD files.')
  Goal.register('bootstrap', 'Bootstrap tools needed by subsequent build steps.')
  Goal.register('imports', 'Resolve external source dependencies.')
  Goal.register('gen', 'Generate code.')
  Goal.register('resolve', 'Resolve external binary dependencies.')
  Goal.register('compile', 'Compile source code.')
  Goal.register('binary', 'Create a runnable binary.')
  Goal.register('resources', 'Prepare resources.')
  Goal.register('bundle', 'Create a deployable application bundle.')
  Goal.register('test', 'Run tests.')
  Goal.register('bench', 'Run benchmarks.')
  Goal.register('repl', 'Run a REPL.')
  Goal.register('repl-dirty', 'Run a REPL, skipping compilation.')
  Goal.register('run', 'Invoke a binary.')
  Goal.register('run-dirty', 'Invoke a binary, skipping compilation.')
  Goal.register('doc', 'Generate documentation.')
  Goal.register('publish', 'Publish a build artifact.')
  Goal.register('dep-usage', 'Collect target dependency usage data.')

  # Register tasks.

  # Cleaning.
  task(name='invalidate', action=Invalidate).install()
  task(name='clean-all', action=Clean).install()

  # Reporting server.
  # TODO: The reporting server should be subsumed into pantsd, and not run via a task.
  task(name='server', action=ReportingServerRun, serialize=False).install()
  task(name='killserver', action=ReportingServerKill, serialize=False).install()

  # Getting help.
  task(name='goals', action=ListGoals).install()
  task(name='options', action=ExplainOptionsTask).install()
  task(name='targets', action=TargetsHelp).install()

  # Stub for other goals to schedule 'compile'. See noop_exec_task.py for why this is useful.
  task(name='compile', action=NoopCompile).install('compile')

  # Must be the first thing we register under 'test'.
  task(name='run_prep_command', action=RunPrepCommand).install('test')
  # Stub for other goals to schedule 'test'. See noop_exec_task.py for why this is useful.
  task(name='test', action=NoopTest).install('test')

  # Operations on files that the SCM detects as changed.
  task(name='changed', action=WhatChanged).install()
  task(name='compile-changed', action=CompileChanged).install()
  task(name='test-changed', action=TestChanged).install()

  # Workspace information.
  task(name='roots', action=ListRoots).install()
  task(name='bash-completion', action=BashCompletion).install()

  # Handle sources that aren't loose files in the repo.
  task(name='deferred-sources', action=DeferredSourcesMapper).install()