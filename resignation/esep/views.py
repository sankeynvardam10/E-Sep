from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Registration, Resignation
from .serializers import RegisterationSerializer, ResignationSerializer
import json
import hashlib
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from datetime import timedelta
from .email_sender import send_email


#This class-view is for Employee registration and to get overall employee data of registered employees
class EmployeeRegisterView(APIView):
    def get(self, request):
        users = Registration.objects.all()
        serializer = RegisterationSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = serializer.save(password=hashed_password)
            return Response(RegisterationSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#This class-view is to get overall employees list, individual employee details, edit employee details and delete employee  
class EmployeeDetailedView(APIView):
    def get_object(self, employee_id):
        try:
            return  Registration.objects.get(pk=employee_id)
        except  Registration.DoesNotExist:
            return None
    def get(self, request, employee_id):
        user = self.get_object(employee_id)
        if user is None:
            return Response({'message': 'Employee not registered'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RegisterationSerializer(user)
        return Response(serializer.data)

    def put(self, request, employee_id):
        user = self.get_object(employee_id)
        if user is None:
            return Response({'message': 'User not registered'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RegisterationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id):
        user = get_object_or_404(Registration,pk=employee_id,deleted=False)
        user.deleted = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


#This class-view is for employee login
class EmployeeLoginView(APIView):
    def post(self, request,pk=None,resignation_status=None):
        request_object=json.loads(request.body)
        user = Registration.objects.filter(employee_id=request_object['employee_id']).first()
        if user is not None:
            # if user_password[0]['password'] == request_object['password']:
            # if check_password(request_object['password'], user.password):
            if user.password == hashlib.sha256(request_object['password'].encode()).hexdigest():

                if user.employee_type == 'E':
                    return Response ({'message':"Employee Login Successfully"}, status=status.HTTP_200_OK)

                elif user.employee_type == 'M':
                    # return Response ({'message':"Manager Login Successfully"}, status=status.HTTP_200_OK)
                    if resignation_status is not None:
                        if resignation_status == 'pending':
                            pending=Resignation.objects.filter(deleted=False,resignation_current_status=False)
                            if pk is not None:
                                pending = pending.filter(pk=pk)
                                if not pending:
                                    return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                            serializer = ResignationSerializer( pending, many=True, context={
                                'exclude_fields': [
                                    'bhr_approval',
                                    'bhr_reason',
                                    'bhr_remark',
                                    'bhur_approval',
                                    'bhur_reason',
                                    'bhur_remark',
                                    'deleted'
                                ]
                            })
                            return Response(serializer.data , status=status.HTTP_200_OK)
                        if resignation_status == 'approved':
                            pending=Resignation.objects.filter(deleted=False,manager_approval=True)
                            if pk is not None:
                                pending = pending.filter(pk=pk)
                                if not pending:
                                    return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                            serializer = ResignationSerializer( pending, many=True, context={
                                'exclude_fields': [
                                    'bhr_approval',
                                    'bhr_reason',
                                    'bhr_remark',
                                    'bhur_approval',
                                    'bhur_reason',
                                    'bhur_remark',
                                    'deleted'
                                ]
                            })
                            return Response(serializer.data , status=status.HTTP_200_OK)
                        if resignation_status == 'reject':
                            pending=Resignation.objects.filter(deleted=False,manager_approval=False)
                            if pk is not None:
                                pending = pending.filter(pk=pk)
                                if not pending:
                                    return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                            serializer = ResignationSerializer( pending, many=True, context={
                                'exclude_fields': [
                                    'bhr_approval',
                                    'bhr_reason',
                                    'bhr_remark',
                                    'bhur_approval',
                                    'bhur_reason',
                                    'bhur_remark',
                                    'deleted'
                                ]
                            })
                            return Response(serializer.data , status=status.HTTP_200_OK)
                    id=pk
                    if id is not None:
                        resign=Resignation.objects.filter(resignation_id=id,deleted=False)
                        if not resign:
                            return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                        serializer = ResignationSerializer( resign, many=True, context={
                            'exclude_fields': [
                                'bhr_approval',
                                'bhr_reason',
                                'bhr_remark',
                                'bhur_approval',
                                'bhur_reason',
                                'bhur_remark',
                                'deleted'
                            ]
                        })
                        return Response(serializer.data)
                    resignations =  Resignation.objects.filter(deleted=False)
                    serializer = ResignationSerializer( resignations, many=True, context={
                        'exclude_fields': [
                            'bhr_approval',
                            'bhr_reason',
                            'bhr_remark',
                            'bhur_approval',
                            'bhur_reason',
                            'bhur_remark',
                            'deleted'
                        ]
                    })
                    return Response(serializer.data , status=status.HTTP_200_OK)

                elif user.employee_type == 'B':
                    # return Response ({'message':"BHR Login Successfully"}, status=status.HTTP_200_OK)
                    if resignation_status is not None:
                        if resignation_status == 'approved':
                            pending=Resignation.objects.filter(manager_approval=True,bhr_approval=True)
                            if pk is not None:
                                pending = pending.filter(pk=pk)
                                if not pending:
                                    return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                            serializer = ResignationSerializer( pending, many=True, context={
                                'exclude_fields': [
                                    'bhur_approval',
                                    'bhur_reason',
                                    'bhur_remark',
                                    'deleted'
                                ]
                            })
                            return Response(serializer.data , status=status.HTTP_200_OK)
                        if resignation_status == 'rejected':
                            pending=Resignation.objects.filter(manager_approval=True,bhr_approval=False)
                            if pk is not None:
                                pending = pending.filter(pk=pk)
                                if not pending:
                                    return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                            serializer = ResignationSerializer( pending, many=True, context={
                                'exclude_fields': [
                                    'bhur_approval',
                                    'bhur_reason',
                                    'bhur_remark',
                                    'deleted'
                                ]
                            })
                    id=pk
                    if id is not None:
                        resign=Resignation.objects.filter(manager_approval=True)
                        serializer = ResignationSerializer( resign, many=True, context={
                            'exclude_fields': [
                                'bhur_approval',
                                'bhur_reason',
                                'bhur_remark',
                                'deleted'
                            ]
                        })
                        # serializer = ResignationSerializer( resign, many=True)
                        return Response(serializer.data)
                    resignations =  Resignation.objects.filter(manager_approval=True)
                    serializer = ResignationSerializer( resignations, many=True, context={
                        'exclude_fields': [
                            'bhur_approval',
                            'bhur_reason',
                            'bhur_remark',
                            'deleted'
                        ]
                    })
                    return Response(serializer.data, status=status.HTTP_200_OK)

                elif user.employee_type == 'BU':
                    # return Response ({'message':"BHUR Login Successfully"}, status=status.HTTP_200_OK)
                    if resignation_status is not None:
                        if resignation_status == 'approved':
                            pending=Resignation.objects.filter(bhr_approval=True,bhur_approval=False)
                            if pk is not None:
                                pending = pending.filter(pk=pk)
                                if not pending:
                                    return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                            serializer = ResignationSerializer( pending, many=True, context={
                                'exclude_fields': [
                                    'deleted'
                                ]
                            })
                            return Response(serializer.data , status=status.HTTP_200_OK)
                        if resignation_status == 'rejected':
                            pending=Resignation.objects.filter(bhr_approval=True,bhur_approval=True)
                            if pk is not None:
                                pending = pending.filter(pk=pk)
                                if not pending:
                                    return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
                            serializer = ResignationSerializer( pending, many=True, context={
                                'exclude_fields': [
                                    'deleted'
                                ]
                            })
                    id=pk
                    if id is not None:
                        resign=Resignation.objects.filter(bhr_approval=True)
                        serializer = ResignationSerializer( resign, many=True, context={
                            'exclude_fields': [
                                'deleted'
                            ]
                        })
                        # serializer = ResignationSerializer( resign, many=True)
                        return Response(serializer.data)
                    resignations =  Resignation.objects.filter(bhr_approval=True)
                    serializer = ResignationSerializer( resignations, many=True, context={
                        'exclude_fields': [
                            'deleted'
                        ]
                    })
                    return Response(serializer.data, status=status.HTTP_200_OK)
                # return Response({'message': "Login Successfull"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


#This class-view provides the user with multiple fields required for resignation and can even view the form
class EmployeeResignationView(APIView):
    def get(self, request):
        resign =  Resignation.objects.all()
        serializer = ResignationSerializer( resign, many=True)
        return Response(serializer.data)

    def post(self, request):
        request_data = request.data
        employee_id = request_data['employee_id']
        count = Resignation.objects.filter(employee_id=employee_id).count()
        request_data['esep_id'] = 'ESP' + str(count).rjust(4, '0')

        serializer = ResignationSerializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        request_object=request.data
        resignation_date_str = request_object['resignation_date']
        actual_resignation_date_str = request_object['actual_resignation_date']
        notice_period_days = request_object['notice_period_days']
        # notice_period_shortfall_days = request_object['notice_period_shortfall_days']
        # notice_period_recovery = request_object['notice_period_recovery']
        employee_id = request_object['employee_id']
        designation = request_object['employee_designation']
        current_date = datetime.now().date()
        notice_period_days = request_object['notice_period_days']
        # notice_period_shortfall_days = request_object['notice_period_shortfall_days']

        resignation_date = datetime.strptime(resignation_date_str, '%Y-%m-%d').date()
        actual_resignation_date = datetime.strptime(actual_resignation_date_str, '%Y-%m-%d').date()
        # lwd_final = datetime.strptime(lwd_final_str, '%Y-%m-%d').date()
        first_name, last_name = Registration.objects.filter(employee_id=employee_id).values_list('first_name', 'last_name').first()

        receiver_email = 'nsvardam@gmail.com'
        subject = 'Resignation Application'
        
        if resignation_date < current_date:
            return Response({"error": "Resignation date is not validate"}, status=status.HTTP_400_BAD_REQUEST)

        if resignation_date < actual_resignation_date:
            return Response({"error": "Resignation date cannot be after actual resignation date"}, status=status.HTTP_400_BAD_REQUEST)

        if designation == 'FC' or designation == 'Pb':
            if actual_resignation_date > current_date + timedelta(days=25):
                return Response({"error": "Actual resignation date must be less than 25 days from now"}, status=status.HTTP_400_BAD_REQUEST)
            resignation=serializer.save()
            lwd = actual_resignation_date + timedelta(days=30)
            if notice_period_days > 30:
                return Response({"error": "Notice period should be less than 30 days"}, status=status.HTTP_400_BAD_REQUEST)
            shortfall_days = 30 - notice_period_days
            notice_period = (shortfall_days / 30.0) * 20000
            if notice_period < 20000: 
                message = f'This is an email notification for a resignation application from employee id : {employee_id}, {first_name} {last_name} who is willing to work for {notice_period_days} days as notice period leading to {shortfall_days} days of shortfall.'
                send_email(receiver_email, subject, message)
                Resignation.objects.filter(resignation_id=resignation.resignation_id).update(notice_period_recovery=notice_period,notice_period_shortfall_days= shortfall_days)
                return Response(
                    {
                        "message": "Resignation Applied Successfully",
                        "Indicative notice period recovery": notice_period
                    },
                    status=status.HTTP_201_CREATED
                    )

        if designation == 'L6' or designation == 'L5' or designation == 'L4':
            if actual_resignation_date > current_date + timedelta(days=55):
                return Response({"error": "Actual resignation date must be less than 55 days from actual_resignation_date"}, status=status.HTTP_400_BAD_REQUEST)
            resignation=serializer.save()
            lwd = actual_resignation_date + timedelta(days=60)
            if notice_period_days > 60:
                return Response({"error": "Notice period should be less than 60 days"}, status=status.HTTP_400_BAD_REQUEST)
            shortfall_days = 60 - notice_period_days
            notice_period = (shortfall_days / 30.0) * 40000
            if notice_period < 40000:
                message = f'This is an email notification for a resignation application from employee id : {employee_id}, {first_name} {last_name} who is willing to work for {notice_period_days} days as notice period leading to {shortfall_days} days of shortfall.'
                send_email(receiver_email, subject, message)
                Resignation.objects.filter(resignation_id=resignation.resignation_id).update(notice_period_recovery=notice_period,notice_period_shortfall_days= shortfall_days)
                return Response(
                    {
                        "message": "Resignation Applied Successfully",
                        "Indicative notice period recovery": notice_period
                    },
                    status=status.HTTP_201_CREATED
                    )
        
        if designation == 'L3' or designation == 'L2' or designation == 'L1':
            if actual_resignation_date > current_date + timedelta(days=75):
                return Response({"error": "Actual resignation date should be less than 75 days from actual_resignation_date"}, status=status.HTTP_400_BAD_REQUEST)
            resignation=serializer.save()
            lwd = actual_resignation_date + timedelta(days=90)
            if notice_period_days > 90:
                return Response({"error": "Notice period should be less than 90 days"}, status=status.HTTP_400_BAD_REQUEST)
            shortfall_days = 90 - notice_period_days
            notice_period = (shortfall_days / 30.0) * 60000
            if notice_period < 60000:
                message = f'This is an email notification for a resignation application from employee id : {employee_id}, {first_name} {last_name} who is willing to work for {notice_period_days} days as notice period leading to {shortfall_days} days of shortfall.'
                send_email(receiver_email, subject, message)
                Resignation.objects.filter(resignation_id=resignation.resignation_id).update(notice_period_recovery=notice_period,notice_period_shortfall_days= shortfall_days)
                return Response(
                    {
                        "message": "Resignation Applied Successfully",
                        "Indicative notice period recovery": notice_period
                    },
                    status=status.HTTP_201_CREATED
                    )
 
#This class-view provides the detailed view of the resignation application applied by the user
class ResignationDetailedView(APIView):
    def get_object(self, resignation_id):
        try:
            return  Resignation.objects.get(pk=resignation_id)
        except  Resignation.DoesNotExist:
            return None

    def get(self, request, resignation_id):
        resign = self.get_object(resignation_id)
        if resign is None:
            return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
        serializer =  ResignationSerializer(resign)
        return Response(serializer.data)
    # def get(self, request, resignation_id):
    #     resign = get_object_or_404(Resignation, pk=resignation_id,deleted=False)
    #     employee_data = resign.resignation_id 

    #     employee_serializer = RegisterationSerializer(employee_data)

    #     employee={ 
    #         'employee_designation': employee_serializer.data['employee_designation'],
    #         'resignation_date': ResignationSerializer.data['resignation_date'],
    #         'actual_resignation_date': ResignationSerializer.data["actual_resignation_date"],
    #         'notice_period_days': ResignationSerializer(resign).data["notice_period_days"],
    #         'notice_period_shortfall_days': ResignationSerializer(resign).data["notice_period_shortfall_days"],
    #         'notice_period_recovery': ResignationSerializer(resign).data["notice_period_recovery"],
    #         'resignation_reason': ResignationSerializer(resign).data["resignation_reason"],
    #         'lwd_final': ResignationSerializer(resign).data["lwd_final"],
    #     }
    #     return Response(employee)
    def put(self, request, resignation_id):
        request_object=json.loads(request.body)
        resign = self.get_object(resignation_id)
        request_header = request.headers['User-Agent']
        if resign is None:
            return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)

        elif request_header == 'E':
            serializer = ResignationSerializer(resign,data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            request_object=request.data
            resignation_date_str = request_object['resignation_date']
            actual_resignation_date_str = request_object['actual_resignation_date']
            notice_period_days = request_object['notice_period_days']
            designation = request_object['employee_designation']
            current_date = datetime.now().date()
            notice_period_days = request_object['notice_period_days']
            employee_id = request_object['employee_id']

            resignation_date = datetime.strptime(resignation_date_str, '%Y-%m-%d').date()
            actual_resignation_date = datetime.strptime(actual_resignation_date_str, '%Y-%m-%d').date()

            receiver_email = 'nsvardam@gmail.com'
            subject = 'Resignation Application'


            if resignation_date < current_date:
                return Response({"error": "Resignation date is not validate"}, status=status.HTTP_400_BAD_REQUEST)

            if resignation_date < actual_resignation_date:
                return Response({"error": "Resignation date cannot be after actual resignation date"}, status=status.HTTP_400_BAD_REQUEST)

            if designation == 'FC' or designation == 'Pb':
                if actual_resignation_date > current_date + timedelta(days=25):
                    return Response({"error": "Actual resignation date must be less than 25 days from now"}, status=status.HTTP_400_BAD_REQUEST)
                lwd = actual_resignation_date + timedelta(days=30)
                shortfall_days = 30 - notice_period_days
                notice_period = (shortfall_days / 30.0) * 20000
                if notice_period < 20000:
                    Resignation.objects.filter(resignation_id=resignation_id).update(notice_period_recovery=notice_period,notice_period_shortfall_days= shortfall_days)
                    message = f'This is an email notification for a resignation application from employee id : {employee_id}, who is willing to work for {notice_period_days} days as notice period leading to {shortfall_days} days of shortfall.'
                    send_email(receiver_email, subject, message)
                    return Response(
                        {
                            "message": "Resignation Applied Successfully",
                            "Indicative notice period recovery": notice_period
                        },
                        status=status.HTTP_201_CREATED
                        )

            if designation == 'L6' or designation == 'L5' or designation == 'L4':
                if actual_resignation_date > current_date + timedelta(days=55):
                    return Response({"error": "Actual resignation date must be less than 55 days from actual_resignation_date"}, status=status.HTTP_400_BAD_REQUEST)
                lwd = actual_resignation_date + timedelta(days=60)
                shortfall_days = 60 - notice_period_days
                notice_period = (shortfall_days / 30.0) * 40000
                if notice_period < 40000:
                    message = f'This is an email notification for a resignation application from employee id : {employee_id}, who is willing to work for {notice_period_days} days as notice period leading to {shortfall_days} days of shortfall.'
                    send_email(receiver_email, subject, message)
                    Resignation.objects.filter(resignation_id=resignation_id).update(notice_period_recovery=notice_period,notice_period_shortfall_days= shortfall_days)
                    serializer.save()
                    return Response(
                    {
                        "message": "Resignation Applied Successfully",
                        "Indicative notice period recovery": notice_period
                    },
                    status=status.HTTP_201_CREATED
                    )
            
            if designation == 'L3' or designation == 'L2' or designation == 'L1':
                if actual_resignation_date > current_date + timedelta(days=75):
                    return Response({"error": "Actual resignation date should be less than 75 days from actual_resignation_date"}, status=status.HTTP_400_BAD_REQUEST)
                lwd = actual_resignation_date + timedelta(days=90)
                shortfall_days = 90 - notice_period_days
                notice_period = (shortfall_days / 30.0) * 60000
                if notice_period <= 180000 :
                    message = f'This is an email notification for a resignation application from employee id : {employee_id}, who is willing to work for {notice_period_days} days as notice period leading to {shortfall_days} days of shortfall.'
                    send_email(receiver_email, subject, message)
                    Resignation.objects.filter(resignation_id=resignation_id).update(notice_period_recovery=notice_period,notice_period_shortfall_days= shortfall_days)
                    serializer.save()
                    return Response(
                    {
                        "message": "Resignation Applied Successfully",
                        "Indicative notice period recovery": notice_period
                    },
                    status=status.HTTP_201_CREATED
                    )
    
        elif request_header == 'M':
            if resign.deleted==True:
                return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResignationSerializer(resign, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            request_object=request.data
            manager_approval = request_object['manager_approval']
            manager_reason = request_object['manager_reason']
            manager_remark = request_object['manager_remark']
            lwd_final_str = request_object['lwd_final']
            resignation_current_status = request_object['resignation_current_status']
            lwd_final = datetime.strptime(lwd_final_str, '%Y-%m-%d').date()

            receiver_email = 'nihar.vardam_19@sakec.ac.in'
            subject = 'Manager Approval'
            message_approved= 'Your resignation application has been approved by the manager.'
            message_rejected= 'Sorry, your resignation application has been rejected by the manager.'
            
            if resignation_current_status == True:
                if  lwd_final < resign.actual_resignation_date :
                    return Response({'message':'LWD should be more than actual_resignation_date'}, status=status.HTTP_400_BAD_REQUEST)
                if manager_approval == True:
                    if manager_reason == None:
                        return Response({'message':'Please provide a suitable reason'}, status=status.HTTP_400_BAD_REQUEST)
                    serializer.save()
                    send_email(receiver_email, subject, message_approved)
                    return Response({'message':'Manger Response Submitted'}, status=status.HTTP_201_CREATED)
                elif manager_approval == False:
                    if manager_remark == None:
                        return Response({'message':'Please provide a suitable remark'}, status=status.HTTP_400_BAD_REQUEST)
                    serializer.save()
                    send_email(receiver_email, subject, message_rejected)
                    return Response({'message':'Manger Response Submitted'}, status=status.HTTP_201_CREATED)
                    # return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message':'Please update the status'})

        elif request_header == 'B':
            if resign.manager_approval==False:
                return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResignationSerializer(resign, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            request_object=request.data
            bhr_approval = request_object['bhr_approval']
            bhr_reason = request_object['bhr_reason']
            bhr_remark = request_object['bhr_remark']
            lwd_final_str = request_object['lwd_final']
            lwd_final = datetime.strptime(lwd_final_str, '%Y-%m-%d').date()

            receiver_email = 'nihar.vardam_19@sakec.ac.in'
            subject = 'BHR Approval'
            message_approved= 'Your resignation application has been approved by the BHR.'
            message_rejected= 'Sorry, your resignation application has been rejected by the BHR.'

            if  lwd_final < resign.actual_resignation_date :
                    return Response({'message':'LWD should be more than actual_resignation_date'}, status=status.HTTP_400_BAD_REQUEST)
            if bhr_approval == True:
                if bhr_reason == None:
                    return Response({'message':'Please provide a suitable reason'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                send_email(receiver_email, subject, message_approved)
                return Response({'message':'BHR Response Submitted'}, status=status.HTTP_201_CREATED)
            elif bhr_approval == False:
                if bhr_remark == None:
                    return Response({'message':'Please provide a suitable remark'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                send_email(receiver_email, subject, message_rejected)
                return Response({'message':'BHR Response Submitted'}, status=status.HTTP_201_CREATED)
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request_header == 'BU':
            if resign.bhr_approval==False:
                return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResignationSerializer(resign, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            request_object=request.data
            bhur_approval = request_object['bhur_approval']
            bhur_reason = request_object['bhur_reason']
            bhur_remark = request_object['bhur_remark']
            lwd_final_str = request_object['lwd_final']
            lwd_final = datetime.strptime(lwd_final_str, '%Y-%m-%d').date()

            receiver_email = 'nihar.vardam_19@sakec.ac.in'
            subject = 'BHUR Approval'
            message_approved= 'Your resignation application has been approved by the BHUR.'
            message_rejected= 'Sorry, your resignation application has been rejected by the BHUR.'

            if  lwd_final < resign.actual_resignation_date :
                    return Response({'message':'LWD should be more than actual_resignation_date'}, status=status.HTTP_400_BAD_REQUEST)
            if bhur_approval == True:
                if bhur_reason == None:
                    return Response({'message':'Please provide a suitable reason'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                send_email(receiver_email, subject, message_approved)
                return Response({'message':'Manger Response Submitted'}, status=status.HTTP_201_CREATED)
            elif bhur_approval == False:
                if bhur_remark == None:
                    return Response({'message':'Please provide a suitable remark'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                send_email(receiver_email, subject, message_rejected)
                return Response({'message':'BUHR Response Submitted'}, status=status.HTTP_201_CREATED)
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Please enter valid employement level'},status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, resignation_id):
        # resign = get_object_or_404(Resignation,pk=resignation_id,deleted=False,manager_approval=null)
        request_header = request.headers['User-Agent']
        # resign = get_object_or_404(Resignation,pk=resignation_id,deleted=False,resignation_current_status=False)
        resign = self.get_object(resignation_id)
        if resign is None or resign.deleted == True:
            return Response({'message': 'No resignation found'}, status=status.HTTP_404_NOT_FOUND)
        if resign.resignation_current_status == True :
            return Response({'message': 'Apllication cannot be deleted'}, status=status.HTTP_404_NOT_FOUND)
        if request_header == 'E':
            resign.deleted = True
            resign.save()
            return Response({'message': 'Application deleted'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Not accessible'}, status=status.HTTP_400_BAD_REQUEST)
    

    
 