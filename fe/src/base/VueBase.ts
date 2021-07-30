import { Vue, Watch } from 'vue-property-decorator';
import { RawLocation } from 'vue-router';

export default class VueBase extends Vue {

    @Watch('$vuetify.lang.current')
    updateI18n(newVal: string, oldVal: string) {
        this.$i18n.locale = newVal;
    }

    get currentRoutePath(): string {
        return this.$router.currentRoute.path;
    }

    push(location: RawLocation) {
        this.$router.push(location).catch((reason: any) => {
            if (reason.name !== 'NavigationDuplicated') {
                throw reason;
            }
        })
    }
}
