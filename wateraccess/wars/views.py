from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
import json
from django.utils.timezone import localtime, now
from datetime import timedelta, datetime
from django.contrib.auth.hashers import check_password,make_password
import random
import string
import logging
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Case, Province, District, Sector, Cell, Tap, Village,warsUser, Location, Password, userProfile
from .forms import ContactMessageForm, ProvinceForm, DistrictForm, SectorForm, CellForm, VillageForm,CaseForm

# Create your views here.

# Views to display static files

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')
def registration_success(request):
    return render(request, 'registration_success.html')# Login user
def register(request):
    return render(request, 'register.html')
def password_reset(request):
    return render(request, 'password_reset.html')
def password_update(request):
    return render(request, 'password_update.html')
def password_reset_confirm(request):
    return render(request, 'password_reset_confirm.html')
def register_otp_verification(request):
    return render(request, 'reg_otp_verification.html')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
def sedo_cell_dashboard(request):
    return render(request, 'sedo_cell_dashboard.html')
def technician_dashboard(request):
    return render(request, 'technician_dashboard.html')
def responsible_dashboard(request):
    return render(request, 'responsible_dashboard.html')
def wasac_dashboard(request):
    return render(request, 'wasac_dashboard.html')

def user_dashboard(request):
    return render(request, 'customer_dashboard.html')

# Wasac (Admin) system dashboard views

def profi_view(request):
    # Assuming request.user is linked to warsUser
    wars_user = get_object_or_404(warsUser, email=request.user.email)
    profile = get_object_or_404(userProfile, user=wars_user)
    return render(request, 'admin_views/profile.html', {'profile': profile})

def manage_users_view(request):
    return render(request, 'admin_views/manage_users.html')

def case_categories_view(request):
    return render(request, 'admin_views/case_categories.html')

def reported_cases_view(request):
    return render(request, 'admin_views/reported_cases.html')

def branch_overview_view(request):
    return render(request, 'admin_views/branch_overview.html')

def reports_view(request):
    return render(request, 'admin_views/reports.html')

def notifications_view(request):
    return render(request, 'admin_views/notifications.html')

def help_desk_view(request):
    return render(request, 'admin_views/helpdesk.html')

def logout_view(request):
    # Add logout logic here (e.g., Django's `logout()` function)
    return render(request, 'admin_views/logout.html')


# Branch system dashboard views

@login_required
def branch_dashboard(request):
    # Example data to render charts
    analytics_data = {
        "taps": {"working": 120, "not_working": 30, "total": 150},
        "users": {"active": 2000, "inactive": 500, "total": 2500},
        "technicians": {"available": 20, "busy": 10, "total": 30},
        "cases": {"resolved": 100, "pending": 25, "in_progress": 15, "total": 140},
    }
    analytics_data_json = json.dumps(analytics_data)
    return render(request, 'branch/branch_dashboard.html', {'analytics_data': analytics_data_json})

# API for asynchronous chart data (optional)
def analytics_data_api(request):
    data = {
        "taps": {"working": 120, "not_working": 30, "total": 150},
        "users": {"active": 2000, "inactive": 500, "total": 2500},
        "technicians": {"available": 20, "busy": 10, "total": 30},
        "cases": {"resolved": 100, "pending": 25, "in_progress": 15, "total": 140},
    }
    return JsonResponse(data)

@login_required
def branch_management(request):
    return render(request, 'branch/branch_management.html')

@login_required
def tap_monitoring(request):
    taps=Tap.objects.all()  # Fetch all taps from the database
    return render(request, 'branch/tap_monitoring.html', {'taps': taps})

def add_tap(request):
    if request.method == 'POST':
        try:
            customer_name = request.POST.get('customer_name')
            location = request.POST.get('location')
            new_tap = Tap(customer_name=customer_name, location=location)
            new_tap.save()
            return JsonResponse({"success": True, "message": "Tap added successfully.", "tap_id": new_tap.id,'redirect_url': 'wasac_dashboard'})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

    return redirect('wasac_dashboard')  # Redirect back if not a POST request
@login_required
def edit_tap(request, tap_id):
    try:
        tap = Tap.objects.get(id=tap_id)  # Fetch the tap by ID
    except Tap.DoesNotExist:
        return redirect('wasac_dashboard')  # Redirect if tap is not found

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        location = request.POST.get('location', '').strip()

        if customer_name and location:
            tap.customer_name = customer_name
            tap.location = location
            tap.save()
            return redirect('wasac_dashboard')  # Redirect on success
        else:
            # Handle missing fields (optional)
            error_message = "Customer Name and Location are required."
            return render(request, 'edit_tap.html', {'tap': tap, 'error': error_message})

    return render(request, 'edit_tap.html', {'tap': tap})


@login_required
def delete_tap(request, tap_id):
    try:
        tap = Tap.objects.get(id=tap_id)  # Fetch the tap by its ID
        tap.delete()  # Delete the tap
    except Tap.DoesNotExist:
        # Handle the case where the tap doesn't exist (optional)
        pass

    return redirect('wasac_dashboard')  # Redirect after deletion

