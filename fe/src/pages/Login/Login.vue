<template>
  <v-main class="no-select">
    <v-container fluid fill-height class="container">
      <v-layout align-center justify-center>
        <v-flex xs12 sm6 md4 lg4 xl4>
          <v-card>
            <v-toolbar>
              <v-spacer></v-spacer>
              <main-title></main-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-expand-transition hide-on-leave>
              <af-login-form v-if="initComplete"></af-login-form>
            </v-expand-transition>
            <v-fade-transition hide-on-leave>
              <v-card-text v-if="!initComplete">
                <v-loader
                  :serialize="false"
                  :loadList="initCheckLists"
                  @allComplete="initComplete = $event"
                  ref="loader"
                ></v-loader>
              </v-card-text>
            </v-fade-transition>
          </v-card>
        </v-flex>
      </v-layout>
      <v-btn
        icon
        class="settingButton"
        @click="openApiSettingDialog"
        :title="'API Configure'"
      >
        <v-icon>settings</v-icon>
      </v-btn>
    </v-container>

    <v-dialog
      v-model="openSetting"
      max-width="500px"
      scrollable
      transition="dialog-transition"
      :overlay="false"
      :dark="$vuetify.theme.dark"
    >
      <v-card outlined>
        <v-card-title>
          <span>API Configure</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-text-field
            dense
            outlined
            hide-details
            ref="apiUrl"
            label="API Address"
            v-model="api_url"
            clearable
            @keypress.enter.stop="onOk"
          ></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn @click="onCancel">{{ $t("cancel") }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn @click="onOk" :disabled="!ok_disabled">{{ $t("ok") }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-main>
</template>

<script>
import afLoginForm from "@/components/Form/afLoginForm";
import vLoader from "@/components/Progress/processProgress";
import MainTitle from "@/components/Text/MainTitle";

export default {
  name: "LoginPage",
  components: {
    "af-login-form": afLoginForm,
    "v-loader": vLoader,
    "main-title": MainTitle,
  },
  data() {
    return {
      initComplete: false,
      initCheckLists: [
        {
          name: "checking_init_api",
          i18n: true,
          func: () => {
            return new Promise((resolve, reject) => {
              this.$api
                .checkAdmin()
                .then((res) => {
                  if (res.data.status === "ERROR") {
                    this.$info(
                      this.$options.name,
                      "API::checkAdmin",
                      "Is not existed admin."
                    );
                    setTimeout(() => {
                      reject({
                        status: true,
                        message:
                          "&nbsp;" +
                          this.$t("is_not_existed_admin_go_to_signup_admin"),
                      });
                    }, 1000);
                  } else {
                    setTimeout(() => {
                      resolve(true);
                    }, 1000);
                  }
                })
                .catch((err) => {
                  setTimeout(() => {
                    reject({ status: false, message: err });
                  }, 1000);
                });
            });
          },
          complete: false,
          status: null,
          onError: (e) => {
            if (e.status) {
              setTimeout(() => {
                this.$router.push("/signupadmin");
              }, 3000);
            } else {
              this.$error("API", "checkAdmin", e);
            }
          },
        },
      ],
      onShift: false,
      onEnter: false,
      openSetting: false,
      api_url: "",
    };
  },
  methods: {
    openApiSettingDialog: function() {
      this.api_url = this.$api.getUrl();
      this.openSetting = true;
      this.$nextTick().then(() => {
        this.$refs.apiUrl.focus();
      });
    },
    onCancel: function() {
      this.openSetting = false;
    },
    onOk: function() {
      this.$api.setUrl(this.api_url);
      this.$localStore.commit("etc/setApiUrl", { url: this.api_url });
      this.openSetting = false;
      this.initComplete = false;
      this.$nextTick(() => {
        if (!this.$refs.loader) {
          return;
        }
        this.$refs.loader.allRetry();
      });
    },
  },
  computed: {
    ok_disabled() {
      if (this.api_url === "") {
        return false;
      } else if (!this.api_url) {
        return false;
      }
      return true;
    },
  },
  mounted() {
    this.$api.setUrl(this.$localStore.getters["etc/getApiUrl"]);
    this.$vuetify.lang.current = "ko";
  },
};
</script>

<style lang="scss" scoped>
@import "~@/styles/sass/user-select-none.scss";

.no-select {
  @include user-select-none;
}

.container {
  display: inline-block;
  /* background-color: whitesmoke; */
}

.md-app {
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.content-style {
  margin-top: 60px;
  margin-bottom: auto;
}

.settingButton {
  position: absolute;
  top: 15px;
  right: 15px;
}
</style>
