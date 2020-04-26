from django import forms
from admin_panel.models import Batch,Login,Student,Subject,Teacher_subject
from django.core.validators import RegexValidator
import datetime

course_validator = RegexValidator(r"^MBA|^MCA", "Course should be mba or mca")
password_validator = RegexValidator(r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%!*^])).{6,20}", "Must Contains one digit from 0-9,Must contain one lowercase characters, Must contain one uppercase character,must contain a special symbol,should have a minimum of 8 characters and should not exceed maximum of 20 characters")  
username_validator = RegexValidator(r"^[a-z0-9_-]{3,15}$", "Should not contain white space.must be at least 3 characters")  
admission_no_validator = RegexValidator(r"[^a-zA-Z]{7,}", "Admission No. should be atleast 7 numbers") 
phone_no_validator = RegexValidator(r"[^a-zA-Z]{7,}", "Phone No. should be atleast 10 numbers")  

class LoginForm(forms.Form):
    name =  forms.CharField(help_text="User Name",widget=forms.TextInput(
        attrs={'placeholder':"Username",'class':"form-control"}
    ),max_length=100,required=True,)
    pwd =   forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':"Password",'class':"form-control"}
    ),max_length=32,required=True,)


class CreateBatchForm(forms.Form):
    course = forms.ChoiceField(
        choices=(
            (None,"Select Course"),
            ("MCA","MCA"),
            ("MBA","MBA")
        ),
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        required=True,
        validators=[
            course_validator
        ]
    )
    year = forms.ChoiceField(
        choices=(
            (None,"Select Year"),
            ("2017","2017"),
            ("2018","2018"),
            ("2019","2019"),
            ("2020","2020"),
            ("2021","2021"),
            ("2022","2022"),
            ("2023","2023"),
            ("2024","2024"),
            ("2025","2025"),
        ),
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        required=True
    )
    def clean(self):
        course = self.cleaned_data['course']
        year = self.cleaned_data['year']
        batch = course+year
        isBatchExist = Batch.objects.filter(name=batch)
        if isBatchExist is not None and len(isBatchExist) > 0:
            raise forms.ValidationError(u'Batch "%s" is already added.' % batch)
        return self.cleaned_data

class CreateStudentForm(forms.Form):
    admission_no = forms.CharField(help_text="Admission No.",widget=forms.TextInput(
        attrs={'placeholder':"Admisssion No.",'class':"form-control"}
    ),max_length=100,required=True,validators=[
        admission_no_validator
    ])

    name = forms.CharField(
        help_text="Name",widget=forms.TextInput(
            attrs={'placeholder':"Name",'class':"form-control"}
        ),required=True
    )

    batch_id = forms.ModelChoiceField(queryset=Batch.objects.all(),empty_label="Select Batch",required=True,widget=forms.Select(attrs={'class':'form-control'}))
    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'class':'form-control',
                'id':'datepicker',
                'placeholder':"Dob (DD/MM/YYYY)"
            }
        )
    )

    parent_name = forms.CharField(
        help_text="Parent Name",widget=forms.TextInput(
            attrs={'placeholder':"Parent Name",'class':"form-control"}
        ),required=True
    )

    parent_no = forms.CharField(
        help_text="Parent Number",widget=forms.TextInput(
            attrs={'placeholder':"Parent No.",'class':"form-control"}
        ),required=True,
        validators=[
            phone_no_validator
        ]
    )

    def clean_admission_no(self):
        admission_no = self.cleaned_data['admission_no']
        try:
            user = Student.objects.get(admission_no=admission_no)
        except Student.DoesNotExist:
            return admission_no
        raise forms.ValidationError(u'Student admission no "%s" is already in use.' % admission_no)

class CreateTeacherForm(forms.Form):
    name = forms.CharField(help_text="Name",widget=forms.TextInput(
        attrs={'placeholder':"Name",'class':"form-control"}
    ),max_length=100,required=True)
    username = forms.CharField(help_text="Username",widget=forms.TextInput(
        attrs={'placeholder':"Username",'class':"form-control"}
    ),max_length=100,required=True,validators=[
        username_validator
    ])
    password = forms.CharField(help_text="Password",widget=forms.PasswordInput(
        attrs={'placeholder':"Password",'class':"form-control"}
    ),max_length=100,required=True,
    validators=[
        password_validator
    ])
    cpassword = forms.CharField(help_text="Confirm Password",widget=forms.PasswordInput(
        attrs={'placeholder':"Confirm Password",'class':"form-control"}
    ),max_length=100,required=True)

    def clean(self):
        password = self.cleaned_data.get('password', None)
        cpassword = self.cleaned_data.get('cpassword', None)
        if password and cpassword and (password == cpassword):
            return self.cleaned_data
        raise forms.ValidationError("Passwords are not identical.")    

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Login.objects.get(username=username)
        except Login.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)

class CreateSubjectForm(forms.Form):
    semester = forms.ChoiceField(
        choices=(
            (None,"Select Semester"),
            ("s1","S1"),
            ("s2","S2"),
            ("s3","S3"),
            ("s4","S4"),
            ("s5","S5"),
            ("s6","S6"),
        ),
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        required=True
    )
    subject = forms.CharField(help_text="Subject",widget=forms.TextInput(
        attrs={'placeholder':"Subject",'class':"form-control"}
    ),required=True)

    def clean(self):
        subject = self.cleaned_data['subject']
        semester = self.cleaned_data['semester']
        try:
            sub = Subject.objects.get(name=subject,sem=semester)
        except Subject.DoesNotExist:
            return self.cleaned_data
        raise forms.ValidationError(u'Subject "%s" is already added.' % subject)

class ManageStudentForm(forms.Form):
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),empty_label="Select Batch",required=True,widget=forms.Select(attrs={'class':'form-control'}))


class UploadDatasetForm(forms.Form):
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),empty_label="Select Batch",required=True,widget=forms.Select(attrs={'class':'form-control','id':'batch'}))
    student = forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Select Student",required=True,widget=forms.Select(attrs={'class':'form-control','id':'students'}))

class SnapForm(forms.Form):
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),empty_label="Select Batch",required=True,widget=forms.Select(attrs={'class':'form-control','id':'batch'}))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(),empty_label="Select Subject",required=True,widget=forms.Select(attrs={'class':'form-control','id':'subject'}))

class DialyReportForm(forms.Form):
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),empty_label="Select Batch",required=True,widget=forms.Select(attrs={'class':'form-control','id':'batch'}))
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'class':'form-control',
                'id':'atdate',
                'placeholder':"Attendence Date (DD/MM/YYYY)"
            }
        )
    )

class MonthlyReportForm(forms.Form):
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),empty_label="Select Batch",required=True,widget=forms.Select(attrs={'class':'form-control','id':'batch'}))
    month = forms.ChoiceField(
        choices=((key, str(val)) for key,val in [
            ('1','January'),
            ('2','February'),
            ('3','March'),
            ('4','April'),
            ('5','May'),
            ('6','June'),
            ('7','July'),
            ('8','August'),
            ('9','September'),
            ('10','October'),
            ('11','November'),
            ('12','December')
        ]),
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        required=True
    )
    year = forms.ChoiceField(
        choices=((o, str(o)) for o in range(2015,datetime.datetime.now().year+1)),
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        required=True
    )
