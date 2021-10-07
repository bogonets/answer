import {Vue, Component, Watch} from 'vue-property-decorator';
import moment from 'moment-timezone';

@Component
export default class WatchI18n extends Vue {
    @Watch('$vuetify.lang.current')
    onWatchI18n(newVal: string, oldVal: string) {
        console.debug(`Watch i18n: ${oldVal} -> ${newVal}`);
        this.$i18n.locale = newVal;
        moment.locale(newVal);
    }
}
