<template>
  <div :style="outline ? 'border: 1px solid' : ''">
    <template v-if="!openSignup">
      <v-toolbar
        height="50"
        class="elevation-1"
        :color="
          this.$vuetify.theme.dark ? 'rgb(10, 10, 10)' : 'rgb(245, 245, 245)'
        "
      >
        <span class="titleFont"
          ><strong>{{ title ? title : $t("user_list") }}</strong></span
        >
        <!--<v-icon class="addMember" @click="openSignupDialog" :title="$t('add')" v-if="level <= 0">add</v-icon>-->
        <v-spacer></v-spacer>
        <!-- <v-btn v-if="!getSignal" small @click.stop="getSignal = !getSignal" class="elevation-3" style="border-radius: 5px; margin-right: 10px;">{{ $t('refresh') }}</v-btn> -->
        <v-icon
          v-if="!getSignal"
          @click.stop="getSignal = !getSignal"
          class="elevation-3"
          style="border-radius: 5px; margin-right: 10px;"
          >refresh</v-icon
        >
        <div class="searchZone">
          <input
            class="searchInput"
            type="text"
            :placeholder="$t('search')"
            v-model="searchUser"
          />
          <v-icon class="searchIcon">search</v-icon>
        </div>
        <v-btn
          small
          @click="openSignupDialog"
          color="info"
          :title="$t('add')"
          v-if="level <= 0"
          style="margin-left: 10px;"
          >{{ $t("sign_up") }}</v-btn
        >
      </v-toolbar>
      <v-divider></v-divider>
      <v-data-table
        v-if="userlist.length !== 0"
        hide-default-footer
        :headers="headers"
        :items="userlist"
        :loading="deleteSignal"
        :search="searchUser"
        :items-per-page="10"
        :page.sync="page"
        :mobile-breakpoint="1055"
        @page-count="pageCount = $event"
      >
        <template v-slot:item.profile>
          <v-icon>far fa-user-circle</v-icon>
        </template>
        <template v-slot:item.id="{ item }">
          <span :title="item.id">{{ item.id }}</span
          ><v-chip
            v-if="item.id === myID"
            small
            color="info"
            class="chipStyle"
            >{{ $t("its_me") }}</v-chip
          >
        </template>
        <template v-slot:item.email="{ item }">
          <span :title="item.email">{{ item.email }}</span>
        </template>
        <template v-slot:item.telephone="{ item }">
          <span :title="item.telephone">{{ item.telephone }}</span>
        </template>
        <template v-slot:item.lastLogin="{ item }">
          <span :title="item.lastLogin">{{ item.lastLogin }}</span>
        </template>
        <template v-slot:item.createdAt="{ item }">
          <span :title="item.createdAt">{{ item.createdAt }}</span>
        </template>
        <template v-slot:item.edit="{ item }">
          <v-icon
            class="editButton"
            size="20"
            @click="openEditor(item)"
            :title="$t('edit')"
            >edit</v-icon
          >
        </template>
        <template v-slot:item.delete="{ item }">
          <v-icon
            class="deleteButton"
            :disabled="item.id === myID"
            size="20"
            @click="openDeleteChecker(item)"
            :title="$t('delete')"
            >delete</v-icon
          >
        </template>
        <template v-slot:footer>
          <div
            :style="
              this.$vuetify.theme.dark
                ? 'background-color: rgb(10, 10, 10)'
                : 'background-color: rgb(245, 245, 245)'
            "
          >
            <v-pagination
              v-model="page"
              :length="pageCount"
              :total-visible="7"
            ></v-pagination>
          </div>
        </template>
        <template v-slot:no-data>
          <v-alert
            :value="true"
            color="warning"
            outlined
            class="alertStyle text-center"
          >
            <v-icon class="alertIcon--error" color="warning">warning</v-icon
            >{{ noDataMessage }}
          </v-alert>
        </template>
        <template v-slot:no-results>
          <v-alert
            :value="true"
            color="warning"
            outlined
            class="alertStyle text-center"
          >
            <v-icon class="alertIcon--error" color="warning">warning</v-icon
            >{{ noDataMessage }}
          </v-alert>
        </template>
      </v-data-table>
      <div v-else>
        <v-alert
          v-if="getSignal"
          :value="true"
          color="info"
          outlined
          class="alertStyle text-center"
        >
          <v-icon class="alertIcon" color="info">fas fa-hourglass-start</v-icon
          >{{ loadingMessage }}
        </v-alert>
        <v-alert
          v-else
          :value="true"
          color="grey"
          outlined
          class="alertStyle text-center"
        >
          <v-icon class="alertIcon--error" color="grey">error</v-icon
          >{{ errorMessage }}
        </v-alert>
      </div>
    </template>

    <template v-else>
      <v-container fluid grid-list-lg>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card style="height: 100%;">
              <v-card-title class="headline">
                {{ $t("sign_up") }}
              </v-card-title>
              <v-divider></v-divider>
              <v-container fluid>
                <v-layout row wrap>
                  <v-flex xs3>
                    <v-card style="height: 100%;">
                      <pre>{{ $t("signup.descriptions") }}</pre>
                      <br />
                      <h3>{{ "[ " + $t("how_to") + " ]" }}</h3>
                      <pre>{{ $t("signup.how_to") }}</pre>
                    </v-card>
                  </v-flex>
                  <v-flex xs9>
                    <signup
                      v-if="openSignup"
                      ref="signup"
                      :useTitle="false"
                      :cancel-text="'back'"
                      @close="onSignupClose"
                      @success="onSignupSuccess"
                      @signupError="onSignupError"
                    ></signup>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </template>

    <v-snackbar v-model="alert" :timeout="5000" bottom right absolute>
      <span :style="'color: ' + alertColor">{{ alertMessage }}</span>
      <v-btn text icon @click="alert = false"><v-icon>close</v-icon></v-btn>
    </v-snackbar>

    <v-dialog
      v-model="showEditor"
      max-width="450px"
      :dark="this.$vuetify.theme.dark"
    >
      <v-card>
        <v-card-title>
          <span class="headline">{{ $t("user_edit") }}</span>
          <v-spacer></v-spacer>
          <div
            class="status-circle"
            :style="
              editUserProps.active
                ? 'background-color: greenyellow'
                : 'background-color: rgb(216, 92, 45)'
            "
          ></div>
        </v-card-title>
        <v-card-subtitle style="padding-bottom: 0;">
          <div class="subInfo-username">
            <span>{{ editUserProps.id }}</span>
          </div>
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-text>
          <v-container fluid grid-list-xs>
            <div class="subInfo">
              <span>{{ $t("created_time") }}&nbsp;:&nbsp;</span
              ><span>{{ editUserProps.createdAt }}</span>
            </div>
            <div class="subInfo">
              <span>{{ $t("last_login") }}&nbsp;:&nbsp;</span
              ><span>{{ editUserProps.lastLogin }}</span>
            </div>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12>
                  <v-text-field
                    v-model="editUserProps.email"
                    :label="$t('email')"
                    :rules="[rules.email]"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="editUserProps.telephone"
                    :label="$t('phone_number')"
                    mask="(###) #### - ####"
                  ></v-text-field>
                </v-flex>
                <!-- <v-flex xs12>
                    <v-select
                      :label="$t('permission')"
                      :items="permissions"
                      :value="$t(editUserProps.permission)"
                      @change="onChangePermission($event)"
                    ></v-select>
                  </v-flex> -->
              </v-layout>
            </v-container>
          </v-container>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn text @click="closeEditor">{{ $t("cancel") }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="rgb(108, 195, 120)"
            text
            @click="saveEditor"
            :loading="editSignal"
            >{{ $t("edit") }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="showDeleteChecker"
      max-width="450"
      :dark="this.$vuetify.theme.dark"
    >
      <v-card outlined>
        <v-card-title class="text-center" style="padding: 0px;">
          <v-alert
            :value="true"
            color="warning"
            tile
            dense
            text
            style="margin: 0px; width: 100%; border-radius: 4px 0px 0px 0px;"
            border="left"
          >
            <v-icon color="warning">warning</v-icon>&nbsp;&nbsp;&nbsp;<span>{{
              $t("warning")
            }}</span>
          </v-alert>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-2">
          <span class="focusUsername"
            ><b>{{ "[ " + deleteUsername + " ] " }}</b></span
          ><span>{{ deleteMessage }}</span>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn text @click="closeDeleteCheck">{{ $t("cancel") }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="rgb(216, 92, 45)"
            text
            @click="onDeleteUser"
            :loading="deleteSignal"
            >{{ $t("ok") }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { Observable } from "rxjs";
import Signup from "@/components/Form/afSignupForm.vue";
export default {
  name: "aUserTable",
  props: {
    /**
     * List title.
     */
    title: {
      type: String,
      default: undefined,
    },
    /**
     * Outline style.
     */
    outline: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    Signup,
  },
  data() {
    return {
      // open signup dialog
      openSignup: false,

      // Signal(Req to api).
      getSignal: false,
      editSignal: false,
      deleteSignal: false,
      // messages.
      noDataMessage: this.$t("no_search_data"),
      loadingMessage: this.$t("loading_data"),
      errorMessage: this.$t("no_data_table"),
      deleteMessage: this.$t("dialog_message.user_delete"),
      // Table data.
      searchUser: "",
      page: 1,
      pageCount: 0,
      headers: [
        {
          text: " ",
          align: "center",
          sortable: false,
          value: "profile",
        },
        {
          text: this.$t("user_name"),
          align: "center",
          sortable: false,
          value: "id",
        },
        {
          text: this.$t("email"),
          align: "center",
          sortable: false,
          value: "email",
        },
        {
          text: this.$t("telephone"),
          align: "center",
          sortable: false,
          value: "telephone",
        },
        {
          text: this.$t("last_login"),
          align: "center",
          sortable: false,
          value: "lastLogin",
        },
        {
          text: this.$t("created_time"),
          align: "center",
          sortable: false,
          value: "createdAt",
        },
        {
          text: this.$t("edit"),
          align: "center",
          sortable: false,
          value: "edit",
        },
        {
          text: this.$t("delete"),
          align: "center",
          sortable: false,
          value: "delete",
        },
      ],
      userlist: [],
      // edit dialog data.
      showEditor: false,
      permissions: [this.$t("admin"), this.$t("guest")],
      rules: {
        email: (value) => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return (
            pattern.test(value) ||
            this.$t("join_error_message.email_format_error")
          );
        },
      },
      editUserProps: {
        username: "",
        permission: "",
        created_time: "",
        last_login: "",
        active: false,
        email: "",
        telephone: "",
      },
      initUserProps: {
        username: "",
        permission: "",
        created_time: "",
        last_login: "",
        active: false,
        email: "",
        telephone: "",
      },
      // delete check dialog data.
      showDeleteChecker: false,
      deleteUsername: "",

      alert: false,
      alertColor: "",
      alertMessage: "",
      alertColors: {
        success: "rgb(108, 195, 120)",
        error: "rgb(216, 92, 45)",
      },
      alertMessages: {
        edit: {
          success: this.$t("member_edit_success"),
          error: this.$t("member_edit_failed"),
        },
        delete: {
          success: this.$t("member_delete_success"),
          error: this.$t("member_delete_failed"),
        },
        list: {
          success: this.$t("get_member_list_success"),
          error: this.$t("get_member_list_failed"),
        },
        add: {
          success: this.$t("member_add_success"),
          error: this.$t("member_add_failed"),
        },
      },
    };
  },
  computed: {
    // Caculrate page length.
    level() {
      if (this.myPermission === "admin") {
        return 0; // admin level.
      } else {
        return 5; // guest level.
      }
    },
    myID() {
      return this.$store.getters["user/getUserID"];
    },
    myPermission() {
      return "admin";
    },
  },
  watch: {
    getSignal() {
      if (this.getSignal) {
        // Initialize userlist.
        this.userlist = [];
      }
    },
  },
  methods: {
    /**
     * Open signup dialog (add memeber).
     * @public
     */
    openSignupDialog: function() {
      this.openSignup = true;
    },

    /**
     * Close signup dialog (close event).
     * @public
     */
    onSignupClose: function() {
      this.openSignup = false;
    },

    /**
     * Signup Success event.
     * @public
     */
    onSignupSuccess: function() {
      this.showAlert(true, "add");
      this.onSignupClose();
      this.getSignal = true;
    },

    /**
     * Signup Failed event.
     * @public
     */
    onSignupError: function() {
      this.showAlert(false, "add");
      this.onSignupClose();
    },

    /**
     * Show alert message
     * @public
     * @param {boolean} - Is success?
     * @param {string} - alert type [list, edit, delete]
     */
    showAlert: function(isSuccess, type) {
      var status = isSuccess ? "success" : "error";
      var type = type || "list";

      this.alert = true;
      this.$nextTick().then(() => {
        this.alertColor = this.alertColors[status];
        this.alertMessage = this.alertMessages[type][status];
      });
    },

    /**
     * Open user editor dialog.
     * @public
     * @param {object} - User information data.
     */
    openEditor: function(userInfo) {
      this.editUserProps = Object.assign({}, userInfo);
      this.showEditor = true;
    },

    /**
     * Close user editor dialog.
     * @public
     */
    closeEditor: function() {
      this.showEditor = false;
      this.$nextTick().then(() => {
        this.editUserProps = Object.assign({}, this.initUserProps);
      });
    },

    /**
     * Change value event.
     * @public
     * @param {string} - permission.
     */
    onChangePermission: function(permission) {
      var cvtOriginValue;
      if (permission === this.$t("admin")) {
        cvtOriginValue = "admin";
      } else {
        cvtOriginValue = "guest";
      }
      this.editUserProps.permission = cvtOriginValue;
    },
    /**
     * Send edited user data for save and close editor dialog.
     * @public
     */
    saveEditor: function() {
      this.editSignal = true;
    },

    /**
     * Open user delete checker dialog.
     * @public
     * @param {object} - User information data.
     */
    openDeleteChecker: function(userInfo) {
      this.deleteUsername = userInfo.id;
      this.showDeleteChecker = true;
    },

    /**
     * Close user delete checker dialog.
     * @public
     */
    closeDeleteCheck: function() {
      this.showDeleteChecker = false;
      this.$nextTick().then(() => {
        this.deleteUsername = "";
      });
    },

    /**
     * Send will be delete user data for delete and close delete check dialog.
     * @public
     */
    onDeleteUser: function() {
      this.deleteSignal = true;
    },
  },
  created() {},
  mounted() {
    // This component actived : Send get userlist from API.
    this.getSignal = true;
  },
  subscriptions() {
    const $getSignal = this.$watchAsObservable("getSignal", { immediate: true })
      .pluck("newValue")
      .filter((getSignal) => getSignal == true) // if signal is true.
      .debounceTime(1000);
    const $deleteSignal = this.$watchAsObservable("deleteSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((deleteSignal) => deleteSignal == true) // if signal is true.
      .debounceTime(1000);
    const $editSignal = this.$watchAsObservable("editSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((editSignal) => editSignal == true) // if signal is true.
      .debounceTime(1000);
    return {
      getUsers: Observable.combineLatest($getSignal, (getSignal) => ({
        getSignal,
      })).flatMap(({ getSignal }) =>
        this.$api
          .getMembersList(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"]
          )
          .do((res) => {
            this.showAlert(true, "list");
            this.$debug(
              this.$options.name,
              "subscriptions::getMembersList",
              "Response:",
              res
            );
            var list = res.obj;
            for (var index = 0; index < list.length; ++index) {
              list[index].active = true;
              var createdAtDateTime = this.$util.cvtTime(list[index].createdAt);
              list[index].createdAt = `${
                createdAtDateTime.year ? createdAtDateTime.year + "." : ""
              } ${
                createdAtDateTime.month ? createdAtDateTime.month + "." : ""
              } ${createdAtDateTime.day ? createdAtDateTime.day + "." : ""} ${
                createdAtDateTime.hour ? createdAtDateTime.hour + ":" : ""
              }${createdAtDateTime.min ? createdAtDateTime.min + ":" : ""}${
                createdAtDateTime.sec ? createdAtDateTime.sec : ""
              }`;
              var lastLoginDateTime = this.$util.cvtTime(list[index].lastLogin);
              list[index].lastLogin = `${
                lastLoginDateTime.year ? lastLoginDateTime.year + "." : ""
              } ${
                lastLoginDateTime.month ? lastLoginDateTime.month + "." : ""
              } ${lastLoginDateTime.day ? lastLoginDateTime.day + "." : ""} ${
                lastLoginDateTime.hour ? lastLoginDateTime.hour + ":" : ""
              }${lastLoginDateTime.min ? lastLoginDateTime.min + ":" : ""}${
                lastLoginDateTime.sec ? lastLoginDateTime.sec : ""
              }`;
              var modifiedAtDateTime = this.$util.cvtTime(
                list[index].modifiedAt
              );
              list[index].modifiedAt = `${
                modifiedAtDateTime.year ? modifiedAtDateTime.year + "." : ""
              } ${
                modifiedAtDateTime.month ? modifiedAtDateTime.month + "." : ""
              } ${modifiedAtDateTime.day ? modifiedAtDateTime.day + "." : ""} ${
                modifiedAtDateTime.hour ? modifiedAtDateTime.hour + ":" : ""
              }${modifiedAtDateTime.min ? modifiedAtDateTime.min + ":" : ""}${
                modifiedAtDateTime.sec ? modifiedAtDateTime.sec : ""
              }`;
              this.userlist.push(list[index]);
            }
            // Myname To place at the top.
            for (var index = 0; index < this.userlist.length; ++index) {
              if (this.userlist[index].id === this.myID) {
                var itsme = this.userlist.splice(index, 1)[0];
                this.userlist.unshift(itsme);
                this.userlist = [...this.userlist];
                break;
              }
            }
          })
          .catch((error) => {
            this.showAlert(false, "list");
            this.$error(
              this.$options.name,
              "subscriptions::getMembersList",
              error
            );
            /* // test.
            var list = require("./test/userlist.json")["obj"];
            for (var index = 0; index < list.length; ++index) {
              list[index].active = true;
              this.userlist.push(list[index]);
            }
            // Myname To place at the top.
            for (var index = 0; index < this.userlist.length; ++index) {
              if (this.userlist[index].id === this.myID) {
                var itsme = this.userlist.splice(index, 1)[0];
                this.userlist.unshift(itsme);
                this.userlist = [...this.userlist];
                break;
              }
            }
            */
            return Observable.of(null);
          })
          .do(() => {
            this.getSignal = false;
          })
      ),
      deleteUser: Observable.combineLatest($deleteSignal, (deleteSignal) => ({
        deleteSignal,
      })).flatMap(({ deleteSignal }) =>
        this.$api
          .rmMember(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            { id: this.deleteUsername }
          )
          .do((res) => {
            // success.
            this.showAlert(true, "delete");
            this.closeDeleteCheck();
            this.getSignal = true;
          })
          .catch((error) => {
            // failed.
            this.showAlert(false, "delete");
            this.$error(this.$options.name, "subscriptions::rmMember", error);
            return Observable.of(null);
          })
          .do(() => {
            this.deleteSignal = false;
          })
      ),
      editUser: Observable.combineLatest($editSignal, (editSignal) => ({
        editSignal,
      })).flatMap(({ editSignal }) =>
        this.$api
          .editMember(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            {
              id: this.editUserProps.id,
              password: this.editUserProps.password,
              email: this.editUserProps.email,
              telephone: this.editUserProps.telephone,
            }
          )
          .do((res) => {
            // success.
            this.showAlert(true, "edit");
            this.closeEditor();
            this.getSignal = true;
          })
          .catch((error) => {
            // failed.
            this.showAlert(false, "edit");
            this.$error(this.$options.name, "subscriptions::editMember", error);
            return Observable.of(null);
          })
          .do(() => {
            this.editSignal = false;
          })
      ),
    };
  },
};
</script>

<style scoped>
.titleStyle {
  margin: 0;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 10px;
  padding-right: 10px;
}
.titleFont {
  font-size: 22px;
}
.addMember {
  /* border: 1px solid; */
  border-radius: 75px;
  margin-left: 15px;
  margin-right: 15px;
}
.addMember:hover {
  background-color: rgba(125, 125, 125, 0.5);
}
.addMember:active {
  background-color: rgba(125, 125, 125, 0.8);
}
.status-circle {
  border-radius: 75px;
  width: 20px;
  height: 20px;
  animation: blink 2s infinite linear;
  -webkit-animation: blink 2s infinite linear;
}
.status-circle-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
.editButton {
  border-radius: 5px;
  padding: 2px;
}
.editButton:hover {
  color: rgb(108, 195, 120);
  background-color: rgba(125, 125, 125, 0.5);
  box-shadow: 1px 1px black !important;
}
.deleteButton {
  border-radius: 5px;
  padding: 2px;
}
.deleteButton:hover {
  color: rgb(216, 92, 45);
  background-color: rgba(125, 125, 125, 0.5);
  box-shadow: 1px 1px black !important;
}
.alertStyle {
  border-color: rgba(255, 255, 255, 0) !important;
  /* border-radius: 10px; */
}
.alertStyle--delete {
  width: 100%;
  padding: 5px;
  /* border: none !important; */
}
.alertIcon--error {
  width: 20px;
  height: 20px;
  margin-left: 5px;
  margin-right: 7px;
}
.alertIcon {
  width: 20px;
  height: fit-content;
  margin-left: 7px;
  margin-right: 7px;
  animation: rotation 3s infinite;
  -webkit-animation: rotation 3s infinite;
  -webkit-transform-origin: 0% 100% 0% 100%;
  -moz-transform-origin: 0% 100% 0% 100%;
  -ms-transform-origin: 0% 100% 0% 100%;
  -o-transform-origin: 0% 100% 0% 100%;
  transform-origin: 0% 100% 0% 100%;
}
.searchZone {
  display: inline-block;
  position: relative;
  width: 20%;
}
.searchInput {
  width: 100%;
  height: 35px;
  border: 2px solid;
  border-radius: 4px;
  padding-left: 5px;
  padding-right: 5px;
  outline: none;
}
.searchInput:focus {
  border-color: rgb(75, 85, 180);
}
.searchInput:focus + .searchIcon {
  color: rgb(75, 85, 180);
}
.searchIcon {
  margin: 0;
  padding: 0;
  position: absolute;
  top: 5px;
  right: 5px;
}
.header-text {
  font-size: 16px;
  font-weight: bold;
}
.chipStyle {
  /* height: 19px; */
  margin-left: 5px;
}
.footerStyle {
  background-color: rgba(20, 20, 20, 0.5);
}
.subInfo-username {
  font-size: 15px;
  color: grey;
}
.subInfo {
  font-size: 10px;
  color: grey;
}
.refreshButton {
  /* position: absolute; */
  /* right: 15px; */
  border-radius: 5px;
  box-shadow: 1px 1px black !important;
}
.no-drag {
  -ms-user-select: none;
  -moz-user-select: -moz-none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
.focusUsername {
  font-size: 19px;
}

pre {
  white-space: pre-line;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(359deg);
  }
}
@-webkit-keyframes rotation {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(359deg);
  }
}
@keyframes blink {
  0% {
    opacity: 0.5;
  }
  25% {
    opacity: 0.75;
  }
  50% {
    opacity: 1;
  }
  75% {
    opacity: 0.75;
  }
  100% {
    opacity: 0.5;
  }
}
@-webkit-keyframes blink {
  0% {
    -webkit-transform: opacity(0.5);
  }
  25% {
    -webkit-transform: opacity(0.75);
  }
  50% {
    -webkit-transform: opacity(1);
  }
  75% {
    -webkit-transform: opacity(0.75);
  }
  100% {
    -webkit-transform: opacity(0.5);
  }
}
</style>
