from datetime import date
from math import pi
from sys import exec_prefix
from PyQt5.QtCore import qUnregisterResourceData
import psycopg2
import random

# Notes: need to add hospital if there is none; make patients and doctors select hosptial on login in
# possibly make admin role that can create hospitals

class Connection(object):

    def __init__(self, user, password) -> None:
        super().__init__()
        self.user = user
        self.__conn = psycopg2.connect(database="project425", user=user, password=password, host = "127.0.0.1", port = "5432")
        self.__cur = self.__conn.cursor()


    def get_dr_id(self):
        cur = self.__cur
        query = f"SELECT id FROM public.\"Doctor\" WHERE username = \'{self.user}\'"
        try:
            cur.execute(query)
            return cur.fetchall()[0][0]
        except Exception as e:
            print(type(e), e)
            return None

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
        cur.execute("SELECT id FROM public.\"Doctor\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        # Add doctor to database
        query = f"INSERT INTO public.\"Doctor\"(id, \"name\", organspec, dob, email, phone, h_id, username) VALUES ({curr_id}, \'{name}\', \'{organspec}\', \'{dob}\', \'{email}\', \'{phone}\', {h_id}, \'{username}\')"
        try:
            cur.execute(query=query)
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

    def create_doc_acc(self, username, password):
        cur = self.__cur
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

    def create_pat_acc(self, username, password):
        cur = self.__cur
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
        query = f"GRANT patient to {username}"
        try:
            cur.execute(query=query, vars=(username))
        except Exception as e: # TODO go through and add more exceptions
            print('grant privileges', e)
            return

    def add_patient(self, username, password, name, bloodtype, dob, requestedorgan, email, phone, dr_id, requestedblood='FALSE'):
        """Add patient is intended to be called when the user is dbadmin, it will both add a doctor to the database and create a new role"""
        cur = self.__cur
        cur.execute("SELECT id FROM public.\"Patient\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        # Add patient to database
        query = f"INSERT INTO public.\"Patient\"(\"name\", bloodtype, dob, requestedorgan, requestedblood, email, phone, id, dr_id, username) VALUES (\'{name}\', \'{bloodtype}\', \'{dob}\', \'{requestedorgan}\', {requestedblood}, \'{email}\', \'{phone}\', {curr_id}, {dr_id}, \'{username}\')"
        try:
            cur.execute(query=query)
        except Exception as e: # TODO go through and add more exceptions
            print('add patient', type(e), e)
            return

        # create patient role
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
        
        # grant patient privileges
        query = f"GRANT patient to {username}"
        try:
            cur.execute(query=query, vars=(username))
        except Exception as e: # TODO go through and add more exceptions
            print('grant privileges', e)
            return

        self.__conn.commit()

    def add_Bdonor(self, name, bloodtype, dob, chronicilness, drugusage, medicalhistory, lastdonation, city, state, email, phone):
        cur = self.__cur

        # generate a unique id
        cur.execute("SELECT id FROM public.\"BloodDonor\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        query = f"INSERT INTO public.\"BloodDonor\"(\"name\", bloodtype, dob, chronicillness, drugusage, medicalhistory, lastdonation, city, state, email, phone, id) \
            VALUES (\'{name}\', \'{bloodtype}\', \'{dob}\', \'{chronicilness}\', \'{drugusage}\', \'{medicalhistory}\', \'{lastdonation}\', \'{city}\', \'{state}\', \'{email}\', \'{phone}\', {curr_id});"

        try:
            cur.execute(query=query)
        except Exception as e: # TODO go through and add more exceptions
            print(e)

        self.__conn.commit()

    def add_Odonor(self, name, bloodtype, dob, chronicilness, drugusage, medicalhistory, city, state, organname, email, phone):
        cur = self.__cur
        
        # generate a unique id
        cur.execute("SELECT id FROM public.\"OrganDonor\"")
        ids = cur.fetchall()
        curr_id = random.randint(0, 2 ** 16 - 1)
        while curr_id in ids:
            curr_id = random.randint(0, 2 ** 16 - 1)

        query = f"INSERT INTO public.\"OrganDonor\"(\"name\", bloodtype, dob, chronicillness, drugusage, medicalhistory, city, state, organname, email, phone, id) \
            VALUES (\'{name}\', \'{bloodtype}\', \'{dob}\', \'{chronicilness}\', \'{drugusage}\', \'{medicalhistory}\', \'{city}\', \'{state}\', \'{organname}\', \'{email}\', \'{phone}\', {curr_id});"
        try:
            cur.execute(query=query)
        except Exception as e: # TODO go through and add more exceptions
            print(e)

        self.__conn.commit()

    def add_organ(self, organname, availabledate, donationdate, life, p_id, dn_id, dr_id):
        cur = self.__cur
        query = f"INSERT INTO public.\"Organ\"(organname, availabledate, donationdate, life, p_id, dn_id, dr_id) \
            VALUES (\'{organname}\', \'{availabledate}\', \'{donationdate}\', {life}, {p_id}, {dn_id}, {dr_id});"
        try:
            cur.execute(query=query)
        except Exception as e: # TODO go through and add more exceptions
            print('insert organ', type(e), e)

        self.__conn.commit()

    def add_fee(self, p_id, h_id):
        cur = self.__cur
        query = f"INSERT INTO public.\"PaysFee\"(p_id, h_id) VALUES({p_id}, {h_id});"
        try:
            cur.execute(query=query)
        except Exception as e:
            print('could not add fee', type(e), e)

        self.__conn.commit()

    def add_blood(self, bloodtype, donationdate, life, p_id, dn_id, dr_id):
        cur = self.__cur
        query = f"INSERT INTO public.\"Blood\"(bloodtype, donationdate, life, p_id, dn_id, dr_id) VALUES(\'{bloodtype}\', \'{donationdate}\', {life}, {p_id}, {dn_id}, {dr_id});"
        try:
            cur.execute(query=query)
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
        except Exception as e:
            print(type(e), e)


    def create_donation(self, name, dob, bloodtype, city, state, date, organ=None):
        cur = self.__cur
        dr_id = self.get_dr_id()
        if organ:
            # get patient who will receive
            query = f"SELECT id FROM public.\"Patient\" WHERE requestedorgan = \'{organ}\'"
            try:
                cur.execute(query)
            except Exception as e:
                print('getting patient', type(e), e)
                return
            p_id = cur.fetchone()
            if p_id == None:
                # TODO patient not found
                return
            p_id = p_id[0]

            query = f"SELECT id FROM public.\"OrganDonor\" \
                WHERE \"name\" = \'{name}\' AND bloodtype = \'{bloodtype}\' AND dob = \'{dob}\' AND city = \'{city}\' and state = \'{state}\'"
            try:
                cur.execute(query)
            except Exception as e:
                print('finding donor', type(e), e)
                return
            dn_id = cur.fetchone()
            if dn_id == None:
                # TODO donor not found
                return
            dn_id = dn_id[0]
            
            self.add_organ(organname=organ, availabledate=date, donationdate=date, life=7, p_id=p_id, dn_id=dn_id, dr_id=dr_id)

            query = f"SELECT h_id FROM public.\"Doctor\" WHERE id = {dr_id}"
            try:
                cur.execute(query=query)
            except Exception as e:
                print('failed getting h_id', type(e), e)
                return
            h_id = cur.fetchone()[0]

            self.add_fee(p_id=p_id, h_id=h_id)

        else:
            query = f"SELECT id FROM public.\"Patient\" WHERE requestedblood = \'TRUE\'"
            try:
                cur.execute(query)
            except Exception as e:
                print('getting', type(e), e)
                return
            p_id = cur.fetchone()
            if p_id == None:
                # TODO patient not found
                return
            p_id = p_id[0]
            
            query = f"SELECT id FROM public.\"BloodDonor\" \
                WHERE \"name\" = \'{name}\' AND bloodtype = \'{bloodtype}\' AND dob = \'{dob}\' AND city = \'{city}\' and state = \'{state}\'"
            try:
                cur.execute(query)
            except Exception as e:
                print(type(e), e)
                return
            dn_id = cur.fetchone()
            if dn_id == None:
                # TODO donor not found
                return
            dn_id = dn_id[0]
            
            self.add_blood(bloodtype=bloodtype, donationdate=date, life=7, p_id=p_id, dn_id=dn_id, dr_id=dr_id)

            query = f"SELECT h_id FROM public.\"Doctor\" WHERE id = {dr_id}"
            try:
                cur.execute(query=query)
            except Exception as e:
                print('failed getting h_id', type(e), e)
                return
            h_id = cur.fetchone()[0]

            self.add_fee(p_id=p_id, h_id=h_id)
        
    def get_hospitals_info(self, info=None):
        cur = self.__cur
        if info == None:
            query = f"SELECT * FROM public.\"Hospital\""
        else:
            query = f"SELECT {info} FROM public.\"Hospital\""
        try:
            cur.execute(query)
            return cur.fetchall()
        except psycopg2.errors.InsufficientPrivilege as insfpr:
            return insfpr

    def get_doctor_info(self, info=None):
        cur = self.__cur
        if info == None:
            query = f"SELECT * FROM public.\"Doctor\""
        else:
            query = f"SELECT {info} FROM public.\"Doctor\""
        try:
            cur.execute(query)
            return cur.fetchall()
        except psycopg2.errors.InsufficientPrivilege as insfpr:
            return insfpr

    def organ_donor_list(self, state, organ, doctor):
        cur = self.__cur

        # get doctor id from doctor name 
        query = f"""SELECT public.\"Doctor\".id 
        FROM public.\"Doctor\" INNER JOIN public.\"Hospital\" ON public.\"Doctor\".h_id = public.\"Hospital\".id
        WHERE public.\"Doctor\".\"name\" = \'{doctor}\' AND public.\"Hospital\".state = \'{state}\'
        """
        try:
            cur.execute(query)
        except Exception as e:
            print(e)
            return

        dr_ids = [str(e[0]) for e in cur.fetchall()]
        dr_id_str = f"({', '.join(dr_ids)})"

        # pull donor id from organ relation that match state, organ, and doctor
        query = f"SELECT dn_id FROM public.\"Organ\" WHERE dr_id IN {dr_id_str} AND organname = \'{organ}\'"
        print(query)
        try:
            cur.execute(query)
        except Exception as e:
            print(e)
            return

        dn_ids = cur.fetchall()
        dn_ids_str = f"({', '.join(dn_ids)})"

        # pull donors with donor id from above
        query = f"SELECT * FROM public.\"OrganDonor\" WHERE id IN {dn_ids_str}"
        try:
            cur.execute(query)
        except Exception as e:
            print(e)
            return

        return cur.fetchall()

    def on_exit(self):
        self.__cur.close()
        self.__conn.close()

if __name__ == "__main__":
    names = ['chloe', 'jamie', 'allison', 'ian', 'eta', 'dylan', 'xavier', 'imani', 'amber', 'joel', 'pooja']
    organs = ['heart', 'lung', 'kidney', 'liver']
    phonenumbers = [random.randint(10 ** 9, (10 ** 10) -1) for i in range(10000)]
    bloodtypes = ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']
    locations = [('Chicago', 'IL'), ('Indianapolis', 'IN'), ('Detriot', 'MI'), ('Des Moines', 'IA'), ('Madison', 'WI'), ('Minneapolis', 'MN')]
    
    # email = name + @test.com
    # dob = rand.randint(1900, 2020)-random.randint(1,12)-random.randint(1,28)

    # make a bunch of hospitals
    cnn = Connection(user="hspadmin", password="password")
    ''' 
    for i in range(20):
        l = random.choice(locations)
        cnn.add_hospital('h' + str(i), l[0], l[1], hcost=random.randint(300, 900))
    '''

    # make a bunch of doctors
    '''
    hospital_ids = [i[0] for i in cnn.get_hospitals_info(info='id')]
    for name in names:
        username = 'dr' + name
        cnn.add_doctor(username=username, password='password', name=name, organspec=random.choice(organs), dob=f'{random.randint(1900, 2020)}-{random.randint(1,12)}-{random.randint(1,28)}', email=name + '@dr.com', phone=random.choice(phonenumbers), h_id=random.choice(hospital_ids))
    '''

    # make a bunch of patients
    '''
    doctors_ids = [i[0] for i in cnn.get_doctor_info(info='id')]
    doctors_ids.pop(0)
    for name in names:
        cnn.add_patient(username='pt' + name, password='password', name=name, bloodtype=random.choice(bloodtypes), dob=f'{random.randint(1900, 2020)}-{random.randint(1,12)}-{random.randint(1,28)}', requestedorgan=random.choice(organs), email=name + '@pt.com', phone=random.choice(phonenumbers), dr_id=random.choice(doctors_ids))
    '''

    # make a bunch of organ donors
    '''
    doctors_ids = [i[0] for i in cnn.get_doctor_info(info='username')]
    print(doctors_ids)
    for i in range(100):
        location = random.choice(locations)
        name = random.choice(names)
        temp_cnn = Connection(user=random.choice(doctors_ids), password='password')
        temp_cnn.add_Odonor(name=name, bloodtype=random.choice(bloodtypes), dob=f'{random.randint(1900, 2020)}-{random.randint(1,12)}-{random.randint(1,28)}', chronicilness='None', drugusage='None', medicalhistory='None', lastdonation=f'2020-{random.randint(1,12)}-{random.randint(1,28)}', city=location [0], state=location[1], organname=random.choice(organs), email=name + '@donor.com', phone=random.choice(phonenumbers))
    '''

    # make a bunch of blood donors
    '''
    doctors_ids = [i[0] for i in cnn.get_doctor_info(info='username')]
    for i in range(100):
        location = random.choice(locations)
        name = random.choice(names)
        temp_cnn = Connection(user=random.choice(doctors_ids), password='password')
        temp_cnn.add_Bdonor(name=name, bloodtype=random.choice(bloodtypes), dob=f'{random.randint(1900, 2020)}-{random.randint(1,12)}-{random.randint(1,28)}', chronicilness='None', drugusage='None', medicalhistory='None', lastdonation=f'2020-{random.randint(1,12)}-{random.randint(1,28)}', city=location [0], state=location[1], email=name + '@donor.com', phone=random.choice(phonenumbers))
    '''
    # doctors_ids = [i[0] for i in cnn.get_doctor_info(info='id')]
    # cnn.add_patient(username='pt' + 'mercy', password='password', name='mercy', bloodtype=random.choice(bloodtypes), dob=f'{random.randint(1900, 2020)}-{random.randint(1,12)}-{random.randint(1,28)}', requestedorgan='NULL', email='mercy@pt.com', phone=random.choice(phonenumbers), dr_id=random.choice(doctors_ids), requestedblood='TRUE')

    # print(cnn.organ_donor_list(state='MI', organ='kidney', doctor='ian'))

    cnn.on_exit()
