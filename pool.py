
class ConnectionPool:

    def __init__(self, connection, status = True, number = 10):
        self.connection = connection
        self.status = status
        self.number = number
        self.pool = [[self.connection, self.status] for _ in range(self.number)]


    def check_free_connections(self):
        """return amout of free connections"""
        return len([conn for conn in self.pool if conn[1] == True])


    def get_first_free_connection(self):
        """return index of first free conn in pool"""
        g = (e for e, conn in enumerate(self.pool) if conn[1] == True)
        return next(g)


    def set_connection_status(self, connection, status):
        """return tuple obj example: (conn_obj, True)"""
        connection[1] = status
        return connection


    def update_connection_obj_in_pool(self, connection, index):
        self.pool[index] = connection
        return self.pool[index]

    
    def get_connection(self):
        if len(self.pool) <= 100:
            free_connections = self.check_free_connections()
            # print(f'free: {free_connections}, list_conn: {len(self.pool)}' )
            if free_connections == 0:
                self.create_additional_connection()

            index = self.get_first_free_connection()
            connection = self.pool[index]
            conn_in_use = self.set_connection_status(connection, False)
            self.update_connection_obj_in_pool(conn_in_use, index)
            return (conn_in_use, index)
        # print('Refused')
        return ConnectionRefusedError

    
    def return_connection(self, connection, index):
        conn_free = self.set_connection_status(connection, True)
        self.update_connection_obj_in_pool(conn_free, index)
        return self.pool


    def create_additional_connection(self):
        return self.pool.append([self.connection, self.status])


    def destroy_connection(self):
        """remove free connections if pool > 10"""
        if len(self.pool) > 10:
            for index, conn in enumerate(self.pool):
                if conn[1] is True:
                    self.pool.pop(index)
        return self.pool
