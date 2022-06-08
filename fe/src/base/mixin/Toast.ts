import {Vue, Component} from 'vue-property-decorator';
import SimpleToast from '@/components/SimpleToast.vue';

@Component
export default class Toast extends Vue {
  simpleToast(message: any, detail?: any) {
    return {
      component: SimpleToast,
      props: {
        message: message?.toString() || '',
        detail: detail?.toString() || '',
      },
      listeners: {
        click: () => {},
      },
    };
  }

  toastSuccess(message: any, detail?: any) {
    this.$toast.success(this.simpleToast(message, detail));
  }

  toastInfo(message: any, detail?: any) {
    this.$toast.info(this.simpleToast(message, detail));
  }

  toastWarning(message: any, detail?: any) {
    this.$toast.warning(this.simpleToast(message, detail));
  }

  toastError(message: any, detail?: any) {
    this.$toast.error(this.simpleToast(message, detail));
  }

  toastRequestSuccess(detail?: any) {
    this.toastSuccess(this.$t('toast.request_success').toString(), detail);
  }

  toastRequestFailure(error?: any) {
    const message = this.$t('toast.request_failure').toString();
    if (!error) {
      this.toastError(message);
      return;
    }

    if (typeof error.response !== 'undefined') {
      const code = error.response.status || '?';
      const reason = error.response.statusText || 'Unknown';
      this.toastError(message, `[${code}] ${reason}`);
    } else {
      this.toastError(message, error.toString());
    }
  }
}
