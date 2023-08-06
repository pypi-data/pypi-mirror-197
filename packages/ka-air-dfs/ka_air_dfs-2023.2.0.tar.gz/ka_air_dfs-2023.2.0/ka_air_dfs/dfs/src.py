"""
Source Utilities for Source DAG Factory
"""

import os
from jinja2 import Template

from ka_utg.log import Log
from ka_utg.str import Str

from ka_air_dfs.dfs.fac import DagFac as DagFacCom
from ka_air_dfs.dfs.uts import Tg as UtsTg
from ka_air_dfs.dfs.uts import GroupId as UtsGroupId


class Cmd:
    @staticmethod
    def sh_script(cmd):
        """
        Show task id included in command string.
        the command string formats should be:
          [<path>/]<command[.suffix]> [<parameter>]

        :param cmd: str, the command string to be parsed in valid format
        :return: boolean, the result of the check: true or false
        """
        if cmd.startswith("standard.sh"):
            script = cmd.replace("standard.sh", "").strip()
        else:
            script = cmd.strip()
        # remove script parameters
        script = script.split(' ', 1)[0]
        # show basename
        script_basename = os.path.basename(script)
        # remove extension
        script = os.path.splitext(script_basename)[0]
        return script


class Utils:

    @staticmethod
    def sh_replace_id(d_cmd):
        id = d_cmd.get('id')
        if '$' in id:
            return id.replace('$', '')
        return id

    @classmethod
    def sh_replace_task_id_prefix(cls, d_cmd, prefix=None):
        id = cls.sh_replace_id(d_cmd)
        if prefix is not None:
            return f"{prefix}_{id}"
        return id

    @staticmethod
    def sh_task_id_prefix(d_cmd, prefix=None):
        id = d_cmd.get('id')
        if prefix is not None:
            return f"{prefix}_{id}"
        return id

    @staticmethod
    def sh_ix(tsk_ix, d_cmd):
        if DagFacCom.sw_cmd_ix:
            return d_cmd.get('command_ix')
        return tsk_ix

    @classmethod
    def sh_task_id(cls, tsk_ix, d_cmd):
        """
        Show task id

        :cmd: , Command
        :return: , task_id
        """
        cmd = d_cmd.get('command')
        cmd_base = Cmd.sh_script(cmd)
        return f"{cmd_base}_{cls.sh_ix(tsk_ix, d_cmd)}"

    @classmethod
    def sh_options(cls, dag_id, tsk_ix, d_cmd):
        """
        Show options
        :dag_id: , Command
        :tsk_id: , Task index
        :return: , options
        """
        return f"--task {dag_id} --step {cls.sh_ix(tsk_ix, d_cmd)}"

    @staticmethod
    def sh_trigger_rule(d_cmd):
        """
        Show trigger rule
        """
        Log.Eq.debug("d_cmd", d_cmd)
        if 'trigger_rule' in d_cmd:
            return d_cmd['trigger_rule']
        else:
            return "all_success"


class TskString:
    """
    Operator class
    """
    TriggerDagRun = """
{{_tsk}} = TriggerDagRunOperator(
    task_id="{{task_id}}",
    trigger_dag_id="{{trigger_dag_id}}",
    execution_date="{{execution_date}}",
    reset_dag_run=True,
    wait_for_completion=True,
    poke_interval=30,
    allowed_states=['success'],
    failed_states=None,
    params={
        "triggered_by_dag_id": "{{triggered_by_dag_id}}"
    },
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}"
)

"""

    ExternalTaskSensor = """
{{_tsk}} = ExternalTaskSensor(
    task_id="{{tsk_id}}",
    task_group={{_tg}},
    external_dag_id="{{external_dag_id}}",
    timeout=600,
    allowed_states=['success'],
    failed_states=['failed', 'skipped'],
    mode="reschedule",
)

"""

    Bash = """
{{_tsk}} = BashOperator(
    bash_command='{{command}}',
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id='{{task_id}}',
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}"
)

"""


