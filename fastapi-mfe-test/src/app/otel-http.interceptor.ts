import {Injectable} from '@angular/core';
import {HttpHandler, HttpInterceptor, HttpRequest, HttpResponse} from '@angular/common/http';
import {tap} from 'rxjs';
import opentelemetry from '@opentelemetry/api';

@Injectable()
export class OtelHttpInterceptor implements HttpInterceptor {
  meter = opentelemetry.metrics.getMeter(
    'fastapi-mfe-test',
    '0.1.0'
  );


  httpClientDuration = this.meter.createHistogram(
    'http_client_request_duration_ms',
    {
      description: 'HTTP client request latency',
      unit: 'ms',
    }
  );

  httpClientRequests = this.meter.createCounter(
    'http_client_requests_total',
    {
      description: 'Total HTTP client requests',
    }
  );

  httpClientErrors = this.meter.createCounter(
    'http_client_errors_total',
    {
      description: 'Total HTTP client errors',
    }
  );

  normalizeRoute = (url: string) => {
    try {
      const u = new URL(url, window.location.origin);
      return u.pathname
        .replace(/\/\d+/g, '')        // remove numeric IDs
        .replace(/\/$/, '') || '/';
    } catch {
      return 'unknown';
    }
  }

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const start = performance.now();
    const route = this.normalizeRoute(req.url);

    return next.handle(req).pipe(
      tap({
        next: (event) => {
          if (event instanceof HttpResponse) {
            const duration = performance.now() - start;

            this.httpClientDuration.record(duration, {
              'http.route': route,
              'http.method': req.method,
              'http.status_code': event.status,
            });

            this.httpClientRequests.add(1, {
              'http.route': route,
              'http.method': req.method,
            });
          }
        },
        error: (err) => {
          this.httpClientErrors.add(1, {
            'http.route': route,
            'http.method': req.method,
            'http.status_code': err.status || 'NETWORK_ERROR',
          });
        },
      })
    );
  }
}
