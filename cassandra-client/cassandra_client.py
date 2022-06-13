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

        self.domains_insert = self.session.prepare(
            "INSERT INTO domains (domain)"
            "VALUES (?)")
        self.page_user_insert = self.session.prepare(
            "INSERT INTO page_user (domain, page_name, user_id, page_id)"
            "VALUES (?, ?, ?, ?)")
        self.page_domains_insert = self.session.prepare(
            "INSERT INTO page_domains (domain, page_id)"
            "VALUES (?, ?)")
        self.pages_info_insert = self.session.prepare(
            "INSERT INTO pages_info (page_id, page_name, domain, created_at)"
            "VALUES (?, ?, ?, ?)")
        self.page_users_info_insert = self.session.prepare(
            "INSERT INTO page_users_info (user_id, username, page_id, created_at)"
            "VALUES (?, ?, ?, ?)")
        self.domains_select = self.session.prepare(
            "SELECT DISTINCT domain FROM domains;")
        self.page_user_select = self.session.prepare(
            "SELECT page_name, domain FROM page_user "
            "WHERE user_id = ?;")
        self.page_domains_select = self.session.prepare(
            "SELECT COUNT(page_id) FROM page_domains "
            "WHERE domain = ?;")
        self.pages_info_select = self.session.prepare(
            "SELECT page_name, domain, created_at FROM pages_info "
            "WHERE page_id = ?;")
        self.page_users_info_select = self.session.prepare(
            "SELECT user_id, username, COUNT(page_id) FROM page_users_info "
            "WHERE (created_at > ?) AND (created_at < ?) GROUP BY user_id ALLOW FILTERING;")

    def insert_to_domains(self, domain):
        self.session.execute(self.domains_insert, (domain,))
    
    def insert_to_page_user(self, domain, page_name, user_id, page_id):
        self.session.execute(self.page_user_insert, (domain, page_name, user_id, page_id))

    def insert_to_page_domains(self, domain, page_id):
        self.session.execute(self.page_domains_insert, (domain, page_id))
    
    def insert_to_pages_info(self, page_id, page_name, domain, created_at):
        self.session.execute(self.pages_info_insert, (page_id, page_name, domain, created_at))
    
    def insert_to_page_users_info(self, user_id, username, page_id, created_at):
        self.session.execute(self.page_users_info_insert, (user_id, username, page_id, created_at))

    def select_from_domains(self, data):
        return list(self.session.execute(self.domains_select))
    
    def select_from_page_user(self, data):
        user_id = data['user_id']
        return list(self.session.execute(self.page_user_select, (user_id,)))
    
    def select_from_page_domains(self, data):
        domain = data['domain']
        return list(self.session.execute(self.page_domains_select, (domain,)))
    
    def select_from_pages_info(self, data):
        page_id = data['page_id']
        return list(self.session.execute(self.pages_info_select, (page_id,)))
    
    def select_from_page_users_info(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        return list(self.session.execute(self.page_users_info_select, (start_time, end_time)))
    
    def update_tables(self, data):
        page_id, created_at, domain, page_name, user_id, username = data
        self.insert_to_domains(domain)
        self.insert_to_page_user(domain, page_name, user_id, page_id)
        self.insert_to_page_domains(domain, page_id)
        self.insert_to_pages_info(page_id, page_name, domain, created_at)
        self.insert_to_page_users_info(user_id, username, page_id, created_at)

    def shutdown(self):
        self.session.shutdown()
