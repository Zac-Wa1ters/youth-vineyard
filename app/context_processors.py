from .models import SiteBranding, SiteFooter


def site_branding(request):
    return {
        "site_branding": SiteBranding.objects.first()
    }

def site_footer(request):
    return {
        "site_footer": SiteFooter.objects.first()
    }

