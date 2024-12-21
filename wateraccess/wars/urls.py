from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_user, name='login'),
    path('login_otp_verification/', views.login_otp_verification, name='login_otp_verification'),
    path('register/', views.register_user, name='register_user'),
    path('registration-otp-verification/', views.register_otp_verification, name='register_otp_verification'),
    path('logout/', views.login, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-update/', views.reset_password, name='password_update'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('contact/', views.contact_view, name='contact'),

    # Dashboards urls

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sedo_cell_dashboard/', views.sedo_cell_dashboard, name='sedo_cell_dashboard'),
    path('technician_dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('responsible_dashboard/', views.responsible_dashboard, name='responsible_dashboard'),
    path('wasac-dashboard/', views.wasac_dashboard, name='wasac_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),

    # Admin urls

    path('profile/', views.profile_view, name='profile'),
    path('manage-users/', views.manage_users_view, name='manage_users'),
    path('case-categories/', views.case_categories_view, name='case_categories'),
    path('reported-cases/', views.reported_cases_view, name='reported_cases'),
    path('branch-overview/', views.branch_overview_view, name='branch_overview'),
    path('reports/', views.reports_view, name='reports'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('help-desk/', views.help_desk_view, name='help_desk'),
    path('logout/', views.logout_view, name='logout'),


    # Wasac Branch urls

    path('branch/dashboard/', views.branch_dashboard, name='branch_dashboard'),
    path('branch/branch_management/', views.branch_management, name='branch_management'),
    path('branch/tap_monitoring/', views.tap_monitoring, name='tap_monitoring'),
    path('add-tap/', views.add_tap, name='add_tap'),
    path('edit-tap/<int:tap_id>/', views.edit_tap, name='edit_tap'),
    path('delete-tap/<int:tap_id>/', views.delete_tap, name='delete_tap'),
    path('branch/case_assignment/', views.case_assignment, name='case_assignment'),
    path('assign-case/', views.assign_case, name='assign_case'),
    path('update-case/<int:case_id>/', views.update_case_status, name='update_case'),
    
    path('branch/performance_reports/', views.performance_reports, name='performance_reports'),

    # Responsible System Dashboard Urls

    path('', views.dashboard, name='responsible_dashboard'),  # Responsible Dashboard
    path('dashboard/assign-technicians/', views.assign_technicians, name='assign_technicians'),
    path('dashboard/case-management/', views.case_management, name='case_management'),
    path('dashboard/escalate-case/<int:case_id>/', views.escalate_case, name='escalate_case'),
    path('dashboard/generate-reports/', views.generate_reports, name='generate_reports'),

    # Admin System Dashboard urls

    path('wasac/dashboard/', views.dashboard, name='dashboard'),
    path('wasac/user_management/', views.user_management, name='user_management'),
    path('wasac/case_categories/', views.case_categories, name='case_categories'),
    path('wasac/report_generation/', views.report_generation, name='report_generation'),

    # User System Dashboard urls

    path('dashboard/', views.load_customer_dashboard, name='customer_dashboard'),
    path('user_dashboard/customer/profile/', views.profile_view, name='profile'),
    path('user_dashboard/customer/cases_view/', views.case_view, name='cases'),
    path('user_dashboard/customer/cases_view/', views.cases_view, name='cases'),
    path('user_dashboard/customer/notifications/', views.notifications_view, name='notifications'),
    path('user_dashboard/customer/service-requests/', views.service_requests_view, name='service_requests'),
    path('user_dashboard/customer/helpdesk/', views.helpdesk_view, name='helpdesk'),
    #path('user_dashboard/customer/logout/', views.logout, name='logout'),

    # Admin System Dashboard urls

    path('profile/', views.admin_profile_view, name='profile'),
    path('manage-users/', views.admin_manage_users_view, name='manage_users'),
    path('login-logs/', views.admin_login_logs_view, name='login_logs'),
    path('reports/', views.admin_reports_view, name='reports'),
    path('user-messages/', views.admin_user_messages, name='user_messages'),
    path('reply-users/<int:user_id>', views.reply_users, name='reply_users'),
    path('notifications/', views.admin_notifications_view, name='notifications'),
    path('helpdesk/', views.admin_helpdesk_view, name='helpdesk'),
    # Add more paths as needed

    # Adding Rwanda administrative data

    path('add-province/', views.add_province, name='add_province'),
    path('add-district/<int:province_id>/', views.add_district, name='add_district'),
    path('add-sector/<int:district_id>/', views.add_sector, name='add_sector'),
    path('add-cell/<int:sector_id>/', views.add_cell, name='add_cell'),
    path('add-village/<int:cell_id>/', views.add_village, name='add_village'),

    # List Province, District, Sector, Cell, Village

    path('list-provinces/', views.list_provinces, name='list_provinces'),
    path('list_districts/<int:province_id>/', views.list_districts, name='list_districts'),
    path('list_sectors/<int:district_id>/', views.list_sectors, name='list_sectors'),
    path('list_cells/int:sector_id/', views.list_cells, name='list_cells'),
    path('list_villages/<int:cell_id>/', views.list_villages, name='list_villages'),

    # Get Province, District, Sector, Cell, Village

    path('get-provinces/', views.get_provinces, name='get_provinces'),
    path('get-districts/<str:province_name>/', views.get_districts, name='get_districts'),
    path('get-sectors/<str:district_name>/', views.get_sectors, name='get_sectors'),
    path('get-cells/<str:sector_name>/', views.get_cells, name='get_cells'),
    path('get-villages/<str:cell_name>/', views.get_villages, name='get_villages'),



     # Case Management
    path('', views.case_list, name='case_list'),  # List all cases
    path('assign/', views.assign_case, name='assign_case'),  # Assign a new case
    path('assign/<int:case_id>/', views.assign_case, name='assign_case_with_id'),  # Assign an existing case
    path('reassign/<int:case_id>/', views.reassign_case, name='reassign_case'),  # Reassign a case

    # User Profile Management
    path('profile/', views.user_profile_view, name='user_profile'),  # View the user profile

    # For technicians, showing cases assigned to them
    path('technician/profile/', views.user_profile_view, name='technician_profile'),  # View technician profile and their cases
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
