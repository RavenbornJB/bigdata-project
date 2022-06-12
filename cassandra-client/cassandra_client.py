from cassandra.cluster import Cluster


class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)
    
    def insert_to_domains(self, domain):
        self.session.execute(f"INSERT INTO domains (domain)"
                             f"VALUES ({domain})")
    
    def insert_to_page_user(self, domain, page_name, user_id):
        self.session.execute(f"INSERT INTO page_user (domain, page_name, user_id)"
                             f"VALUES ({domain}, {page_name}, {user_id})")

    def insert_to_page_domains(self, domain, page_id):
        self.session.execute(f"INSERT INTO page_domains (domain, page_id)"
                             f"VALUES ({domain}, {page_id})")
    
    def insert_to_pages_info(self, page_id, page_name, domain, created_at):
        self.session.execute(f"INSERT INTO pages_info (domain, page_name, user_id)"
                             f"VALUES ({page_id}, {page_name}, {domain}, {created_at})")
    
    def insert_to_page_users_info(self, user_id, username, page_id, created_at):
        self.session.execute(f"INSERT INTO page_users_info (user_id, username, page_id, created_at)"
                             f"VALUES ({user_id}, {username}, {page_id}, {created_at})")

    def select_from_domains(self, data):
        query = f"SELECT DISTINCT domain FROM domains;"
        return list(self.session.execute(query))
    
    def select_from_page_user(self, data):
        user_id = data['user_id']
        query = f"SELECT page_name, domain FROM page_user \
                  WHERE user_id = {user_id};"
        return list(self.session.execute(query))
    
    def select_from_page_domains(self, data):
        domain = data['domain']
        query = f"SELECT COUNT(page_id) FROM page_domains \
                  WHERE domain = {domain};"
        return list(self.session.execute(query))
    
    def select_from_pages_info(self, data):
        page_id = data['page_id']
        query = f"SELECT page_name, domain, created_at FROM pages_info \
                  WHERE page_id = {page_id};"
        return list(self.session.execute(query))
    
    def select_from_page_users_info(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        query = f"SELECT user_id, username, COUNT(page_id) FROM page_users_info \
                  WHERE (COUNT(page_id) > 0) AND (created_at > {start_time}) AND (created_at < {end_time});"
        return list(self.session.execute(query))
    
    def update_tables(self, data):
        page_id, created_at, domain, page_name, user_id, username = data
        self.insert_to_domains(domain)
        self.insert_to_page_user(domain, page_name, user_id)
        self.insert_to_page_domains(domain, page_id)
        self.insert_to_pages_info(page_id, page_name, domain, created_at)
        self.insert_to_page_users_info(user_id, username, page_id, created_at)

    def shutdown(self):
        self.session.shutdown()
