import time
import random
import multiprocessing

class ConnectionPool:
    def __init__(self, max_connections):
        """
        Initializes the ConnectionPool with a list of connections and a semaphore.
        :param max_connections: Maximum number of concurrent connections.
        """
        self.max_connections = max_connections
        # Pool of connections
        self.connections = [f"Connection-{i+1}" for i in range(max_connections)]
        # Semaphore with a count equal to the number of available connections.
        self.semaphore = multiprocessing.Semaphore(max_connections)
        # Lock to protect access to the connection list.
        self.lock = multiprocessing.Lock()

    def get_connection(self):
        """
        Acquire a connection from the pool.
        Blocks if no connection is available.
        :return: A connection identifier.
        """
        self.semaphore.acquire()
        with self.lock:
            if self.connections:
                connection = self.connections.pop(0)
                return connection
            else:
                return None

    def release_connection(self, connection):
        """
        Releases a connection back to the pool.
        :param connection: The connection to be released.
        """
        with self.lock:
            self.connections.append(connection)
        self.semaphore.release()

def access_database(pool):
    """
    Simulates a process performing a database operation:
      - Acquires a connection,
      - Prints a message when it acquires the connection,
      - Sleeps for a random duration to simulate work,
      - Releases the connection and prints a message.
    :param pool: An instance of ConnectionPool.
    """
    process_name = multiprocessing.current_process().name
    print(f"\n{process_name} is waiting for a connection...")
    connection = pool.get_connection()
    if connection:
        print(f"\n{process_name} has acquired {connection}.")
        # Database operation simulation
        time.sleep(random.uniform(1, 5))
        pool.release_connection(connection)
        print(f"\n{process_name} has released {connection}.")
    else:
        print(f"\n{process_name} did not get a connection.")