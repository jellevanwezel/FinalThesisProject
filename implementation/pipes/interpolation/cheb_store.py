import json


class ChebStore(object):
    def __init__(self, file_path):
        self.chebs = self.load_chebs_from_file(file_path)
        self.file_path = file_path

    def add_cheb(self, n, x, cheb):
        """Adds (or replaces) a cheb to the store"""
        if self.chebs.get(n) is None:
            self.chebs[n] = dict()
        self.chebs[n][x] = cheb

    def get_cheb(self, n, x):
        """gets a cheb from the store or returns None"""
        if self.chebs.get(n) is None:
            return None
        return self.chebs[n].get(x)

    def load_chebs_from_file(self, file_path):
        """
        Gets the chebs from a file or use an empty dict
        :param file_path: path to the file
        :return: the chebs dict
        :rtype: dict
        """
        try:
            with open(file_path, 'r') as file_chebs:
                chebs = json.load(file_chebs)
        except IOError:
            print "File:", file_path, "not found! Using empty dictionary."
            chebs = dict()
        return chebs

    def save_chebs_to_file(self):
        """Merges and saves the chebs to the file"""
        file_name = self.data_path
        saved_chebs = self.load_chebs_from_file()
        merged = ChebStore.merge_two_dicts(self.chebs, saved_chebs)
        with open(file_name, 'w') as outfile:
            json.dump(merged, outfile)

    def has_cheb(self, n, x):
        """Returns wether or not a cheb is in the store"""
        return self.get_cheb(n, x) is not None

    @staticmethod
    def merge_two_dicts(d1, d2):
        """Helper function to merge two dictionries"""
        merged = d1.copy()
        merged.update(d2)
        return merged
