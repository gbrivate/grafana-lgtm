/* instrumentation.ts */

import * as opentelemetry from '@opentelemetry/api';
import {registerInstrumentations} from '@opentelemetry/instrumentation';

import {
  WebTracerProvider,
  BatchSpanProcessor,
} from '@opentelemetry/sdk-trace-web';

import {OTLPTraceExporter} from '@opentelemetry/exporter-trace-otlp-http';
import {B3Propagator} from '@opentelemetry/propagator-b3';

import {
  MeterProvider,
  PeriodicExportingMetricReader,
} from '@opentelemetry/sdk-metrics';

import {OTLPMetricExporter} from '@opentelemetry/exporter-metrics-otlp-http';

import {Resource} from '@opentelemetry/resources';
import {SemanticResourceAttributes} from '@opentelemetry/semantic-conventions';

import {getWebAutoInstrumentations} from '@opentelemetry/auto-instrumentations-web';

import {onCLS, onLCP, onFID, onINP} from 'web-vitals';

import {context, trace} from '@opentelemetry/api';

/* ------------------------------------------------------------------ */
/* Resource                                                           */
/* ------------------------------------------------------------------ */

const resource = new Resource({
  [SemanticResourceAttributes.SERVICE_NAME]: 'fastapi-mfe-test',
  [SemanticResourceAttributes.SERVICE_VERSION]: '0.1.0',
});

/* ------------------------------------------------------------------ */
/* Tracing                                                            */
/* ------------------------------------------------------------------ */

const tracerProvider = new WebTracerProvider({resource});

export const userInteractionHook = (span: any, element: HTMLElement) => {
  if (!element || typeof element.getAttribute !== 'function') return;

  const id = element.id;
  const nameAttr = element.getAttribute('name');
  const otelName = element.getAttribute('data-otel-name');
  const ariaLabel = element.getAttribute('aria-label');
  const tag = element.tagName.toLowerCase();

  // Choose the best identifier
  const identifier = otelName || id || nameAttr || ariaLabel || element.innerText?.slice(0, 15) || 'anonymous';

  // Update the name
  span.updateName(`UI Click: <${tag}> ${identifier}`);

  // Add attributes for filtering
  span.setAttributes({
    'ui.element.id': id || 'none',
    'ui.element.name': nameAttr || 'none',
    'ui.element.tag': tag,
    'ui.element.data_name': otelName || 'none'
  });
};

tracerProvider.addSpanProcessor(
  new BatchSpanProcessor(
    new OTLPTraceExporter({
      url: '/otel/v1/traces',
    })
  )
);

tracerProvider.register({
  propagator: new B3Propagator(),
});

/* ------------------------------------------------------------------ */
/* Auto-instrumentations (Fetch, XHR, Document, User Interaction)     */
/* ------------------------------------------------------------------ */

registerInstrumentations({
  instrumentations: [
    getWebAutoInstrumentations({
      '@opentelemetry/instrumentation-user-interaction': {
        enabled: true,
        // This is the trick: use the "shouldPrevent" check to modify the span
        shouldPreventSpanCreation: (eventType, element, span) => {
          if (element instanceof HTMLElement && span) {

            const id = element.id || 'none';
            const nameAttr = element.getAttribute('name') || 'none';
            const otelName = element.getAttribute('data-otel-name');
            const tag = element.tagName.toLowerCase();

            // 1. Set the descriptive name
            const identifier = otelName || (id !== 'none' ? id : null) || (nameAttr !== 'none' ? nameAttr : null) || element.innerText?.slice(0, 15) || 'anonymous';
            span.updateName(`UI Click: <${tag}> ${identifier}`);

            // 2. Add extra attributes for backend filtering
            span.setAttribute('ui.element.id', id);
            span.setAttribute('ui.element.name', nameAttr);
            span.setAttribute('ui.element.tag', tag);
            if (otelName) span.setAttribute('ui.element.data_name', otelName);
          }

          return false; // MUST return false so the span is actually created
        },
      },
      '@opentelemetry/instrumentation-fetch': {
        propagateTraceHeaderCorsUrls: /.+/,
        clearTimingResources: true,
      },
      '@opentelemetry/instrumentation-xml-http-request': {
        propagateTraceHeaderCorsUrls: /.+/,
      },
    }),
  ],
});

/* ------------------------------------------------------------------ */
/* Metrics                                                            */
/* ------------------------------------------------------------------ */

const metricExporter = new OTLPMetricExporter({
  url: '/otel/v1/metrics',
});

const metricReader = new PeriodicExportingMetricReader({
  exporter: metricExporter,
  exportIntervalMillis: 15000,
});

const meterProvider = new MeterProvider({resource});
meterProvider.addMetricReader(metricReader);

opentelemetry.metrics.setGlobalMeterProvider(meterProvider);

const meter = opentelemetry.metrics.getMeter(
  'fastapi-mfe-test-frontend',
  '0.1.0'
);

/* ------------------------------------------------------------------ */
/* 1) Web Vitals Metrics                                              */
/* ------------------------------------------------------------------ */
/* Names align with backend Prometheus/OpenTelemetry conventions      */
/* Units are milliseconds where applicable                            */
/* ------------------------------------------------------------------ */

const webVitalsLCP = meter.createHistogram('web_vitals_lcp_ms', {
  description: 'Largest Contentful Paint',
  unit: 'ms',
});

const webVitalsCLS = meter.createHistogram('web_vitals_cls', {
  description: 'Cumulative Layout Shift',
});

const webVitalsFID = meter.createHistogram('web_vitals_fid_ms', {
  description: 'First Input Delay',
  unit: 'ms',
});

const webVitalsINP = meter.createHistogram('web_vitals_inp_ms', {
  description: 'Interaction to Next Paint',
  unit: 'ms',
});

onLCP((metric) => {
  webVitalsLCP.record(metric.value);
});

onCLS((metric) => {
  webVitalsCLS.record(metric.value);
});

onFID((metric) => {
  webVitalsFID.record(metric.value);
});

onINP((metric) => {
  webVitalsINP.record(metric.value);
});

/* ------------------------------------------------------------------ */
/* 3) Frontend ↔ Backend Metric Alignment                              */
/* ------------------------------------------------------------------ */
/*
  Backend (FastAPI) example metrics:
    - http_server_requests_total
    - http_server_request_duration_seconds

  Frontend equivalents:
    - http_client_requests_total
    - http_client_request_duration_ms

  Shared labels:
    - service.name
    - service.version
    - http.method
    - http.url
*/
/* ------------------------------------------------------------------ */

/* Example custom business metric aligned across FE / BE */

export const frontendBusinessEvents = meter.createCounter(
  'frontend_business_events_total',
  {
    description: 'Business events emitted by frontend',
  }
);

/* Example usage elsewhere in app:
   frontendBusinessEvents.add(1, { event: 'checkout_started' });
*/

/* # Frontend error metrics (required for error rate)
const httpClientErrors = meter.createCounter(
  'http_client_errors_total',
  {
    description: 'Total HTTP client errors',
  }
);

if (entry.responseStatus && entry.responseStatus >= 400) {
  httpClientErrors.add(1, {
    'http.route': route,
    'http.status_code': entry.responseStatus,
  });
}
*/

/* ------------------------------------------------------------------ */
/* End of file                                                        */
/* ------------------------------------------------------------------ */