@login_required
def case_assignment(request):
    technicians = userProfile.objects.filter(role='Technician')
    cases = Case.objects.all()  # noqa: F821
    return render(request, 'case_assignment.html', {'technicians': technicians, 'cases': cases})
# View for Assigning Cases
@login_required
def assign_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    responsible_users = userProfile.objects.filter(role__in=['Technician', 'Responsible'])

    if request.method == 'POST':
        responsible_user_id = request.POST.get('responsible_user')
        responsible_user = get_object_or_404(userProfile, id=responsible_user_id)
        case.responsible_user = responsible_user
        case.save()

        messages.success(request, f'Case assigned to {responsible_user.full_name}.')
        return redirect('case_list')

    return render(request, 'branch/case_assignment.html', {'case': case, 'responsible_users': responsible_users})

# View for listing all cases based on user roles
@login_required
def case_list(request):
    user_profile = userProfile.objects.get(user=request.user)
    
    # If the user is a 'Manager' or 'Responsible', they can see all cases
    if user_profile.role in ['Manager', 'Responsible']:
        cases = Case.objects.all()
    else:
        # If the user is a 'Customer' or 'Technician', they can see their own cases
        cases = Case.objects.filter(created_by=request.user)

    return render(request, 'case_list.html', {'cases': cases})

# Assign case to a technician, only accessible by users with 'Manager' or 'Responsible' role
@login_required
def assign_case(request, case_id=None):
    user_profile = userProfile.objects.get(user=request.user)

    # Only users with Manager or Responsible roles can assign cases
    if user_profile.role not in ['Manager', 'Responsible']:
        return redirect('case_list')  # Redirect back to the case list if unauthorized

    if case_id:
        case = get_object_or_404(Case, id=case_id)
    else:
        case = None
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.instance.created_by = request.user  # Assign the logged-in user as the creator
            form.save()
            return redirect('case_list')
    else:
        form = CaseForm(instance=case)
    return render(request, 'assign_case.html', {'form': form})

# Reassign a case (remove current technician), available for 'Manager' or 'Responsible'
@login_required
def reassign_case(request, case_id):
    user_profile = userProfile.objects.get(user=request.user)
    
    if user_profile.role not in ['Manager', 'Responsible']:
        return redirect('case_list')  # Redirect if not authorized
    
    case = get_object_or_404(Case, id=case_id)
    case.assigned_technician = None
    case.save()
    return redirect('assign_case', case_id=case.id)

# View for user profile, showing information based on roles
@login_required
def user_profile_view(request):
    user = request.user
    location = Location.objects.get(user=user)
    profile = user.profile  # from userProfile model
    
    # Render different profile information based on role
    if profile.role == 'Technician':
        cases = Case.objects.filter(assigned_technician__user=user)
        return render(request, 'technician_profile.html', {'user': user, 'location': location, 'profile': profile, 'cases': cases})
    
    return render(request, 'user_profile.html', {'user': user, 'location': location, 'profile': profile})

# View for Updating Case Status
def update_case_status(request, case_id):
    case = get_object_or_404(Case, id=case_id)

    # Check if the user is the assigned responsible user or a manager
    if case.responsible_user != request.user.profile and request.user.profile.role != 'Manager':
        messages.error(request, "You don't have permission to update this case.")
        return redirect('case_list')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Case.STATUS_CHOICES):
            case.status = new_status
            case.save()

            # Notify the case owner via email
            send_mail(  # noqa: F821
                'Case Status Updated',
                f'The status of your case "{case.title}" has been updated to "{new_status}".',
                settings.DEFAULT_FROM_EMAIL,
                [case.user.email],
                fail_silently=False,
            )

            messages.success(request, f'Status updated to {new_status}.')
            return redirect('case_list')
        else:
            messages.error(request, 'Invalid status selected.')

    return render(request, 'branch/update_case_status.html', {'case': case})


@login_required
def performance_reports(request):
    return render(request, 'branch/performance_reports.html')

# View for the Responsible Dashboard main page
def dashboard(request):
    return render(request, 'responsible/dashboard.html')

def assign_technicians(request):
    # Fetch all technicians
    technicians = userProfile.objects.filter(role='Technician')  # Get all users with the 'Technician' role

    return render(request, 'responsible/assign_technicians.html', {'technicians': technicians})

# View for case management
def case_management(request):
    cases = Case.objects.all()  # noqa: F821
    return render(request, 'responsible/case_management.html', {'cases': cases})

# View for escalating cases
def escalate_case(request, case_id):
    case = Case.objects.get(id=case_id)  # noqa: F821
    # Logic for escalating the case
    case.status = 'Escalated'
    case.save()
    return JsonResponse({'status': 'success', 'message': f'Case {case_id} has been escalated.'})

# View for generating reports
def generate_reports(request):
    reports = Report.objects.all()  # noqa: F821
    return render(request, 'responsible/generate_reports.html', {'reports': reports})



def profil_view(request):  # noqa: F811
    return render(request, 'wasac/profile.html')

def taps_owners_view(request):
    return render(request, 'wasac/taps_owners.html')

