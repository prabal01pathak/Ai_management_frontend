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
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(json.dumps(result))  # Return the result of the processing
        finally:
            self.signals.finished.emit()
