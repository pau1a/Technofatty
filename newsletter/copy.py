from django.conf import settings


def get_copy() -> dict:
    copy = {
        "error": "Something went wrong. Please try again.",
        "server_busy": "We’re having trouble right now. Try again in a few minutes.",
        "required_email": "Please enter your email address to subscribe.",
        "invalid_email": "Enter a valid email address (example: name@example.com).",
    }
    if getattr(settings, "OPT_IN_MODE", "single") == "double":
        copy["success"] = (
            "Thanks — please check your inbox and confirm your subscription to start receiving the newsletter."
        )
    else:
        copy["success_no_confirm"] = (
            "Thanks — you’re subscribed and will get the next newsletter."
        )
    return copy
