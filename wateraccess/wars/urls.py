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

    # Adding User data

    path('registration-success/', views.registration_success, name='registration_success'),

    path('contact/', views.contact_view, name='contact'),

    # Dashboards urls

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sedo_cell_dashboard/', views.sedo_cell_dashboard, name='sedo_cell_dashboard'),
    path('sedo_sec_dashboard/', views.sedo_sec_dashboard, name='sedo_sec_dashboard'),
    path('sedo_dist_dashboard/', views.sedo_dist_dashboard, name='sedo_dist_dashboard'),
    path('wasac_dashboard/', views.wasac_dashboard, name='wasac_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),


    # User System Dashboard urls

     path('dashboard/profile/', views.profile_view, name='dashboard-profile'),
    path('dashboard/providers/', views.providers_view, name='dashboard-providers'),
    path('dashboard/reports/', views.reports_view, name='dashboard-reports'),
    path('dashboard/cases/', views.cases_view, name='dashboard-cases'),
    path('dashboard/helpdesk/', views.helpdesk_view, name='dashboard-helpdesk'),
    path('dashboard/notifications/', views.notifications_view, name='dashboard-notifications'),
    path('dashboard/logout/', views.logout, name='logout'),

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
