# from . import nodes


class Session(object):
    """
    Class organizing lambda function lifecycle
    """

    def __init__(self, source_path: str):
        assert type(source_path) is str
        self.source_path = source_path
        self.filename = source_path.rsplit("/", 1)[1]

    # def read_file(self, source_path: str):
    #     self.stops = nodes.read_excel_file(
    #         path=source_path,
    #     )
    #     self.__source_path

    # def process_stops(self):
    #     self.stops = self.stops \
    #         .pipe(lambda x: nodes.expand_name(stops=x, path=SRC_S3_FPATH)) \
    #         .pipe(nodes.expand_processing_time) \
    #         .pipe(nodes.generate_id)
