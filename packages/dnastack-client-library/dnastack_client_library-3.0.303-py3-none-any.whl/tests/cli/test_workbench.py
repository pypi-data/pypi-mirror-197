from .base import WorkbenchCliTestCase


class TestWorkbenchCommand(WorkbenchCliTestCase):
    @staticmethod
    def reuse_session() -> bool:
        return True

    def setUp(self) -> None:
        super().setUp()
        self.invoke('use', f'{self.workbench_base_url}/api/service-registry')

    def test_runs_list(self):
        self.submit_hello_world_workflow_batch()

        runs = self.simple_invoke('alpha', 'workbench', 'runs', 'list')
        self.assert_not_empty(runs, 'Expected at least one run.')
