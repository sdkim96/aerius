from ...models import User, Staff

class ManagingStaffs:
    def __init__(self):

        self.levels = {'superuser' : 3,
                       'high_staff' : 2,
                       'low_staff' : 1}


    
    def making_staff_by_txt(self):
        with open('/home/azureuser/projects/aerius/myweb/backend/myapp/admin/staffs/who_is_staffs.txt') as f:
            staffs = f.readlines()

            for s in staffs:
                username_password, level = s.split(',')
                this_who, password = username_password.split(':')
                this_level = level.split(':')[1].strip()

                # Try to get the User with the given user id (this_who)
                try:
                    user = User.objects.get(userid=this_who.strip())
                except User.DoesNotExist:
                    print(f"User with id {this_who.strip()} does not exist.")
                    continue  # Skip to the next line

                # Initialize all permissions as False
                is_superuser = False
                is_high_staff = False
                is_low_staff = False

                # Update the corresponding permission according to the level
                if this_level == 'superuser':
                    is_superuser = True
                elif this_level == 'high_staff':
                    is_high_staff = True
                elif this_level == 'low_staff':
                    is_low_staff = True

                try:
                    is_duplicated_staffs = Staff.objects.get(staff_user = user)
                    # 중복된 유저가 있으면 아무런 작업도 수행하지 않고 다음 레코드로 넘어감
                    print(f"User {this_who.strip()} is already a staff member.")
                    continue
                except Staff.DoesNotExist:
                    # 중복된 유저가 없으면 새로운 Staff 인스턴스를 생성
                    staff = Staff(staff_user=user, is_superuser=is_superuser, is_high_staff=is_high_staff, is_low_staff=is_low_staff)
                    staff.save()  # Don't forget to save the instance





                

    
    def making_staff_by_web(self, user):
        pass

            



            
            