import psycopg2

conn = psycopg2.connect(database="project425", user = "jamie", password = "password", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

# cur.execute("INSERT INTO public.\"Patient\"(\"name\", bloodtype, dob, requestedorgan, email, phone, id) VALUES (%s, %s, %s, %s, %s, %s, %s);", ('jamie', 'O+', '2001-10-06', 'Kidney', 'jamisonkerney@gmail.com', '3127312822', 1))

query = f"""SELECT * FROM public.\"Patient\""""
cur.execute(query=query)
print(cur.fetchone())
print(cur.fetchone())

# conn.commit()
conn.close()
cur.close()

class Database(object):

    def __init__(self, user, password) -> None:
        super().__init__()
        self.__conn = psycopg2.connect(database="project425", user=user, password=password, host = "127.0.0.1", port = "5432")
        self.__cur = conn.cursor()

    def add_donor():
        pass

    def add_organ():
        pass
    
    def get_patient_info():
        pass

    def get_blood_list():
        pass

    def get_organ_list():
        pass


def organ_report(db: Database):
    pass