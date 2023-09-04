from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Registration(models.Model):
    LEVEL_CHOICES = (
        ('E', 'Employee'),
        ('M', 'Manager'),
        ('B', 'BHR'),
        ('BU','BUHR')
    )
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(unique=True)
    password = models.TextField()
    employee_type = models.CharField(max_length=2,choices=LEVEL_CHOICES,default='E')
    email_id = models.EmailField(unique=True)
    phone = models.CharField(max_length=12, unique=True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.employee_id)

class Resignation (models.Model):
    ROLE_CHOICES = (
        ('FC', 'FTC'),
        ('Pb', 'Probationer'),
        ('L6', 'L6-L5-L4'),
        ('L5', 'L6-L5-L4'),
        ('L4', 'L6-L5-L4'),
        ('L3', 'L3-L2-L1'),
        ('L2', 'L3-L2-L1'),
        ('L1', 'L3-L2-L1'),
    )
    resignation_id = models.AutoField(primary_key=True)
    esep_id = models.CharField(null=True)
    employee_id = models.ForeignKey(Registration, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(null=True)
    last_name = models.CharField(null=True)
    employee_designation = models.CharField(max_length=2,choices=ROLE_CHOICES,default='FC',null=True)
    resignation_date = models.DateField(null=True)
    actual_resignation_date = models.DateField(null=True)
    notice_period_days = models.IntegerField(null=True)
    notice_period_shortfall_days = models.IntegerField(null=True)
    notice_period_recovery = models.PositiveIntegerField(null=True)
    resignation_reason = models.TextField(validators=[MinLengthValidator(300)],null=True)
    manager_approval = models.BooleanField(default=False,null=True)
    manager_reason = models.TextField(validators=[MinLengthValidator(300)],null=True)
    manager_remark = models.TextField(validators=[MinLengthValidator(100)],null=True)
    bhr_approval = models.BooleanField(default=False,null=True)
    bhr_reason = models.TextField(validators=[MinLengthValidator(300)],null=True)
    bhr_remark = models.TextField(validators=[MinLengthValidator(100)],null=True)
    bhur_approval = models.BooleanField(default=False,null=True)
    bhur_reason = models.TextField(validators=[MinLengthValidator(300)],null=True)
    bhur_remark = models.TextField(validators=[MinLengthValidator(100)],null=True)
    lwd_final = models.DateField(null = True)
    deleted = models.BooleanField(default=False,editable=False)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    resignation_current_status = models.BooleanField(default=False,null=True)

    def __str__(self):
        return str(self.resignation_id)
    