class Tsk:
    """
    Operator class
    """
    @staticmethod
    def sh_trigger_dag_run(dag_id, tg, tsk_ix, d_cmd, env):
        """
        Show trigger task

        :cls: , class name
        :dag_id: , dag Id
        :tg: , Task Group
        :tsk_ix: str, Task index
        :d_cmd: dict, Command Dictionary
        :return: , task
        """
        execution_date = "{{ ds }}"

        return Template(TskString.TriggerDagRun).render(
            execution_date=execution_date,
            triggered_by_dag_id=dag_id,
            var_tsk=dag_id,

            task_id=Utils.sh_replace_task_id_prefix(d_cmd, "tri"),
            trigger_dag_id=Utils.sh_replace_id(d_cmd),
            trigger_rule=Utils.sh_trigger_rule(d_cmd),

            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
            _tg=UtsTg.sh_tg(tg),
        )

    @staticmethod
    def sh_external_task_sensor(dag_id, tg, tsk_ix, d_cmd, env):
        """
        Show task

        :cls: , class name
        :dag: , dag
        :tsk_ix: str, Task index
        :d_cmd: dict, Task Dag Dictionary
        :return: , task
        """
        external_dag_id = Utils.sh_replace_task_id_prefix(d_cmd, "tsk")
        tsk_id = f"sen_{external_dag_id}"
        if DagFacCom.sw_cmd_ix:
            tsk_id = f"{tsk_id}_{DagFacCom.cmd_ix}"

        return Template(TskString.ExternalTaskSensor).render(
            tsk_id=tsk_id,
            external_dag_id=external_dag_id,

            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
        )

    @staticmethod
    def sh_bash(dag_id, tg, tsk_ix, d_cmd, env):
        return Template(TskString.Bash).render(
            command=d_cmd.get('command'),
            run_as_user=d_cmd.get('run_as_user', 'root'),
            skip_exit_code=d_cmd.get('skip_exit_code'),

            task_id=Utils.sh_task_id(tsk_ix, d_cmd),
            trigger_rule=Utils.sh_trigger_rule(d_cmd),

            _tg=UtsTg.sh_tg(tg),
            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
        )


