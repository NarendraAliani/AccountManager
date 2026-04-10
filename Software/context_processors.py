from .models import FirmSettings


def firm_settings(request):
	return {
		"firm": FirmSettings.current(),
	}
