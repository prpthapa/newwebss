"""
Health check endpoint.

Returns 200 with a tiny JSON body, no DB access. Suitable for Render's
free-tier health-check and any external uptime monitor.

Note: this is intentionally NOT a full readiness check (no DB ping) — it
must stay cheap so a slow/dead database doesn't trip the load balancer's
health check and cause the service to cycle. Use a separate readiness probe
if you need that.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def healthz(request):
    return JsonResponse({"status": "ok"})