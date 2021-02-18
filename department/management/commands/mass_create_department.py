from django.core.management import BaseCommand

from department.models import UserDepartment, GRC, Division


class Command(BaseCommand):
    def handle(self, **args):
        user_department, created = UserDepartment.objects.get_or_create(department_name='Central Regional Office')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Ang Mo Kio GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Ang Mo Kio-Hougang', grc=grc)
        Division.objects.get_or_create(division_name='Cheng San-Seletar', grc=grc)
        Division.objects.get_or_create(division_name='Jalan Kayu', grc=grc)
        Division.objects.get_or_create(division_name='Teck Ghee', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Kebun Baru SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Kebun Baru', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Yio Chu Kang SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Yio Chu Kang', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Bishan-Toa Payoh GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Bishan East-Sin Ming', grc=grc)
        Division.objects.get_or_create(division_name='Toa Payoh Central', grc=grc)
        Division.objects.get_or_create(division_name='Toa Payoh East', grc=grc)
        Division.objects.get_or_create(division_name='Toa Payoh West-Thomson', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Marymount SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Marymount', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Jalan Besar GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Kampong Glam', grc=grc)
        Division.objects.get_or_create(division_name='Kolam Ayer', grc=grc)
        Division.objects.get_or_create(division_name='Kreta Ayer-Kim Seng', grc=grc)
        Division.objects.get_or_create(division_name='Whampoa', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Potong Pasir SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Potong Pasir', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Radin Mas SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Radin Mas', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Tanjong Pagar GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Buona Vista', grc=grc)
        Division.objects.get_or_create(division_name='Henderson-Dawson', grc=grc)
        Division.objects.get_or_create(division_name='Moulmein-Cairnhill', grc=grc)
        Division.objects.get_or_create(division_name='Queenstown', grc=grc)
        Division.objects.get_or_create(division_name='Tanjong Pagar-Tiong Bahru', grc=grc)


        # ERO
        user_department, created = UserDepartment.objects.get_or_create(department_name='Eastern Regional Office')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Aljunied GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Bedok Reservoir-Punggol', grc=grc)
        Division.objects.get_or_create(division_name='Eunos', grc=grc)
        Division.objects.get_or_create(division_name='Kaki Bukit', grc=grc)
        Division.objects.get_or_create(division_name='Paya Lebar', grc=grc)
        Division.objects.get_or_create(division_name='Serangoon', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Hougang SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Hougang', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Pasir Ris-Punggol GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Pasir Ris Central', grc=grc)
        Division.objects.get_or_create(division_name='Pasir Ris East', grc=grc)
        Division.objects.get_or_create(division_name='Pasir Ris West', grc=grc)
        Division.objects.get_or_create(division_name='Punggol Coast', grc=grc)
        Division.objects.get_or_create(division_name='Punggol Shore', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Punggol West SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Punggol West', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Sengkang GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Anchorvale', grc=grc)
        Division.objects.get_or_create(division_name='Buangkok', grc=grc)
        Division.objects.get_or_create(division_name='Compassvale', grc=grc)
        Division.objects.get_or_create(division_name='Rivervale', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Tampines GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Tampines Central', grc=grc)
        Division.objects.get_or_create(division_name='Tampines Changkat', grc=grc)
        Division.objects.get_or_create(division_name='Tampines East', grc=grc)
        Division.objects.get_or_create(division_name='Tampines North', grc=grc)
        Division.objects.get_or_create(division_name='Tampines West', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='East Coast GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Bedok', grc=grc)
        Division.objects.get_or_create(division_name='Changi Simei', grc=grc)
        Division.objects.get_or_create(division_name='Fengshan', grc=grc)
        Division.objects.get_or_create(division_name='Kampong Chai Chee', grc=grc)
        Division.objects.get_or_create(division_name='Siglap', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='MacPherson SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='MacPherson', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Marine Parade GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Braddell Heights', grc=grc)
        Division.objects.get_or_create(division_name='Geylang Serai', grc=grc)
        Division.objects.get_or_create(division_name='Joo Chiat', grc=grc)
        Division.objects.get_or_create(division_name='Kembangan-Chai Chee', grc=grc)
        Division.objects.get_or_create(division_name='Marine Parade', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Mountbatten SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Mountbatten', grc=grc)

        # WRO
        user_department, created = UserDepartment.objects.get_or_create(department_name='Western Regional Office')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Bukit Panjang SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Bukit Panjang', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Holland-Bukit Timah GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Bukit Timah', grc=grc)
        Division.objects.get_or_create(division_name='Cashew', grc=grc)
        Division.objects.get_or_create(division_name='Ulu Pandan', grc=grc)
        Division.objects.get_or_create(division_name='Zhenghua', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Marsiling-Yew Tee GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Limbang', grc=grc)
        Division.objects.get_or_create(division_name='Marsiling', grc=grc)
        Division.objects.get_or_create(division_name='Woodgrove', grc=grc)
        Division.objects.get_or_create(division_name='Yew Tee', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Nee Soon GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Chong Pang', grc=grc)
        Division.objects.get_or_create(division_name='Nee Soon Central', grc=grc)
        Division.objects.get_or_create(division_name='Nee Soon East', grc=grc)
        Division.objects.get_or_create(division_name='Nee Soon Link', grc=grc)
        Division.objects.get_or_create(division_name='Nee Soon South', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Sembawang GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Admiralty', grc=grc)
        Division.objects.get_or_create(division_name='Canberra', grc=grc)
        Division.objects.get_or_create(division_name='Sembawang Central', grc=grc)
        Division.objects.get_or_create(division_name='Sembawang West', grc=grc)
        Division.objects.get_or_create(division_name='Woodlands', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Chua Chu Kang GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Brickland', grc=grc)
        Division.objects.get_or_create(division_name='Bukit Gombak', grc=grc)
        Division.objects.get_or_create(division_name='Chua Chu Kang', grc=grc)
        Division.objects.get_or_create(division_name='Keat Hong', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Hong Kah North SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Hong Kah North', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Bukit Batok SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Bukit Batok', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Jurong GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Bukit Batok East', grc=grc)
        Division.objects.get_or_create(division_name='Clementi', grc=grc)
        Division.objects.get_or_create(division_name='Jurong Central', grc=grc)
        Division.objects.get_or_create(division_name='Jurong Spring', grc=grc)
        Division.objects.get_or_create(division_name='Taman Jurong', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Yuhua SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Yuhua', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Pioneer SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Pioneer', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='West Coast GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Ayer Rajah-Gek Poh', grc=grc)
        Division.objects.get_or_create(division_name='Boon Lay', grc=grc)
        Division.objects.get_or_create(division_name='Nanyang', grc=grc)
        Division.objects.get_or_create(division_name='Telok Blangah', grc=grc)
        Division.objects.get_or_create(division_name='West Coast', grc=grc)

        # VCOD
        user_department, created = UserDepartment.objects.get_or_create(department_name='Vector Control Operation Division')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        # SACD
        user_department, created = UserDepartment.objects.get_or_create(department_name='Sanitation and Compliance Division')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        # SEI
        user_department, created = UserDepartment.objects.get_or_create(department_name='Singapore Environment Institute')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)
