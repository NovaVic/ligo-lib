import os


class Utils(object):
    @staticmethod
    def _make_gen(reader):
        """Generator function via reader"""
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    @staticmethod
    def file_len(fname):
        """Counts number of lines in file fname"""
        if not os.path.isfile(fname):
            return 0

        f = open(fname, 'rb')
        f_gen = Utils._make_gen(f.raw.read)
        return sum(buf.count(b'\n') for buf in f_gen)

    @staticmethod
    def load_json(json_path):
        """Parses a JSON Project file at json_path"""
        import json

        with open(json_path) as data_file:
            project = json.load(data_file)

        return project

    @staticmethod
    def load_project_data(json_filename):
        """Parses the JSON Project json_filename and applies a task_uuid"""
        import uuid

        project = Utils.load_json(os.path.join(os.path.dirname(__file__),
                                               'data', json_filename))

        # Add task_uuid to this project
        if 'task_uuid' not in project:
            project['task_uuid'] = uuid.uuid4().hex
        return project
