<template>
    <v-menu :dark="this.$vuetify.theme.dark" left offset-y open-on-hover>
        <template v-slot:activator="{ on }">
            <v-btn class="border-style" v-on="on" @click="onRenewal()">{{$t('renewal')}}</v-btn>
        </template>
    </v-menu>
</template>

<script>
import { Observable } from "rxjs";
export default {
    name: "acbLambdaTemplatesRenewal",
    data() {
        return {
            signal: false
        };
    },
    methods: {
        onRenewal: function() {
            this.signal = true;
        }
    },
    subscriptions() {
        const $signal = this.$watchAsObservable("signal", {
            immediate: true
        })
            .pluck("newValue")
            .filter(signal => signal == true);

        return {
            getLambdaTemplates: Observable.combineLatest($signal, signal => ({
                signal
            })).flatMap(({ signal }) =>
                this.$api
                    .getLambdaTemplates(
                        this.$store.getters["user/getAccessToken"]
                    )
                    .do(res => {
                        this.$templateStore.commit(
                            "setLambdaTemplates",
                            res.result.obj
                        );
                    })
                    .catch(err => {
                        this.$error(
                            this.name,
                            "subscriptions::getLambdaTemplates",
                            err
                        );
                    })
                    .do(() => {
                        this.signal = false;
                    })
            )
        };
    }
};
</script>

<style scoped>
.icon-margin {
    padding: 0px 0px 0px 0px;
    margin-right: 10px;
}
</style>