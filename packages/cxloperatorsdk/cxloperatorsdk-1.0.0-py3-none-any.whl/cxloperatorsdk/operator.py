from cxloperatorsdk.run_status import RunStatus
from cxloperatorsdk.operator_exception import OperatorException


class Operator:
    def __init__(self):
        self.status = None
        self.error = None

    # prepare is a place holder/hook method, which allows operator developers to plug in all necessary preparations
    # before running the operator
    def prepare(self):
        # TODO: initialize and prepare the operator
        self.status = RunStatus.PENDING


    def run(self):
        self.prepare()

        self.status = RunStatus.RUNNING

        try:
            self.execute()

            self.status = RunStatus.SUCCESS
        except Exception as exp:
            self.status = RunStatus.FAILED
            self.error = exp

    # execute is the method where the real business logic is implemented. Operator developer must override this method
    # for an operator to work properly. The default implementation throws an OperatorException, which will always put
    # the operator in a failed state
    def execute(self):
        raise OperatorException('Failed')