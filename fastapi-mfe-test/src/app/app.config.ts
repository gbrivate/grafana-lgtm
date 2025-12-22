import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import {HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi} from '@angular/common/http';
import {OtelHttpInterceptor} from './otel-http.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),

    // REQUIRED for HttpClient + interceptors
    provideHttpClient(withInterceptorsFromDi()),

    // OpenTelemetry HTTP metrics interceptor
    {
      provide: HTTP_INTERCEPTORS,
      useClass: OtelHttpInterceptor,
      multi: true,
    },
  ]
};
