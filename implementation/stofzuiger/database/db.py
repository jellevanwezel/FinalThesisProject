import psycopg2 as pg
import pandas as pd

class db:

    username='valuea'
    password='valuea'
    dbname='valuea'
    host='localhost'

    def __init__(self):
        self.connection = None


    def connect(self):
        try:
            self.connection = pg.connect(dbname=self.dbname, user=self.username, password=self.password, host=self.host)
        except pg.DatabaseError as e:
            print("\nAn OperationalError occurred. Error number {0}: {1}.".format(e.args[0], e.args[1]))

    def do_query(self, query):

        df = pd.DataFrame()
        for chunk in pd.read_sql(query, con=self.connection, chunksize=5000):
            df = df.append(chunk)

        return df


    def get_kb_roots(self):
        return self.do_query((
                    "SELECT pip.* "
                    "FROM kb.measurepoint mp "
                    "JOIN kb.measurepointcode mpc "
                    "ON mp.code_id = mpc.id "
                    "JOIN kb.pipesegment pip "
                    "ON mpc.id = pip.measurepoint_in "
                    "WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL"
         ))

    def get_kb_measurements(self,root_id):
        return self.do_query((
            "WITH RECURSIVE search_graph(id, parent, depth, root) AS ( "
                "SELECT pip.id, pip.parent_id, 1, pip.id "
                "FROM kb.measurepoint mp "
                "JOIN kb.measurepointcode mpc "
                "ON mp.code_id = mpc.id "
                "JOIN kb.pipesegment pip "
                "ON mpc.id = pip.measurepoint_in "
                "WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL AND pip.id = " + str(root_id) + " "
                "UNION ALL "
                "SELECT pipc.id, pipc.parent_id, search_graph.depth + 1, search_graph.root "
                "FROM kb.pipesegment pipc, search_graph "
                "WHERE pipc.parent_id = search_graph.id ) "
            "SELECT "
                "mpc.id as measurepoint_id, "
                "rec.date, "
                "mes.id as measurement_id, "
                "mes.characteristic_id, "
                "mes.value, "
                "mes.comments "
            "FROM search_graph "
            "JOIN kb.pipesegment pip "
            "ON pip.id = search_graph.id "
            "JOIN kb.measurepointcode mpc "
            "ON pip.measurepoint_in = mpc.id "
            "JOIN kb.measurepoint mp "
            "ON mpc.id = mp.code_id "
            "JOIN kb.recording rec "
            "ON mp.id = rec.measurepoint_id "
            "JOIN kb.measurement mes "
            "ON rec.id = mes.recording_id "
            "WHERE mp.valid_to > now() AND (mes.characteristic_id = 3) "
        ))