def admin_messages_view(request):
    return render(request, 'wasac/admin_messages.html')

def sedo_messages_view(request):
    return render(request, 'wasac/sedo_messages.html')

def dashboard(request):  # noqa: F811
    # Your dashboard logic
    return render(request, 'wasac/dashboard.html')

def user_management(request):
    # Your user management logic
    return render(request, 'wasac/user_management.html')

def case_categories(request):
    # Your case categories logic
    return render(request, 'wasac/case_categories.html')

def report_generation(request):
    # Your report generation logic
    return render(request, 'wasac/report_generation.html')


# views.py for customer dashboard

def load_customer_dashboard(request):
    return render(request, 'customer/dashboard.html')

@login_required
def profile_view(request):
    customer = warsUser.objects.filter(email=request.user.email).first()
    if not customer:
        return JsonResponse({'error': 'Customer profile not found'}, status=404)

    location = Location.objects.filter(user=customer).first()
    profile = userProfile.objects.filter(user=customer).first()

    if request.method == "POST":
        customer.names = request.POST.get('names', customer.names)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.nationalId = request.POST.get('nationalId', customer.nationalId)
        customer.save()
        
        if location:
            location.province = request.POST.get('province', location.province)
            location.district = request.POST.get('district', location.district)
            location.save()
        
        if profile:
            profile.role = request.POST.get('role', profile.role)
            profile.save()

        return JsonResponse({'message': 'Profile updated successfully.'})

    return render(request, 'customer/profile.html', {
        'customer': customer,
        'location': location,
        'profile': profile
    })
@login_required
def cases_view(request):
    if request.method == "POST":
        case_title = request.POST.get('title')
        case_description = request.POST.get('description')
        return JsonResponse({'message': 'Case reported successfully.'})
    return render(request, 'customer/cases.html')

@login_required
def notifications_view(request):
    notifications = [
        {'title': 'Notification 1', 'description': 'Details of notification 1'},
        {'title': 'Notification 2', 'description': 'Details of notification 2'}
    ]
    return render(request, 'customer/notifications.html', {'notifications': notifications})

@login_required
def service_requests_view(request):
    if request.method == "POST":
        service_type = request.POST.get('service_type')
        service_description = request.POST.get('description')
        return JsonResponse({'message': 'Service request submitted successfully.'})
    return render(request, 'customer/service_requests.html')

@login_required
def helpdesk_view(request):
    if request.method == "POST":
        issue = request.POST.get('issue')
        details = request.POST.get('details')
        return JsonResponse({'message': 'Help desk request submitted successfully.'})
    return render(request, 'customer/helpdesk.html')



# User system dashboard

def profile_view(request):
    #user = request.warsUser  # Assuming user is logged in
    try:
        warsUser = warsUser.objects.get(user=user)  # Fetch related profile if exists
    except userProfile.DoesNotExist:
        profile = None  # Handle case where no profile exists
    return render(request, 'customer/profile.html', {'user': user, 'profile': profile})

def service_request_view(request):
    return render(request, 'customer/providers.html')

def reports_view(request):  
    return render(request, 'customer/reports.html')

