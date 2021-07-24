import { Vue, Watch } from 'vue-property-decorator';
import { Extra } from "@/apis/api-v2";

export default class VueBase extends Vue {

    @Watch('$vuetify.lang.current')
    updateI18n(newVal: string, oldVal: string) {
        this.$i18n.locale = newVal;
    }

    private hasLoggedInSession(): boolean {
        return !!this.$localStore.access;
    }

    private updateExtra(key: string, value: any) {
        if (!this.hasLoggedInSession()) {
            console.debug('The logged in session does not exist.');
            return;
        }

        console.debug('A logged in session already exists.');
        const user = this.$localStore.user;
        if (user.extra === undefined) {
            user.extra = {} as Extra;
        }
        user.extra[key] = value;
        this.$localStore.user = user;
    }

    get $$dark(): boolean {
        return this.$vuetify.theme.dark;
    }

    set $$dark(value: boolean) {
        const themeText = value ? 'Dark' : 'Light';
        console.debug('Change Dark: ' + themeText);

        this.$localStore.dark = value;
        this.$vuetify.theme.dark = value;
        this.updateExtra('dark', value);
    }

    get $$lang(): string {
        return this.$i18n.locale;
    }

    set $$lang(value: string) {
        console.debug('Change Lang: ' + value);

        this.$localStore.lang = value;
        this.$i18n.locale = value;
        this.$vuetify.lang.current = value;
        this.updateExtra('lang', value);
    }

    get $$origin(): string {
        return this.$api2.origin;
    }

    set $$origin(value: string) {
        console.debug('Change API Origin: ' + value);

        this.$localStore.origin = value;
        this.$api.setUrl(value);
        this.$api2.origin = value;
    }
}
