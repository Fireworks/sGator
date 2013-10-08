from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from sgator import views
from sgator import custom_backends

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ama.views.home', name='home'),
    # url(r'^ama/', include('ama.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', views.home, name="home"),
    
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}, name='logout'),

    # static pages
    url(r'about/', views.static_page("about.html", "About")),
    url(r'profile/', views.static_page("profile.html", "Profile")),
    url(r'courses/', views.static_page("courses.html", "Courses")),
    url(r'search/', views.search),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Registration page
    url(r'^accounts/register/$', custom_backends.RegistrationRedirect.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
