class ConnectionPool:

    def __init__(self, connection, in_use = False, number = 10, max_conn = 100):
        self.connection = connection
        self.in_use = in_use
        self.number = number
        self.max_conn = max_conn
        self.pool = [[self.connection, self.in_use] for _ in range(self.number)]


    def check_free_connections(self):
        """return amout of free connections"""
        return len([conn for conn in self.pool if conn[1] is False])


    def get_first_free_connection(self):
        """return index of first free conn in pool or info str"""
        try:
            g = (e for e, conn in enumerate(self.pool) if conn[1] is False)
            index = next(g)
        except StopIteration:
            return f"WARNINIG: NO free connections now!"
        return self.pool[index]


    def set_connection_status_occupied(self, connection):
        connection[1] = True
        return connection


    def create_additional_connection_if_needed(self):
        """
        check if no free connections. if no free conns - add one
        """
        
        free_connections = self.check_free_connections() #int
        if free_connections == 0:
            self.pool.append([self.connection, self.in_use])
            return self.pool[-1]
        return None

    
    def get_connection(self):
        if len(self.pool) <= self.max_conn:
            self.create_additional_connection_if_needed()
            free_conn = self.get_first_free_connection()
            self.set_connection_status_occupied(free_conn)
            return free_conn
        return "Pool can't allow add more connections"


    


    
    # def return_connection(self, connection, index):
    #     conn_free = self.set_connection_status(connection, True)
    #     self.update_connection_obj_in_pool(conn_free, index)
    #     return self.pool





    # def destroy_connection(self):
    #     """remove free connections if pool > 10"""
    #     if len(self.pool) > 10:
    #         for index, conn in enumerate(self.pool):
    #             if conn[1] is True:
    #                 self.pool.pop(index)
    #     return self.pool

p2 = ConnectionPool("DB")
p2.pool = [p2.set_connection_status_occupied(conn) for conn in p2.pool]
print(p2.pool)
additional_conn = p2.create_additional_connection_if_needed()
print(additional_conn)


