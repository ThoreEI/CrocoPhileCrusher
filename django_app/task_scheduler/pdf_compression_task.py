from django_app.task_scheduler.processing_task import ProcessingTask
from pdfcompressor.pdfcompressor import PDFCompressor


class PdfCompressionTask(ProcessingTask):

    def run(self):
        print("Finished task " + str(self.task_id))
        event_handler = [super()._get_process_stats_event_handler()]
        PDFCompressor(event_handler=event_handler, **self._parameters).compress()
        self.finish_task()