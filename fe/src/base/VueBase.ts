import { Vue, Watch } from 'vue-property-decorator';

export default class VueBase extends Vue {

    @Watch('$vuetify.lang.current')
    updateI18n(newVal: string, oldVal: string) {
        this.$i18n.locale = newVal;
    }
}