class DbTskString:
    """
    Operator class
    """
    DbTriggerDagRun = """
{{_tsk}} = TriggerDagRunOperator(
    task_id="{{task_id}}",
    trigger_dag_id="{{trigger_dag_id}}",
    execution_date="{{execution_date}}",
    reset_dag_run=True,
    wait_for_completion=True,
    poke_interval=30,
    allowed_states=['success'],
    failed_states=None,
    params={
        "triggered_by_dag_id": "{{triggered_by_dag_id}}"
    },
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbApcShell = """
{{_tsk}} = DbApcShellOperator(
    shell="{{shell}}",
    command="{{command}}",
    parameter={{parameter|tojson}},
    options="{{options}}",
    appl="{{appl}}",
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbShell = """
{{_tsk}} = DbShellOperator(
    shell="{{shell}}",
    command="{{command}}",
    parameter={{parameter|tojson}},
    options="{{options}}",
    appl="{{appl}}",
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbShellCyclic = """
{{_tsk}} = DbShellCyclicOperator(
    shell="{{shell}}",
    command="{{command}}",
    parameter={{parameter|tojson}},
    sequence={{sequence}},
    interval={{interval}},
    options="{{options}}",
    appl="{{appl}}",
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbCond = """
{{_tsk}} = DbCondOperator(
    cond_key="{{cond_key}}",
    run_as_user="{{run_as_user}}",
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}}
)

"""

    DbFileSensorAsync = """
{{_tsk}} = DbFileSensorAsyncOperator(
    cond_key="{{cond_key}}",
    run_as_user="{{run_as_user}}",
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}}
)

"""


class DbTsk:

    @staticmethod
    def sh_db_trigger_dag_run(dag_id, tg, tsk_ix, d_cmd, env):
        """
        Show trigger task

        :cls: , class name
        :dag_id: , dag Id
        :tg: , Task Group
        :tsk_ix: str, Task index
        :d_cmd: dict, Command Dictionary
        :return: , task
        """
        execution_date = "{{ ds }}"

        return Template(DbTskString.DbTriggerDagRun).render(
            execution_date=execution_date,
            triggered_by_dag_id=dag_id,
            var_tsk=dag_id,

            task_id=Utils.sh_replace_task_id_prefix(d_cmd, "tri"),
            trigger_dag_id=Utils.sh_replace_id(d_cmd),
            trigger_rule=Utils.sh_trigger_rule(d_cmd),

            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
            _tg=UtsTg.sh_tg(tg),
        )

    @staticmethod
    def sh_db_apc_shell(dag_id, tg, tsk_ix, d_cmd, env):
        # if len(tsk_id) >= 250:
        return Template(DbTskString.DbApcShell).render(
            shell=d_cmd.get('shell', 'bash'),
            command=d_cmd.get('command'),
            parameter=d_cmd.get('parameter'),
            appl=d_cmd.get('appl', 'FDW'),
            run_as_user=d_cmd.get('run_as_user', 'root'),
            skip_exit_code=d_cmd.get('skip_exit_code'),
            var_tsk=dag_id,

            options=Utils.sh_options(dag_id, tsk_ix, d_cmd),
            task_id=Utils.sh_task_id(tsk_ix, d_cmd),
            trigger_rule=Utils.sh_trigger_rule(d_cmd),

            _tg=UtsTg.sh_tg(tg),
            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
        )

    @staticmethod
    def sh_db_shell(dag_id, tg, tsk_ix, d_cmd, env):
        return Template(DbTskString.DbShell).render(
            shell=d_cmd.get('shell', 'bash'),
            command=d_cmd.get('command'),
            parameter=d_cmd.get('parameter'),
            appl=d_cmd.get('appl', 'FDW'),
            run_as_user=d_cmd.get('run_as_user', 'root'),
            skip_exit_code=d_cmd.get('skip_exit_code'),
            var_tsk=dag_id,

            options=Utils.sh_options(dag_id, tsk_ix, d_cmd),
            task_id=Utils.sh_task_id(tsk_ix, d_cmd),
            trigger_rule=Utils.sh_trigger_rule(d_cmd),

            _tg=UtsTg.sh_tg(tg),
            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
        )

    @staticmethod
    def sh_db_shell_cyclic(dag_id, tg, tsk_ix, d_cmd, env):
        return Template(DbTskString.DbShellCyclic).render(
            shell=d_cmd.get('shell', 'bash'),
            command=d_cmd.get('command'),
            parameter=d_cmd.get('parameter'),
            appl=d_cmd.get('appl', 'FDW'),
            run_as_user=d_cmd.get('run_as_user', 'root'),
            skip_exit_code=d_cmd.get('skip_exit_code'),
            sequence=d_cmd.get('sequence'),
            interval=d_cmd.get('interval'),
            var_tsk=dag_id,

            options=Utils.sh_options(dag_id, tsk_ix, d_cmd),
            task_id=Utils.sh_task_id(tsk_ix, d_cmd),
            trigger_rule=Utils.sh_trigger_rule(d_cmd),

            _tg=UtsTg.sh_tg(tg),
            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
        )

    @staticmethod
    def sh_db_cond(dag_id, tg, tsk_ix, d_obj, env):

        return Template(DbTskString.DbCond).render(
            cond_key=d_obj.get('cond_key'),
            run_as_user=d_obj.get('run_as_user', 'root'),
            skip_exit_code=d_obj.get('skip_exit_code'),

            task_id=Utils.sh_task_id_prefix(d_obj, "cnd"),

            _tg=UtsTg.sh_tg(tg),
            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
        )

    @staticmethod
    def sh_db_file_sensor_async(dag_id, tg, tsk_ix, d_obj, env):
        return Template(DbTskString.DbFileSensorAsync).render(
            run_as_user=d_obj.get('run_as_user', 'root'),
            fs_conn_id=d_obj.get('fs_conn_id'),
            filepath=d_obj.get('filepath'),
            recursive=d_obj.get('recursive'),
            skip_exit_code=d_obj.get('skip_exit_code'),

            task_id=Utils.sh_task_id_prefix(d_obj, "fsa"),

            _tg=UtsTg.sh_tg(tg),
            _tsk=UtsTg.sh_tsk(tg, tsk_ix),
        )


class Ope:

    cmd2tsk = {
      "DbApcShell": DbTsk.sh_db_apc_shell,
      "DbShell": DbTsk.sh_db_shell,
      "DbShellCyclic": DbTsk.sh_db_shell_cyclic,
      "DbCond": DbTsk.sh_db_cond,
      "DbBash": Tsk.sh_bash,
      "DbTriggerDagRun": DbTsk.sh_db_trigger_dag_run,
      "DbFileSensorAsync": DbTsk.sh_db_file_sensor_async,

      "Bash": Tsk.sh_bash,
      "TriggerDagRun": Tsk.sh_trigger_dag_run,
    }

    @classmethod
    def sh_tsk(cls, dag_id, tg, tsk_ix, d_cmd, env):
        """
        Show task

        :cls: , class name (CmdDic)
        :dag: , dag
        :tg: , Task Group
        :tsk_ix: str, Task index
        :env: dict, Environment dictionary
        :d_cmd: dict, Command Dictionary
        :return: , task
        """
        operator = d_cmd.get('operator', 'DbShell')
        fnc = cls.cmd2tsk.get(operator)

        Log.Eq.debug("operator", operator)
        Log.Eq.debug("fnc", fnc)
        Log.Eq.debug("dag_id", dag_id)
        Log.Eq.debug("tg", tg)
        Log.Eq.debug("tsk_ix", tsk_ix)
        Log.Eq.debug("d_cmd", d_cmd)
        Log.Eq.debug("env", env)

        if fnc is None:
            msg = (
                f"Task Function is not defined for dag_id: {dag_id}, "
                f"d_cmd: {d_cmd}"
            )
            Log.warning(msg)
            return None
        return fnc(dag_id, tg, tsk_ix, d_cmd, env)


class OpeArr:
    """
    Operator class for Command-dictionary Arrays
    """
    @staticmethod
    def sh(dag_id, tg, obj, env):
        a_tsk = []
        for tsk_ix, d_cmd in enumerate(obj):
            tsk = Ope.sh_tsk(dag_id, tg, tsk_ix, d_cmd, env)
            if tsk is None:
                continue
            DagFacCom.cmd_ix = DagFacCom.cmd_ix + 1
            a_tsk.append(tsk)
        return a_tsk


class TskArrDownstream:
    """
    Task Array class
    """
    s_downstream = """
{{source}}.set_downstream({{target}})"""

    @classmethod
    def sh(cls, a_tsk):
        if len(a_tsk) < 2:
            return
        arr = []
        for ii in range(len(a_tsk)-1):
            jj = ii+1
            source = Str.sh_first_item(a_tsk[ii])
            target = Str.sh_first_item(a_tsk[jj])
            downstream = Template(cls.s_downstream).render(
                source=source,
                target=target
            )
            arr.append(downstream)
        arr.append("\n")
        return arr


class TskArrChain:
    """
    Task Array class
    """
    @classmethod
    def sh(cls, a_tsk):
        if len(a_tsk) < 2:
            return None
        arr = []
        arr.append("\nchain(\n")
        for item in a_tsk[:-1]:

            Log.Eq.debug("item", item)

            arr.append(f"    {Str.sh_first_item(item)},\n")
        arr.append(f"    {Str.sh_first_item(a_tsk[-1])}\n")
        arr.append(")\n")
        return arr


class TskArr:
    """
    Task Array class
    """
    @staticmethod
    def sh_chain(a_tsk, type="chain"):
        if type == 'chain':
            return TskArrChain.sh(a_tsk)
        elif type == 'downstream':
            return TskArrDownstream.sh(a_tsk)


class TskGrp:

    s_child = """
{{group_id}} = TaskGroup(
     group_id='{{group_id}}',
     tooltip='{{tooltip}}',
     parent_group={{parent_group}},
     dag=dag
)

"""

    s_root = """
{{group_id}} = TaskGroup(
    group_id='{{group_id}}',
    tooltip='{{tooltip}}',
    dag=dag
)

"""

    @classmethod
    def create_child(cls, group_id, parent_group, group_ix, env):
        tooltip = f'Tasks of {group_id}'
        group_id_ix = UtsGroupId.sh_group_id_ix(group_id, group_ix)
        parent_group_new = Str.sh_first_item(parent_group)
        tg = Template(cls.s_child).render(
            group_id=group_id_ix,
            tooltip=tooltip,
            parent_group=parent_group_new,
        )
        return tg

    @classmethod
    def create_root(cls, group_id):
        tooltip = f'Tasks of {group_id}'
        tg = Template(cls.s_root).render(
            group_id=group_id,
            tooltip=tooltip,
        )
        return tg


class TskGrpArr:

    @staticmethod
    def add(a_tskgrp, a_line):
        if a_line is None:
            return
        for line in a_line:
            a_tskgrp.append(line)


class Dags:

    s_dag = """
import pendulum

from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.models.dag import DAG
from airflow.models.baseoperator import chain

from ka_air_prv.prv.core.operators.DbApcShell import DbApcShellOperator
from ka_air_prv.prv.core.operators.DbShell import DbShellOperator
from ka_air_prv.prv.core.operators.DbShellCyclic import DbShellCyclicOperator
from ka_air_prv.prv.core.operators.DbCond import DbCondOperator
from ka_air_prv.prv.core.operators.DbFileSensorAsnyc
    import DbFileSensorAsnycOperator
from ka_air_prv.prv.core.operators.DbTriggerDagRun
    import DbTriggerDagRunOperator

from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.bash import BashOperator

# schedule=None
# schedule_interval=timedelta(days=1)
schedule_interval=None
# start_date = days_ago(2)
start_date = pendulum.datetime(2022, 1, 1, tz="UTC")
catchup = False
skip_exit_code = None

email = ['bernd.stroehle@db.com']
email_on_failure = False

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
    'email': email,
    'email_on_failure': email_on_failure,
}

dag = DAG(
    dag_id='{{dag_id}}',
    description='{{description}}',
    default_args=default_args,
    schedule_interval=schedule_interval,
    start_date=start_date,
    catchup=catchup,
    tags={{tags}},
)

"""

    @classmethod
    def sh_dag(cls, obj, **kwargs):
        dag_prefix = kwargs.get('dag_prefix')
        dag_id = "_".join(filter(None, [dag_prefix, f"{obj['chain']['id']}"]))

        dag = Template(cls.s_dag).render(
            dag_id=dag_id,
            tags=kwargs.get('tags'),
            description=obj["chain"].get("description")
        )
        return dag, dag_id
