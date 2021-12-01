import psycopg2
import random

# Notes: need to add hospital if there is none; make patients and doctors select hosptial on login in
# possibly make admin role that can create hospitals

class Connection(object):

    def __init__(self, user, password) -> None:
        super().__init__()
        self.__conn = psycopg2.connect(database="project425", user=user, password=password, host = "127.0.0.1", port = "5432")
        self.__cur = self.__conn.cursor()

    def add_hospital(self, name, city, state, hcost):
        cur = self.__cur
        query = "INSERT INTO public.\"Hospital\"(id, \"name\", city, state, hcost) VALUES (%s, %s, %s, %s, %s)"
        cur.execute("SELECT id FROM public.\"Hospital\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        try:
            cur.execute(query=query, vars=(curr_id, name, city, state, hcost))
        except Exception as e: # TODO go through and add more exceptions
            print(e)
            return

        self.__conn.commit()

    def add_doctor(self, username, password, name, organspec, dob, email, phone, h_id):
        """Add doctor is intended to be called when the user is dbadmin, it will both add a doctor to the database and create a new role"""
        cur = self.__cur
        query = "INSERT INTO public.\"Doctor\"(id, \"name\", organspec, dob, email, phone, h_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute("SELECT id FROM public.\"Doctor\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        # Add doctor to database
        try:
            cur.execute(query=query, vars=(curr_id, name, organspec, dob, email, phone, h_id))
        except Exception as e: # TODO go through and add more exceptions
            print(e)
            return

        # create doctor role
        query = f"CREATE ROLE {username} WITH login"
        try:
            cur.execute(query=query)
        except Exception as e: # TODO go through and add more exceptions
            print('create role', e)
            return

        # change password
        query = f"ALTER ROLE {username} WITH PASSWORD \'{password}\'"
        try:
            cur.execute(query=query)
        except Exception as e: # TODO go through and add more exceptions
            print('createpassword', e)
            return
        
        # grant doctor privileges
        query = f"GRANT doctor to {username}"
        try:
            cur.execute(query=query, vars=(username))
        except Exception as e: # TODO go through and add more exceptions
            print('grant privileges', e)
            return

        self.__conn.commit()

    def add_patient(self, name, bloodtype, dob, requestedorgan, email, phone, dr_id):
        cur = self.__cur
        query = "INSERT INTO public.\"Patient\"(\"name\", bloodtype, dob, requestedorgan, email, phone, id, dr_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute("SELECT id FROM public.\"Patient\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        try:
            cur.execute(query=query, vars=(name, bloodtype, dob, requestedorgan, email, phone, curr_id, dr_id))
        except Exception as e: # TODO go through and add more exceptions
            print(e)
            return

        self.__conn.commit()

    def add_Bdonor(self, name, bloodtype, dob, chronicilness, drugusage, medicalhistory, lastdonation, city, state, email, phone):
        cur = self.__cur
        query = "INSERT INTO public.\"BloodDonor\"(\"name\", bloodtype, dob, chronicillness, drugusage, medicalhistory, lastdonation, city, state, email, phone, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        
        # generate a unique id
        cur.execute("SELECT id FROM public.\"BloodDonor\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

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
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        try:
            cur.execute(query=query, vars=(name, bloodtype, dob, chronicilness, drugusage, medicalhistory, lastdonation, city, state, email, phone, curr_id))
        except Exception as e: # TODO go through and add more exceptions
            print(e)

        self.__conn.commit()

    def add_organ(self, organname, availabledate, donateiondate, life, p_id, dn_id, dr_id):
        cur = self.__cur
        query = "INSERT INTO public.\"Organ\"(organname, availabledate, donateiondate, life, p_id, dn_id, dr_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        try:
            cur.execute(query=query, vars=(organname, availabledate, donateiondate, life, p_id, dn_id, dr_id))
        except Exception as e: # TODO go through and add more exceptions
            print(e)

        self.__conn.commit()

    def add_blood(self, bloodtype, availabledate, donateiondate, life, p_id, dn_id, dr_id):
        cur = self.__cur
        query = "INSERT INTO public.\"Blood\"(bloodtype, availabledate, donateiondate, life, p_id, dn_id, dr_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        try:
            cur.execute(query=query, vars=(bloodtype, availabledate, donateiondate, life, p_id, dn_id, dr_id))
        except Exception as e: # TODO go through and add more exceptions
            print(e)

        self.__conn.commit()

    def get_patient_info(self):
        cur = self.__cur
        query = "SELECT * FROM public.\"Patient\""
        try:
            cur.execute(query)
            return cur.fetchall()
        except psycopg2.errors.InsufficientPrivilege as insfpr:
            return insfpr

    def get_blood_list(self):
        cur = self.__cur
        query = "SELECT * FROM public.\"Blood\""
        try:
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            print(e)
            return None

    def get_organ_list(self):
        cur = self.__cur
        query = "SELECT * FROM public.\"Organ\""
        try:
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            print(e)
            return None

    def on_exit(self):
        self.__cur.close()
        self.__conn.close()

if __name__ == "__main__":
    cnn = Connection(user="hspadmin", password="password")
    # cnn.add_hospital('mercy', 'Chicago', 'IL', 100)
    # print(cnn.get_patient_info())
    # cnn.add_doctor(username='dsmith', password='password', name='Dr_Smith', organspec='Kidney', dob='2002-01-30', email='smith@mercy.org', phone='1098765432', h_id=1639736916)
    # cnn.add_patient(name='name', bloodtype='AB+', dob='2000-01-01', requestedorgan='kidney', email='something@test.com', phone='1234567890', dr_id='50413')
    cnn.on_exit()
