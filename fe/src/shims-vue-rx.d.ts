import Vue from 'vue'
import VueRx from 'vue-rx'
import { Observable, Observables, WatchOptions, WatchObservable } from "vue-rx";

declare module "vue/types/vue" {
  interface Vue {
    $observables: Observables;
    $watchAsObservable(expr: string, options?: WatchOptions): Observable<WatchObservable<any>>
    $watchAsObservable<T>(fn: (this: this) => T, options?: WatchOptions): Observable<WatchObservable<T>>
    $eventToObservable(event: string): Observable<{name: string, msg: any}>
    $subscribeTo<T>(
      observable: Observable<T>,
      next: (t: T) => void,
      error?: (e: any) => void,
      complete?: () => void): void
    $fromDOMEvent(selector: string | null, event: string): Observable<Event>
    $createObservableMethod(methodName: string): Observable<any>
  }
}