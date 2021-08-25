import {Vue, Component} from 'vue-property-decorator';
import {RawLocation} from 'vue-router';
import {Dictionary} from "vue-router/types/router";

@Component
export default class Router extends Vue {
    moveToBack() {
        this.$router.back();
    }

    moveTo(name: string, params?: Dictionary<string>) {
        if (this.$router.currentRoute.name === name) {
            return;
        }

        const rawLocation = {
            name: name,
            params: params,
        } as RawLocation;

        console.log(`moveTo: ${rawLocation}`);
        console.dir(rawLocation);
        this.$router.push(rawLocation).catch((reason: any) => {
            if (reason.name !== 'NavigationDuplicated') {
                throw reason;
            }
        })
    }
}
