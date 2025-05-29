from django.conf import settings


def settings_context(request):
    public_settings = {
        key: getattr(settings, key)
        for key in dir(settings)
        if key.isupper() and not key.startswith("_")
    }
    return {"settings_dict": public_settings}
