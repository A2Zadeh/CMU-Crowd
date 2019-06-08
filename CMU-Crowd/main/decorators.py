from django.contrib.auth.decorators import user_passes_test

def worker_required(function=None):
  actual_decorator = user_passes_test(
    lambda u: u.is_worker)
  if function:
    return actual_decorator(function)
  return actual_decorator

def admin_required(function=None):
  actual_decorator = user_passes_test(
    lambda u: u.is_admin)
  if function:
    return actual_decorator(function)
  return actual_decorator