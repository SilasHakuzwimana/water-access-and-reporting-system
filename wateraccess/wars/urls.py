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

    path('dashboard/', views.branch_dashboard, name='branch_dashboard'),
    path('wasac/branch_management/', views.branch_management, name='branch_management'),
    path('wasac/tap_monitoring/', views.tap_monitoring, name='tap_monitoring'),
    path('wasac/case_assignment/', views.case_assignment, name='case_assignment'),
    path('wasac/performance_reports/', views.performance_reports, name='performance_reports'),

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
    path('customer/profile/', views.profile_view, name='profile'),
    path('customer/cases/', views.cases_view, name='cases'),
    path('customer/notifications/', views.notifications_view, name='notifications'),
    path('customer/service-requests/', views.service_requests_view, name='service_requests'),
    path('customer/helpdesk/', views.helpdesk_view, name='helpdesk'),
    #path('customer/logout/', views.logout, name='logout'),

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