def case_view(request):
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.save()

            # Send email notification
            EmailMultiAlternatives(  # noqa: F821
                'Case Submitted Successfully',
                f'Thank you for submitting your case: {case.title}. Our team will review it soon.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )

            messages.success(request, 'Case submitted successfully. A confirmation email has been sent to you.')
            return redirect('cases_view')
        else:
            messages.error(request, 'There was an error submitting your case. Please try again.')
    else:
        form = CaseForm()

    # Display recent cases
    #recent_cases = Case.objects.filter(user=request.user).order_by('-created_at')
    #return render(request, 'customer/cases.html')
def helpdesk_view(request):
    return render(request, 'customer/helpdesk.html')
def notifications_view(request):  # noqa: F811
    return render(request, 'customer/notifications.html')
def logout(request):
    return render(request, 'customer/logout.html')

# Admin system dashboard

# Define views for each nav link
def admin_profile_view(request):
    return render(request, 'admin_dashboard/profile.html')

def admin_manage_users_view(request):
    users = warsUser.objects.all()
    return render(request, 'admin_dashboard/manage_users.html', {'users': users})

def admin_login_logs_view(request):
    return render(request, 'admin_dashboard/login_logs.html')

def admin_user_messages(request):
    return render(request, 'admin_dashboard/user_messages.html')

def reply_users(request, user_id, ):
    user = warsUser.objects.get(id=user_id)
    return render(request, 'admin_dashboard/reply_users.html', {'user': user})

def admin_reports_view(request):
    return render(request, 'admin_dashboard/reports.html')

def admin_notifications_view(request):
    return render(request, 'admin_dashboard/notifications.html')

def admin_helpdesk_view(request):
    return render(request, 'admin_dashboard/helpdesk.html')

# Add views for all the other nav links as needed

# <img src="{{ user.profile_picture.url }}" alt="Profile Picture">


@receiver(post_save, sender=warsUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userProfile.objects.create(user=instance)

@receiver(post_save, sender=warsUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def register_user(request):
    if request.method == 'POST':
        try:
            # Extract location data from the form
            province_name = request.POST.get('province')
            district_name = request.POST.get('district')
            sector_name = request.POST.get('sector')
            cell_name = request.POST.get('cell')
            village_name = request.POST.get('village')

            # Get the corresponding Location objects by name
            province = Province.objects.get(name=province_name)
            district = District.objects.get(name=district_name)
            sector = Sector.objects.get(name=sector_name)
            cell = Cell.objects.get(name=cell_name)
            village = Village.objects.get(name=village_name)

            # Validate if email already exists
            email = request.POST.get('email')
            if warsUser.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.")

            # Create the user (we use transaction.atomic to ensure all changes are saved or none)
            with transaction.atomic():
                # Create the user
                user = warsUser.objects.create(
                    names=request.POST.get('names'),
                    email=email,
                    phone=request.POST.get('phone'),
                    nationalId=request.POST.get('nationalId'),
                    dob=request.POST.get('dob'),
                    gender=request.POST.get('gender'),
                    nationality=request.POST.get('nationality'),
                    emergencyContact=request.POST.get('emergencyContact'),
                    profile_pic=request.FILES.get('profile_pic'),
                )

                # Create and link location data
                Location.objects.create(
                    user=user,
                    country='Rwanda',  # Assuming it's always Rwanda
                    province=province,
                    district=district,
                    sector=sector,
                    cell=cell,
                    village=village,
                )

                # Ensure userProfile does not already exist before creating
                try:
                    userProfile.objects.get(user=user)
                except userProfile.DoesNotExist:
                    # Create user profile with default role 'Customer' if it does not exist
                    userProfile.objects.create(user=user, role='Customer')


                # Generate temporary password
                allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
                temp_password = get_random_string(length=12, allowed_chars=allowed_chars)

                # Create and hash the password
                password_instance = Password.objects.create(user=user)
                password_instance.set_password(temp_password)
                password_instance.save()

                subject = 'Welcome to WARS - Temporary Password'
                from_email = 'no-reply@wars.com'
                recipient = user.email
                temp_password = temp_password

                # Plain text content
                text_content = f'''
                Welcome to WARS!

                Thank you for registering with us. Below is your temporary password:

                Temporary Password: {temp_password}

                Please log in and change your password as soon as possible to secure your account.

                Log in here: http://127.0.0.1:8000/login/

                Best regards,
                The WARS Team
                '''

                # HTML content with clipboard copy functionality
                html_content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Welcome to WARS</title>
                    <style>
                        body {{
                            font-family: 'Times New Roman', sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f8f9fa;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 20px auto;
                            padding: 20px;
                            background: #ffffff;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        }}
                        .email-header {{
                            background-color: #007bff;
                            color: #ffffff;
                            padding: 20px;
                            text-align: center;
                            border-radius: 8px 8px 0 0;
                        }}
                        .email-body {{
                            padding: 20px;
                            color: #333333;
                            line-height: 1.6;
                        }}
                        .email-footer {{
                            text-align: center;
                            font-size: 12px;
                            color: #888888;
                            margin-top: 20px;
                        }}
                        .temporary-password {{
                            display: block;
                            background-color: #f8d7da;
                            color: #721c24;
                            padding: 10px;
                            border-radius: 4px;
                            margin: 10px 0;
                            font-weight: bold;
                            text-align: center;
                        }}
                        .btn {{
                            display: inline-block;
                            padding: 10px 20px;
                            font-size: 14px;
                            color: #ffffff;
                            background-color: #007bff;
                            text-decoration: none;
                            border-radius: 4px;
                            margin-top: 20px;
                        }}
                        a{{
                            text-decoration: none;
                            color:#ffffff;
                        }}
                        .btn:hover {{
                            background-color: #0056b3;
                        }}
                        .copy-btn {{
                            display: inline-block;
                            margin-top: 10px;
                            padding: 10px 20px;
                            background-color: #28a745;
                            color: white;
                            border-radius: 4px;
                            border: none;
                            cursor: pointer;
                        }}
                        .copy-btn:hover {{
                            background-color: #218838;
                        }}
                        .copy-btn:focus,.temporary-password:focus {{
                            outline: none;
                            cursor: pointer;
                        }}
                    </style>
                    <script>
                        function copyPassword() {{
                            var password = document.getElementById("tempPassword");
                            var textArea = document.createElement("textarea");
                            textArea.value = password.textContent;
                            document.body.appendChild(textArea);
                            textArea.select();
                            document.execCommand("copy");
                            document.body.removeChild(textArea);
                            alert("Password copied to clipboard!");
                        }}
                    </script>
                </head>
                <body>
                    <div class="email-container">
                        <div class="email-header">
                            <h1>Welcome to WARS</h1>
                        </div>
                        <div class="email-body">
                            <p>Dear {user.names},</p>
                            <p>Thank you for registering with WARS!
                            <br>
                            Below is your first login password:</p>
                            <div id="tempPassword" class="temporary-password">{temp_password}</div>
                            <button class="copy-btn" onclick="copyPassword()">Copy Password</button>
                            <p>Use this password to log in to your account and ensure you change it immediately for security purposes.</p>
                            <a href="http://127.0.0.1:8000/login/" class="btn">Log In to Your Account</a>
                            <p>We are excited to have you on board and look forward to serving you!</p>
                            <p>Best regards,</p>
                            <p>The WARS Team</p>
                        </div>
                        <div class="email-footer">
                            <p>Copyright &copy; 2024 WARS. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                '''

                # Send the email
                email = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
                email.attach_alternative(html_content, "text/html")
                email.send()


            # Display success message and redirect
            messages.success(request, 'Registration successful! Temporary password sent to your email.')
            return redirect('registration_success')

        except ValidationError as e:
            messages.error(request, str(e))  # Show validation errors as error messages
        except IntegrityError as e:
            messages.error(request, 'A database error occurred. Please try again later.')
            print(e)
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')

    else:
        RegistrationForm()  # Assuming you have a RegistrationForm for the POST request

    return render(request, 'register.html')

# Function to generate OTP
def generate_otp():
    characters = string.ascii_letters + string.digits + string.punctuation
    otp = ''.join(random.choice(characters) for _ in range(9))
    return otp

def login_user(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Authenticate user by checking the email in WarsUser model
            try:
                user = warsUser.objects.get(email=email)
            except warsUser.DoesNotExist:
                logger.error(f"Login failed: Invalid email address {email}.")
                return JsonResponse({'success': False, 'message': 'Invalid email address'})

            # Retrieve the stored password hash from Password model
            try:
                password_record = Password.objects.get(user=user)
            except Password.DoesNotExist:
                logger.error(f"Login failed: Password record not found for user {email}.")
                return JsonResponse({'success': False, 'message': 'Password record not found'})

            # Verify the provided password using Argon2 hasher
            if not check_password(password, password_record.password_hash):
                logger.error(f"Login failed: Invalid password for email {email}.")
                return JsonResponse({'success': False, 'message': 'Invalid password'})

            # Generate OTP and set expiration time (e.g., 10 minutes)
            otp = generate_otp()  # Example OTP generation
            print(f"Generated OTP: {otp}")
            password_record.otp = otp
            password_record.save()
            print(f"Stored OTP in database: {password_record.otp}")

            expiration_time = datetime.now() + timedelta(minutes=10)
            print(expiration_time)

            # Store OTP and expiration time in Password model
            password_record.otp = otp
            password_record.otp_expiration_time = expiration_time
            password_record.save()

            # Prepare the email to send OTP
            subject = 'WARS Account OTP Code'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient = email

            # Plain text content
            text_content = f'''
            Your OTP Code

            Your OTP code is: {otp}

            Please use this code to verify your identity. It will expire in 10 minutes.

            Best regards,
            The WARS Team
            '''

            # HTML content with professional design and copy functionality for OTP
            html_content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>WARS OTP Code</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f7f7f7;
                        }}
                        .email-container {{
                            max-width: 500px;
                            margin: 20px auto;
                            padding: 20px;
                            background: #ffffff;
                            border-radius: 6px;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        }}
                        .email-header {{
                            text-align: center;
                            background-color: #4CAF50;
                            color: #ffffff;
                            padding: 15px;
                            border-radius: 6px 6px 0 0;
                        }}
                        .email-body {{
                            padding: 15px;
                            color: #333333;
                            line-height: 1.5;
                        }}
                        .otp-code {{
                            display: block;
                            background-color: #f2f2f2;
                            color: #333333;
                            font-weight: bold;
                            text-align: center;
                            padding: 10px;
                            margin: 15px 0;
                            font-size: 18px;
                            border-radius: 4px;
                        }}
                        .btn {{
                            display: inline-block;
                            padding: 10px 20px;
                            color: #ffffff;
                            background-color: #007bff;
                            text-decoration: none;
                            border-radius: 4px;
                            border:none;
                            text-align: center;
                            font-size: 14px;
                        }}
                        .btn:hover {{
                            background-color: #0056b3;
                        }}
                        .email-footer {{
                            text-align: center;
                            font-size: 12px;
                            color: #888888;
                            margin-top: 15px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="email-header">
                            <h1>WARS OTP Code</h1>
                        </div>
                        <div class="email-body">
                            <p>Dear {user.names},</p>
                            <p>Your OTP code is:</p>
                            <div class="otp-code">{otp}</div>
                            <p>This code is valid for 10 minutes. Please use it to complete your verification.</p>
                            <a href="http://127.0.0.1:8000/login_otp_verification" class="btn">Verify OTP</a>
                            <p>If you did not request this code, please ignore this email.</p>
                        </div>
                        <div class="email-footer">
                            <p>Copyright © 2024 WARS. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>


                    '''

            # Send the email
            email = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            email.attach_alternative(html_content, "text/html")
            email.send()

            logger.info(f"OTP sent successfully to {email}.")
            return JsonResponse({'success': True, 'redirect_url': '/login_otp_verification'})

        except Exception as e:
            # General error logging and immediate halt
            logger.error(f"An unexpected error occurred during login: {e}")
            return JsonResponse({'success': False, 'message': 'An unexpected error occurred'})

    # If the request is GET, render the login page
    return render(request, 'login.html')
# View to handle OTP verification

def login_otp_verification(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        print(f"Email: {email}, Entered OTP: {otp}")

        try:
            # Validate if email exists in warsUser model
            user = warsUser.objects.get(email=email)

            # Retrieve the password record for the user
            password_record = Password.objects.get(user=user)

            # Debugging
            localized_expiration = localtime(password_record.otp_expiration_time)
            localized_now = localtime(now())
            print(f"Stored OTP: {password_record.otp}")
            print(f"Expiration Time (localized): {localized_expiration}")
            print(f"Current Time (localized): {localized_now}")

            # Compare OTP
            stored_otp = password_record.otp.strip() if password_record.otp else None
            entered_otp = otp.strip() if otp else None

            if stored_otp == entered_otp:
                # Check expiration
                if password_record.otp_expiration_time and now() > password_record.otp_expiration_time:
                    return JsonResponse({'success': False, 'message': 'OTP has expired'})

                # Clear OTP and expiration time
                password_record.otp = None
                password_record.otp_expiration_time = None
                password_record.save()

                # Access the related user profile and role
                try:
                    user_profile = user.profile  # Use 'profile' as per related_name
                    print(f"User profile exists: {user_profile}")
                    role = user_profile.role
                    print(f"Role for user: {role}")
                except AttributeError as e:
                    print(f"Error accessing user profile or role: {str(e)}")
                    return JsonResponse({'success': False, 'message': 'User profile or role missing'})

                # Redirect user based on their role
                role_redirects = {
                    'Customer': '/wasac-dashboard',
                    'Manager': '/user_dashboard',
                    'Technician': '/technician_dashboard',
                    'Responsible': '/admin_dashboard',
                }

                if role in role_redirects:
                    return JsonResponse({'success': True, 'redirect_url': role_redirects[role]})
                else:
                    return JsonResponse({'success': False, 'message': 'Unknown role, cannot redirect'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP'})

        except warsUser.DoesNotExist:
            print("User not found in warsUser model")
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Password.DoesNotExist:
            print("Password record not found for the user")
            return JsonResponse({'success': False, 'message': 'Password record not found'})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'success': False, 'message': 'An error occurred while verifying OTP'})

    return render(request, 'login_otp_verification.html')


# Forgot Password

# Function to generate a password reset token
def generate_reset_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(50))
    return token

# View to request password reset (email is required)
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = warsUser.objects.get(email=email)

            # Generate reset token and set expiration time
            reset_token = generate_reset_token()
            expiration_time = now() + timedelta(minutes=10)  # 10 min expiration

            # Store reset token and expiration time in Password model
            password_record, created = Password.objects.get_or_create(user=user)
            password_record.reset_token = reset_token
            password_record.reset_token_expiration = expiration_time
            password_record.save()

            subject = 'Password Reset Request'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient = email
            reset_token = reset_token  # The generated reset token

            # Plain text content
            text_content = f'''
            Password Reset Request

            You have requested to reset your password. Your password reset token is: {reset_token}

            Please use this token to reset your password. It will expire in 10 minutes.

            Best regards,
            The WARS Team
            '''

            # HTML content with professional design and copy functionality for reset token
            html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>WARS - Password Reset Request</title>
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f7f7f7;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: 20px auto;
                        padding: 20px;
                        background: #ffffff;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    .email-header {{
                        background-color: #28a745;
                        color: #ffffff;
                        padding: 20px;
                        text-align: center;
                        border-radius: 8px 8px 0 0;
                    }}
                    .email-body {{
                        padding: 20px;
                        color: #333333;
                        line-height: 1.6;
                    }}
                    .reset-token {{
                        display: block;
                        background-color: #f8d7da;
                        color: #721c24;
                        padding: 10px;
                        border-radius: 4px;
                        margin: 10px 0;
                        font-weight: bold;
                        text-align: center;
                        font-size: 20px;
                    }}
                    .copy-btn {{
                        display: inline-block;
                        margin-top: 10px;
                        padding: 10px 20px;
                        background-color: #007bff;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }}
                    .copy-btn:hover {{
                        background-color: #0056b3;
                    }}
                    .btn {{
                        display: inline-block;
                        padding: 10px 20px;
                        font-size: 14px;
                        color: #ffffff;
                        background-color: #007bff;
                        text-decoration: none;
                        border-radius: 4px;
                        margin-top: 20px;
                    }}
                    a{{
                        color:#fff;
                        text-decoration: none;
                    }}
                    .btn:hover {{
                        background-color: #0056b3;
                    }}
                    .btn:focus,.copy-btn:focus {{
                        outline: none;
                        cursor: pointer;
                    }}
                    .email-footer {{
                        text-align: center;
                        font-size: 12px;
                        color: #888888;
                        margin-top: 20px;
                    }}
                </style>
                <script>
                    function copyToken() {{
                        var tokenElement = document.getElementById("resetToken");
                        var textArea = document.createElement("textarea");
                        textArea.value = tokenElement.textContent;
                        document.body.appendChild(textArea);
                        textArea.select();
                        document.execCommand("copy");
                        document.body.removeChild(textArea);
                        alert("Reset token copied to clipboard!");
                    }}
                </script>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h1>Password Reset Request</h1>
                    </div>
                    <div class="email-body">
                        <p>Dear {user.names},</p>
                        <p>We received a request to reset your password. Below is your password reset token:</p>
                        <div id="resetToken" class="reset-token">{reset_token}</div>
                        <button class="copy-btn" onclick="copyToken()">Copy Token to Clipboard</button>
                        <p>This token is valid for 10 minutes. Please use it to reset your password.</p>
                        <a href="http://127.0.0.1:8000/password-update/" class="btn">Reset Your Password</a>
                        <p>If you did not request this password reset, please ignore this email.</p>
                        <p>Best regards,</p>
                        <p>The WARS Team</p>
                    </div>
                    <div class="email-footer">
                        <p>Copyright &copy; 2024 WARS. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            '''

            # Send the email
            email = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            email.attach_alternative(html_content, "text/html")
            email.send()

            return JsonResponse({'success': True, 'message': 'Reset token sent to your email','redirect_url': '/password-update'})
            #return redirect('password-update')

        except warsUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})

    return render(request, 'password_reset.html')

# Set up logging
logger = logging.getLogger(__name__)

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        reset_token = request.POST.get('reset_token')
        new_password = request.POST.get('new_password')
        print(f"Email: {email}, Reset Token: {reset_token}, New Password: {new_password}")

        if not email or not reset_token or not new_password:
            logger.error("One or more required fields are missing in the request.")
            return JsonResponse({'success': False, 'message': 'Missing required fields'})

        try:
            # Check if email exists in the database
            user = warsUser.objects.get(email__iexact=email)
            password_record = Password.objects.get(user=user)

            # Check if the reset token matches
            if password_record.reset_token == reset_token:
                # Check if the reset token is expired
                if password_record.reset_token_expiration < now():
                    logger.error(f"Reset token for {email} has expired.")
                    return JsonResponse({'success': False, 'message': 'Reset token has expired'})

                # Token is valid and not expired, update the password
                password_record.password_hash = make_password(new_password, hasher='argon2')
                password_record.reset_token = None  # Clear the reset token after use
                password_record.reset_token_expiration = None
                password_record.save()

                logger.info(f"Password successfully reset for {email}.")
                # Redirect to login page after success
                return JsonResponse({'success': True, 'message': 'Password successfully reset', 'redirect_url': '/login'})

            else:
                logger.error(f"Invalid reset token provided for {email}.")
                return JsonResponse({'success': False, 'message': 'Invalid reset token'})

        except warsUser.DoesNotExist:
            logger.error(f"User with email {email} not found.")
            return JsonResponse({'success': False, 'message': 'User not found'})

        except Password.DoesNotExist:
            logger.error(f"Password record not found for user {email}.")
            return JsonResponse({'success': False, 'message': 'Password record not found'})

        except Exception as e:
            # General exception handling for unexpected errors
            logger.error(f"An unexpected error occurred for {email}: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {str(e)}'})

    return render(request, 'password_update.html')

# View to handle the contact form
def contact_view(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Initialize response structure
        response = {}

        # Instantiate and validate the form
        form = ContactMessageForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Process form data (send an email, save to database, etc.)
            # Example: form.save() or sending an email using Django's send_mail function
            # form.save()

            # Add success message if needed
            messages.success(request, "Your message has been sent successfully.")

            # Return a success response
            response['success'] = True
            response['message'] = "Your message has been sent successfully."
        else:
            # Return errors if form is not valid
            response['success'] = False
            response['error'] = form.errors.as_text()  # You can customize this part for better error reporting

        return JsonResponse(response)

    # For GET requests, render the contact page with an empty form
    return render(request, 'contact.html', {'form': ContactMessageForm()})

# adding Rwanda administrative data

def add_province(request):
    if request.method == 'POST':
        form = ProvinceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_provinces')
    else:
        form = ProvinceForm()
    return render(request, 'add_edit_province.html', {'form': form})

def add_district(request, province_id):
    province = get_object_or_404(Province, id=province_id)
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if District.objects.filter(name=request.POST.get('name'), province=province).exists():
            form.add_error('name', 'District with this name already exists in this province.')
        if form.is_valid():
            district = form.save(commit=False)
            district.province = province
            district.save()
            return redirect('list_districts', province_id=province.id)
    else:
        form = DistrictForm()
    return render(request, 'add_edit.html', {'form': form, 'title': f'Add District to {province.name}'})

def add_sector(request, district_id):
    district = get_object_or_404(District, id=district_id)
    if request.method == 'POST':
        form = SectorForm(request.POST)
        if Sector.objects.filter(name=request.POST.get('name'), district=district).exists():
            form.add_error('name', 'Sector with this name already exists in this district.')
        if form.is_valid():
            sector = form.save(commit=False)
            sector.district = district
            sector.save()
            return redirect('list_sectors', district_id=district.id)
    else:
        form = SectorForm()
    return render(request, 'add_edit.html', {'form': form, 'title': f'Add Sector to {district.name}'})

def add_cell(request, sector_id):
    sector = get_object_or_404(Sector, id=sector_id)
    if request.method == 'POST':
        form = CellForm(request.POST)
        if Cell.objects.filter(name=request.POST.get('name'), sector=sector).exists():
            form.add_error('name', 'Cell with this name already exists in this sector.')
        if form.is_valid():
            cell = form.save(commit=False)
            cell.sector = sector
            cell.save()
            return redirect('list_cells', sector_id=sector.id)
    else:
        form = CellForm()
    return render(request, 'add_edit.html', {'form': form, 'title': f'Add Cell to {sector.name}'})


def add_village(request, cell_id):
    cell = get_object_or_404(Cell, id=cell_id)
    if request.method == 'POST':
        form = VillageForm(request.POST)
        if Village.objects.filter(name=request.POST.get('name'), cell=cell).exists():
            form.add_error('name', 'A village with this name already exists in the selected cell.')
        if form.is_valid():
            village = form.save(commit=False)
            village.cell = cell
            village.save()
            return redirect('list_villages', cell_id=cell.id)
    else:
        form = VillageForm()
    return render(request, 'add_edit.html', {'form': form, 'title': f'Add Village to {cell.name}'})

# Listing data from Rwanda

def list_provinces(request):
    provinces = Province.objects.all().order_by('name')
    return render(request, 'list_provinces.html', {'provinces': provinces})

def list_districts(request, province_id):
    province = get_object_or_404(Province, id=province_id)
    districts = District.objects.filter(province=province).order_by('name')
    return render(request, 'list_districts.html', {'districts': districts, 'province': province})

def list_sectors(request, district_id):
    district = get_object_or_404(District, id=district_id)
    sectors = Sector.objects.filter(district=district).order_by('name')
    return render(request, 'list_sectors.html', {'sectors': sectors, 'district': district})

def list_cells(request, sector_id):
    sector = get_object_or_404(Sector, id=sector_id)
    cells = Cell.objects.filter(sector=sector).order_by('name')
    return render(request, 'list_cells.html', {'cells': cells, 'sector': sector})

def list_villages(request, cell_id):
    cell = get_object_or_404(Cell, id=cell_id)
    villages = Village.objects.filter(cell=cell).order_by('name')
    return render(request, 'list_villages.html', {'villages': villages, 'cell': cell})

def get_provinces(request):
    # Fetch provinces and return names
    provinces = Province.objects.all().order_by('name').values('name')
    return JsonResponse(list(provinces), safe=False)

def get_districts(request, province_name):
    # Fetch districts by province name and return names
    districts = District.objects.filter(province__name=province_name).order_by('name').values('name')
    return JsonResponse(list(districts), safe=False)

def get_sectors(request, district_name):
    # Fetch sectors by district name and return names
    sectors = Sector.objects.filter(district__name=district_name).order_by('name').values('name')
    return JsonResponse(list(sectors), safe=False)

def get_cells(request, sector_name):
    # Fetch cells by sector name and return names
    cells = Cell.objects.filter(sector__name=sector_name).order_by('name').values('name')
    return JsonResponse(list(cells), safe=False)

def get_villages(request, cell_name):
    # Fetch villages by cell name and return names
    villages = Village.objects.filter(cell__name=cell_name).order_by('name').values('name')
    return JsonResponse(list(villages), safe=False)

"""
# Dashboard for Admin
@login_required
def admin_dashboard(request):
    # Filter out users who have not verified their location
    unverified_users = User.objects.filter(location_verified=False)
    return render(request, 'admin_dashboard.html', {'users': unverified_users})

# Dashboard for Sedo Cell
@login_required
def sedo_cell_dashboard(request):
    return render(request, 'sedo_cell_dashboard.html')

# Dashboard for Sedo Sector
@login_required
def sedo_sec_dashboard(request):
    return render(request, 'sedo_sec_dashboard.html')

# Dashboard for Sedo District
@login_required
def sedo_dist_dashboard(request):
    return render(request, 'sedo_dist_dashboard.html')

# Dashboard for WASAC Manager
@login_required
def wasac_dashboard(request):
    return render(request, 'wasac_dashboard.html')

# Dashboard for General User
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

# Location Verification Page
@login_required
def location_verification(request):
    return render(request, 'location_verification.html')

# Function to check if the user is an admin
def is_admin(user):
    return user.user_profile == 'admin'

# Verify Location by Admin
@login_required
@user_passes_test(is_admin)
def verify_location(request, user_id):
    # Get the user to be verified
    user = get_object_or_404(User, id=user_id)
    
    # Example of location check before verification
    if not user.province or not user.district:
        messages.error(request, 'User location is incomplete and cannot be verified.')
        return redirect('admin_dashboard')
    
    # Update location_verified to True
    user.location_verified = True
    user.save()
    
    # Provide a success message to the admin
    messages.success(request, f'Location for {user.names} has been successfully verified.')
    return redirect('admin_dashboard')
"""