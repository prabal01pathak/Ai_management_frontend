from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable
# traceback
import traceback
import sys
import json

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(str)

class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.result

    @pyqtSlot()
    def run(self):
        '''
        Run the worker function
        '''
        print('run')
        try:
            print('run try')
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(str(result))  # Return the result of the processing
        except Exception as e:
            print("Run error: {}".format(e))
        finally:
            self.signals.finished.emit()
