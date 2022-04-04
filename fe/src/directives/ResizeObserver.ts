import {VNodeDirective} from 'vue/types/vnode';
import {ResizeObserver} from '@juggle/resize-observer';

class ResizeObserverElement extends HTMLElement {
  resizeObserver?: ResizeObserver;
  callback?: (size: DOMRectReadOnly) => void;
}

function inserted(el: ResizeObserverElement, binding: VNodeDirective) {
  el.callback = binding.value;
  el.resizeObserver = new ResizeObserver((entries, observer) => {
    for (const entry of entries) {
      if (entry.target === el && el.callback) {
        el.callback(entry.contentRect);
      }
    }
  });
  el.resizeObserver.observe(el);
}

function unbind(el: ResizeObserverElement) {
  if (!el.resizeObserver) {
    return;
  }

  el.resizeObserver.disconnect();
  delete el.resizeObserver;
  delete el.callback;
}

export const ResizeObserverDirective = {
  inserted,
  unbind,
}

export default ResizeObserverDirective;
