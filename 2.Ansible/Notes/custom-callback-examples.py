# Custom Callback Plugin Examples
# Place these in callback_plugins/ directory

# 1. Simple Logging Callback
from ansible.plugins.callback import CallbackBase
import json
import time

class CallbackModule(CallbackBase):
    """Custom logging callback plugin"""
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'custom_logger'
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        self.start_time = time.time()
    
    def v2_playbook_on_start(self, playbook):
        self._display.display(f"Playbook started: {playbook._file_name}")
    
    def v2_playbook_on_task_start(self, task, is_conditional):
        self._display.display(f"Task started: {task.get_name()}")
    
    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        task = result._task.get_name()
        self._display.display(f"SUCCESS: {host} - {task}")

# 2. Slack Notification Callback
import requests

class CallbackModule(CallbackBase):
    """Slack notification callback"""
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'slack_notify'
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        self.webhook_url = "YOUR_SLACK_WEBHOOK_URL"
    
    def send_slack_message(self, message):
        payload = {"text": message}
        try:
            requests.post(self.webhook_url, json=payload)
        except Exception as e:
            self._display.warning(f"Failed to send Slack notification: {e}")
    
    def v2_playbook_on_start(self, playbook):
        message = f"🚀 Ansible playbook started: {playbook._file_name}"
        self.send_slack_message(message)
    
    def v2_playbook_on_stats(self, stats):
        hosts = stats.processed.keys()
        message = f"✅ Playbook completed for {len(hosts)} hosts"
        self.send_slack_message(message)

# 3. Performance Metrics Callback
import time
import json

class CallbackModule(CallbackBase):
    """Performance metrics callback"""
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'performance_metrics'
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        self.task_times = {}
        self.host_stats = {}
    
    def v2_runner_on_start(self, host, task):
        self.task_times[task._uuid] = time.time()
    
    def v2_runner_on_ok(self, result):
        task_uuid = result._task._uuid
        if task_uuid in self.task_times:
            duration = time.time() - self.task_times[task_uuid]
            host = result._host.get_name()
            task_name = result._task.get_name()
            
            if host not in self.host_stats:
                self.host_stats[host] = []
            
            self.host_stats[host].append({
                'task': task_name,
                'duration': duration,
                'status': 'ok'
            })
    
    def v2_playbook_on_stats(self, stats):
        # Output performance summary
        for host, tasks in self.host_stats.items():
            total_time = sum(task['duration'] for task in tasks)
            self._display.display(f"Host {host}: {len(tasks)} tasks, {total_time:.2f}s total")

# 4. Error Tracking Callback
import logging

class CallbackModule(CallbackBase):
    """Error tracking and logging callback"""
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'error_tracker'
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        logging.basicConfig(
            filename='/var/log/ansible-errors.log',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('ansible_errors')
    
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task = result._task.get_name()
        error_msg = result._result.get('msg', 'Unknown error')
        
        log_entry = {
            'host': host,
            'task': task,
            'error': error_msg,
            'ignore_errors': ignore_errors
        }
        
        self.logger.error(json.dumps(log_entry))
        
        if not ignore_errors:
            self._display.error(f"FAILED: {host} - {task}: {error_msg}")

# 5. Compliance Audit Callback
import json
from datetime import datetime

class CallbackModule(CallbackBase):
    """Compliance audit callback"""
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'compliance_audit'
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        self.audit_log = []
        self.compliance_tasks = [
            'Configure SSH',
            'Set firewall rules',
            'Update packages',
            'Configure users'
        ]
    
    def v2_runner_on_ok(self, result):
        task_name = result._task.get_name()
        if any(compliance in task_name for compliance in self.compliance_tasks):
            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'host': result._host.get_name(),
                'task': task_name,
                'status': 'compliant',
                'changed': result._result.get('changed', False)
            }
            self.audit_log.append(audit_entry)
    
    def v2_playbook_on_stats(self, stats):
        # Write audit log
        with open('/var/log/compliance-audit.json', 'w') as f:
            json.dump(self.audit_log, f, indent=2)
        
        self._display.display(f"Compliance audit completed: {len(self.audit_log)} entries logged")

# 6. Real-time Dashboard Callback
import requests
import json

class CallbackModule(CallbackBase):
    """Real-time dashboard callback"""
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'dashboard_update'
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        self.dashboard_url = "http://dashboard.company.com/api/ansible"
    
    def send_update(self, data):
        try:
            requests.post(f"{self.dashboard_url}/update", json=data)
        except Exception as e:
            self._display.warning(f"Dashboard update failed: {e}")
    
    def v2_playbook_on_start(self, playbook):
        data = {
            'event': 'playbook_start',
            'playbook': playbook._file_name,
            'timestamp': time.time()
        }
        self.send_update(data)
    
    def v2_runner_on_ok(self, result):
        data = {
            'event': 'task_success',
            'host': result._host.get_name(),
            'task': result._task.get_name(),
            'timestamp': time.time()
        }
        self.send_update(data)
    
    def v2_runner_on_failed(self, result, ignore_errors=False):
        data = {
            'event': 'task_failed',
            'host': result._host.get_name(),
            'task': result._task.get_name(),
            'error': result._result.get('msg', 'Unknown error'),
            'timestamp': time.time()
        }
        self.send_update(data)