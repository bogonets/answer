import {Vue, Watch} from 'vue-property-decorator';

export default class VueI18n extends Vue {
    @Watch('$vuetify.lang.current')
    updateI18n(newVal: string) {
        this.$i18n.locale = newVal;
    }
}
