from . import nodes


class Session(object):
    """
    Class organizing lambda function lifecycle
    """

    def __init__(self, source_path: str):
        assert type(source_path) is str
        self.source_path = source_path
        self.filename = source_path.rsplit("/", 1)[1]

    def read_stops(self):
        self.stops = nodes.read_excel_file(path=self.source_path)

    def process_stops(self):
        self.stops = self.stops \
            .pipe(lambda x: nodes.expand_name(stops=x, fname=self.filename)) \
            .pipe(nodes.expand_processing_time) \
            .pipe(nodes.generate_id)
