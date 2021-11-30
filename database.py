import psycopg2
import random

# conn = psycopg2.connect(database="project425", user = "jamie", password = "password", host = "127.0.0.1", port = "5432")
# cur = conn.cursor()
# 
# cur.execute("INSERT INTO public.\"Patient\"(\"name\", bloodtype, dob, requestedorgan, email, phone, id) VALUES (%s, %s, %s, %s, %s, %s, %s);", ('jamie', 'O+', '2001-10-06', 'Kidney', 'jamisonkerney@gmail.com', '3127312822', 1))
# 
# query = f"""SELECT * FROM public.\"Patient\""""
# cur.execute(query=query)
# print(cur.fetchone())
# print(cur.fetchone())
# 
# conn.commit()
# conn.close()
# cur.close()

class Connection(object):

    def __init__(self, user, password) -> None:
        super().__init__()
        self.__conn = psycopg2.connect(database="project425", user=user, password=password, host = "127.0.0.1", port = "5432")
        self.__cur = self.__conn.cursor()

    def add_Bdonor(self, name, bloodtype, dob, chronicilness, drugusage, medicalhistory, lastdonation, city, state, email, phone):
        cur = self.__cur
        query = "INSERT INTO public.\"BloodDonor\"(\"name\", bloodtype, dob, chronicillness, drugusage, medicalhistory, lastdonation, city, state, email, phone, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        
        # generate a unique id
        cur.execute("SELECT id FROM public.\"BloodDonor\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 32 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 32 - 1)

        try:
            cur.execute(query=query, vars=(name, bloodtype, dob, chronicilness, drugusage, medicalhistory, lastdonation, city, state, email, phone, curr_id))
        except Exception as e: # TODO go through and add more exceptions
            print(e)

        self.__conn.commit()

    def add_Odonor(self, name, bloodtype, dob, chronicilness, drugusage, medicalhistory, lastdonation, city, state, organname, email, phone):
        cur = self.__cur
        query = "INSERT INTO public.\"BloodDonor\"(\"name\", bloodtype, dob, chronicillness, drugusage, medicalhistory, lastdonation, city, state, email, phone, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        
        # generate a unique id
        cur.execute("SELECT id FROM public.\"BloodDonor\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 32 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 32 - 1)

        try:
            cur.execute(query=query, vars=(name, bloodtype, dob, chronicilness, drugusage, medicalhistory, lastdonation, city, state, email, phone, curr_id))
        except Exception as e: # TODO go through and add more exceptions
            print(e)

    def add_organ(self):
        pass

    def get_patient_info(self):
        pass

    def get_blood_list(self):
        pass

    def get_organ_list(self):
        pass

    def on_exit(self):
        self.__cur.close()
        self.__conn.close()


def organ_report(cnn: Connection):
    pass