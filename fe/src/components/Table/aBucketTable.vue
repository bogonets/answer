<template>
  <div :style="outline ? 'border: 1px solid' : ''">
    <template v-if="!showBucketMaker">
      <v-toolbar
        height="50"
        class="elevation-1"
        :color="
          this.$vuetify.theme.dark
            ? 'rgb(10, 10, 10)'
            : 'rgb(245, 245, 245)'
        "
      >
        <slot name="title">
          <span class="titleFont">
            <strong>{{ title ? title : $t("buckets.bucket_list") }}</strong>
          </span>
        </slot>
        <slot name="options">
          <v-spacer></v-spacer>
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
              v-model="searchBucket"
            />
            <v-icon class="searchIcon">search</v-icon>
          </div>
          <v-btn
            small
            :title="$t('add')"
            v-if="level <= 0 && operator"
            @click="openBucketMaker"
            color="info"
            style="margin-left: 10px;"
            >{{ $t("buckets.new_bucket") }}</v-btn
          >
        </slot>
      </v-toolbar>
      <v-divider></v-divider>
      <v-data-table
        v-if="bucketList.length !== 0"
        hide-default-footer
        :headers="bucketHeaders"
        :items="bucketList"
        :search="searchBucket"
        :items-per-page="10"
        :page.sync="page"
        :mobile-breakpoint="1055"
        @page-count="pageCount = $event"
        item-key="name"
        :expanded.sync="expanded"
        :show-expand="showDescription"
        :single-expand="showDescription"
      >
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">{{ item.description }}</td>
        </template>
        <template v-slot:item.icon="{ item }">
          <v-icon v-if="item.icon">{{ item.icon }}</v-icon>
          <v-avatar v-else :color="$util.makeColor()" size="32">
            <span class="headline bucketAvatar" @click="selectBucket(item)">{{
              item.name.substring(0, 1).toUpperCase()
            }}</span>
          </v-avatar>
        </template>
        <template v-slot:item.name="{ item }">
          <span
            class="projectNaming"
            @click="selectBucket(item)"
            :title="item.name"
            >{{ item.name }}</span
          >
        </template>
        <template v-slot:item.delete="{ item }">
          <v-icon
            class="deleteButton"
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
            <v-icon class="alertIcon--error" color="warning">warning</v-icon>
            {{ $t(noDataMessage) }}
          </v-alert>
        </template>
        <template v-slot:no-results>
          <v-alert
            :value="true"
            color="warning"
            outlined
            class="alertStyle text-center"
          >
            <v-icon class="alertIcon--error" color="warning">warning</v-icon>
            {{ $t(noDataMessage) }}
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
          <v-icon class="alertIcon" color="info">fas fa-hourglass-start</v-icon>
          {{ $t(loadingMessage) }}
        </v-alert>
        <v-alert
          v-else
          :value="true"
          color="grey"
          outlined
          class="alertStyle text-center"
        >
          <v-icon class="alertIcon--error" color="grey">error</v-icon>
          {{ $t(errorMessage) }}
        </v-alert>
      </div>
    </template>

    <template v-else>
      <v-toolbar
        height="50"
        class="elevation-1"
        :color="
          this.$vuetify.theme.dark
            ? 'rgb(10, 10, 10)'
            : 'rgb(245, 245, 245)'
        "
      >
        <span class="titleFont">
          <strong>{{ title ? title : $t("buckets.new_bucket") }}</strong>
        </span>
      </v-toolbar>
      <v-card>
        <div style="width: 100%; height: 100%;">
          <v-layout row wrap fill-height pa-5>
            <v-flex xs3 class="pa-1">
              <v-sheet style="border: 1px solid; height: 100%;">
                <pre style="white-space: pre-line" class="pa-1">
New bucket description</pre
                >
              </v-sheet>
            </v-flex>
            <v-flex xs9 class="pa-1">
              <v-sheet style="height: 100%;">
                <v-text-field
                  :label="$t('name')"
                  dense
                  outlined
                  hide-details
                  :style="
                    showDescription
                      ? 'margin: 0px; margin-bottom: 10px;'
                      : 'margin: 0px;'
                  "
                  v-model="addBucketName"
                  tabindex="1"
                  @keypress.enter.stop="createBucket"
                  autofocus
                ></v-text-field>
                <v-textarea
                  v-if="showDescription"
                  :label="$t('description')"
                  dense
                  outlined
                  hide-details
                  v-model="addBucketDescription"
                >
                </v-textarea>
              </v-sheet>
            </v-flex>
          </v-layout>
        </div>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn text small @click="closeBucketMaker" tabindex="3">{{
            $t("back")
          }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            text
            small
            color="info"
            :loading="addSignal"
            @click="createBucket"
            tabindex="2"
            >{{ $t("add") }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </template>

    <v-snackbar v-model="alert" :timeout="5000" bottom right absolute>
      <span :style="'color: ' + alertColor">{{ alertMessage }}</span>
      <v-btn text icon @click="alert = false">
        <v-icon>close</v-icon>
      </v-btn>
    </v-snackbar>

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
            <v-icon color="warning">warning</v-icon>&nbsp;&nbsp;&nbsp;
            <span>{{ $t("warning") }}</span>
          </v-alert>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-2">
          <span class="focusUsername">
            <b>{{ "[ " + deleteBucketName + " ] " }}</b>
          </span>
          <span>{{ $t(deleteMessage) }}</span>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn text @click="closeDeleteCheck">{{ $t("cancel") }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="rgb(216, 92, 45)"
            text
            @click="onDeleteBucket"
            :loading="deleteSignal"
            >{{ $t("delete") }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { Observable } from "rxjs";
export default {
  name: "aBucketTable",
  props: {
    /**
     * Outline style
     */
    outline: {
      type: Boolean,
      default: false,
    },
    /**
     * List title.
     */
    title: {
      type: String,
      default: undefined,
    },
    showIndex: {
      type: Boolean,
      default: false,
    },
    showIcon: {
      type: Boolean,
      default: true,
    },
    showCreatedAt: {
      type: Boolean,
      default: true,
    },
    showModifiedAt: {
      type: Boolean,
      default: false,
    },
    showDelete: {
      type: Boolean,
      default: true,
    },
    showDescription: {
      type: Boolean,
      default: false,
    },
  },
  components: {},
  data() {
    return {
      myPermission: "admin",

      // signal.
      getSignal: false, // Get project list signal.
      addSignal: false,
      deleteSignal: false, // Delete project signal.

      // table data.
      bucketHeaders: [
        {
          text: " ",
          align: "center",
          sortable: true,
          value: "index",
        },
        {
          text: " ",
          align: "center",
          sortable: false,
          value: "icon",
        },
        {
          text: this.$t("buckets.bucket_name"),
          align: "center",
          sortable: false,
          value: "name",
        },
        {
          text: this.$t("created_time"),
          align: "center",
          sortable: false,
          value: "creationDate",
        },
        {
          text: this.$t("modified_time"),
          align: "center",
          sortable: false,
          value: "modifiedAt",
        },
        {
          text: this.$t("delete"),
          align: "center",
          sortable: false,
          value: "delete",
        },
        {
          text: "",
          value: "data-table-expand",
        },
      ],
      searchBucket: "",
      bucketList: [],
      expanded: [],
      page: 1,
      pageCount: 0,

      // messages.
      noDataMessage: "no_search_data",
      loadingMessage: "loading_data",
      errorMessage: "no_data_table",
      deleteMessage: "buckets.check_delete_bucket",

      // alert.
      alert: false,
      alertColor: "",
      alertMessage: "",
      alertColors: {
        success: "rgb(108, 195, 120)",
        error: "rgb(216, 92, 45)",
      },
      alertMessages: {
        delete: {
          success: this.$t("buckets.delete_success"),
          error: this.$t("buckets.delete_failed"),
        },
        deleteFailed: {
          success: this.$t("buckets.delete_success"),
          error: this.$t("buckets.delete_failed_is_not_empty"),
        },
        list: {
          success: this.$t("buckets.get_list_success"),
          error: this.$t("buckets.get_list_failed"),
        },
        add: {
          success: this.$t("buckets.add_success"),
          error: this.$t("buckets.add_failed"),
        },
        addFailed: {
          success: "",
          error: this.$t("buckets.add_failed_duplicated"),
        },
      },

      // Delete Check dialog.
      showDeleteChecker: false,
      deleteBucketName: "",

      // New bucket dialog.
      showBucketMaker: false,
      addBucketName: "",
      addBucketDescription: "",
      addBucketData: {},

      // Selection.
      selected_bucket: null,

      operator: Boolean,
    };
  },
  computed: {
    level() {
      if (this.myPermission === "admin") {
        return 0; // admin level.
      } else {
        return 5; // guest level.
      }
    },
  },
  watch: {
    getSignal() {
      if (this.getSignal) {
        // Initialize userlist.
        this.bucketList = [];
      }
    },
  },
  methods: {
    /**
     * Show alert message
     * @public
     * @param {boolean} - Is success?
     * @param {string} - alert type [list, delete]
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
     * Open project make dialog.
     * @public
     */
    openBucketMaker: function() {
      this.showBucketMaker = true;
    },

    /**
     * Close project make dialog.
     * @public
     */
    closeBucketMaker: function() {
      this.addBucketName = "";
      this.addBucketDescription = "";
      this.addBucketData = {};
      this.showBucketMaker = false;
    },

    /**
     * Send Create bucket data to API.
     * @public
     */
    createBucket: function() {
      this.addBucketData.name = this.addBucketName;
      if (this.showDescription) {
        this.addBucketData.description = this.addBucketDescription;
      }

      for (var bucket of this.bucketList) {
        if (this.addBucketData.name === bucket.name) {
          // duplicated bucket name.
          this.showAlert(false, "addFailed");
          this.$error(
            this.$options.name,
            "createBucket",
            "Duplicated bucket name."
          );
          return;
        }
      }
      this.addSignal = true;
    },

    /**
     * Project make success event.
     * @public
     */
    onBucketMakerSuccess: function() {
      this.showAlert(true, "add");
      this.onProjectMakerClose();
      this.getSignal = true;
    },

    /**
     * Project make Failed event.
     * @public
     */
    onBucketMakerError: function() {
      this.showAlert(false, "add");
      this.onProjectMakerClose();
    },

    /**
     * Enter Bucket. (Select bucket)
     * @public
     * @param {object} - project data.
     */
    selectBucket: function(bucket) {
      this.$debug(this.$options.name, "selectBucket", "Bucket:", bucket.name);
      this.selected_bucket = bucket.name;
      this.$emit("selectBucket", bucket);
    },

    /**
     * Open user delete checker dialog.
     * @public
     * @param {object} - User information data.
     */
    openDeleteChecker: function(bucketInfo) {
      this.deleteBucketName = bucketInfo.name;
      this.showDeleteChecker = true;
    },

    /**
     * Close Delete check dialog.
     * @public
     */
    closeDeleteCheck: function() {
      this.showDeleteChecker = false;
      this.$nextTick().then(() => {
        this.deleteBucketName = "";
      });
    },

    /**
     * Send will be delete user data for delete and close delete check dialog.
     * @public
     */
    onDeleteBucket: function() {
      this.deleteSignal = true;
    },
  },
  created() {
    this.operator = this.$store.getters["project/isOperator"];
    if (!this.showIndex) {
      var find;
      for (var i = 0; i < this.bucketHeaders.length; ++i) {
        if (this.bucketHeaders[i].value === "index") {
          find = i;
        }
      }
      this.bucketHeaders.splice(find, 1);
      this.bucketHeaders = [...this.bucketHeaders];
    }
    if (!this.showIcon) {
      var find;
      for (var i = 0; i < this.bucketHeaders.length; ++i) {
        if (this.bucketHeaders[i].value === "icon") {
          find = i;
        }
      }
      this.bucketHeaders.splice(find, 1);
      this.bucketHeaders = [...this.bucketHeaders];
    }
    if (!this.showCreatedAt) {
      var find;
      for (var i = 0; i < this.bucketHeaders.length; ++i) {
        if (this.bucketHeaders[i].value === "createdAt") {
          find = i;
        }
      }
      this.bucketHeaders.splice(find, 1);
      this.bucketHeaders = [...this.bucketHeaders];
    }
    if (!this.showModifiedAt) {
      var find;
      for (var i = 0; i < this.bucketHeaders.length; ++i) {
        if (this.bucketHeaders[i].value === "modifiedAt") {
          find = i;
        }
      }
      this.bucketHeaders.splice(find, 1);
      this.bucketHeaders = [...this.bucketHeaders];
    }
    if (!this.showDelete) {
      var find;
      for (var i = 0; i < this.bucketHeaders.length; ++i) {
        if (this.bucketHeaders[i].value === "delete") {
          find = i;
        }
      }
      this.bucketHeaders.splice(find, 1);
      this.bucketHeaders = [...this.bucketHeaders];
    }
    if (!this.showDescription) {
      var find;
      for (var i = 0; i < this.bucketHeaders.length; ++i) {
        if (this.bucketHeaders[i].value === "data-table-expand") {
          find = i;
        }
      }
      this.bucketHeaders.splice(find, 1);
      this.bucketHeaders = [...this.bucketHeaders];
    }
  },
  mounted() {
    this.$nextTick().then(() => {
      this.getSignal = true;
    });
  },
  subscriptions() {
    const $getSignal = this.$watchAsObservable("getSignal", { immediate: true })
      .pluck("newValue")
      .filter((getSignal) => getSignal == true) // if signal is true.
      .debounceTime(1000);
    const $addSignal = this.$watchAsObservable("addSignal", { immediate: true })
      .pluck("newValue")
      .filter((addSignal) => addSignal == true) // if signal is true.
      .debounceTime(1000);
    const $deleteSignal = this.$watchAsObservable("deleteSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((deleteSignal) => deleteSignal == true) // if signal is true.
      .debounceTime(1000);
    return {
      getBuckets: Observable.combineLatest($getSignal, (getSignal) => ({
        getSignal,
      })).flatMap(
        ({ getSignal }) =>
          this.$api
            .getBuckets(
              this.$store.getters["user/getAccessToken"],
              this.$store.getters["user/getRefreshToken"],
              this.$store.getters["project/getSelectProject"]
            )
            .do((res) => {
              this.showAlert(true, "list");
              this.$debug(
                this.$options.name,
                "subscriptions::getBuckets",
                "Response:",
                res
              );
              this.bucketList = res.result.obj;
              for (var bucket of this.bucketList) {
                var dateTime = this.$util.cvtTime(bucket.creationDate);
                bucket.creationDate = `${
                  dateTime.year ? dateTime.year + "." : ""
                } ${dateTime.month ? dateTime.month + "." : ""} ${
                  dateTime.day ? dateTime.day + "." : ""
                } ${dateTime.hour ? dateTime.hour + ":" : ""}${
                  dateTime.min ? dateTime.min + ":" : ""
                }${dateTime.sec ? dateTime.sec : ""}`;
              }
            })
            .catch((error) => {
              this.showAlert(false, "list");
              this.$error(
                this.$options.name,
                "subscriptions::getBuckets",
                error
              );
              return Observable.of(null);
            })
            .do(() => {
              this.getSignal = false;
            })
        // {
        //   this.bucketList = require("./test/bucketlist.json")["obj"];
        //   this.getSignal = false;
        // }
      ),
      addBucket: Observable.combineLatest($addSignal, (addSignal) => ({
        addSignal,
      })).flatMap(({ addSignal }) =>
        this.$api
          .createBucket(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.addBucketData.name
          )
          .do((res) => {
            if (res.status === "ERROR") {
              this.showAlert(false, "addFailed");
              this.$error(
                this.$options.name,
                "subscriptions::createBucket",
                res.detail
              );
              return Observable.of(null);
            }
            // success.
            this.showAlert(true, "add");
            this.$debug(
              this.$options.name,
              "subscriptions::createBucket",
              "Response:",
              res
            );
            this.closeBucketMaker();
            this.getSignal = true;
          })
          .catch((error) => {
            // failed.
            this.showAlert(false, "add");
            this.$error(
              this.$options.name,
              "subscriptions::createBucket",
              error
            );
            return Observable.of(null);
          })
          .do(() => {
            this.addSignal = false;
          })
      ),
      deleteBucket: Observable.combineLatest($deleteSignal, (deleteSignal) => ({
        deleteSignal,
      })).flatMap(({ deleteSignal }) =>
        this.$api
          .deleteBuckets(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.deleteBucketName
          )
          .do((res) => {
            // failed.
            if (res.status === "ERROR") {
              this.showAlert(false, "deleteFailed");
              this.closeDeleteCheck();
              this.$error(
                this.$options.name,
                "subscriptions::deleteBuckets",
                res.detail
              );
              return Observable.of(null);
            }
            // success.
            this.showAlert(true, "delete");
            this.$debug(
              this.$options.name,
              "subscriptions::deleteBuckets",
              "Response:",
              res
            );
            this.closeDeleteCheck();
            this.getSignal = true;
          })
          .catch((error) => {
            // failed.
            this.showAlert(false, "delete");
            this.$error(
              this.$options.name,
              "subscriptions::deleteBuckets",
              error
            );
            return Observable.of(null);
          })
          .do(() => {
            this.deleteSignal = false;
          })
      ),
    };
  },
};
</script>

<style scoped>
.addMember {
  /* border: 1px solid; */
  border-radius: 75px;
  margin-left: 15px;
  margin-right: 15px;
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
.bucketAvatar {
  font-weight: bold;
}
.bucketAvatar:hover {
  cursor: pointer;
  text-decoration: underline;
}
.projectNaming {
  font-weight: bold;
}
.projectNaming:hover {
  cursor: pointer;
  text-decoration: underline;
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
.focusUsername {
  font-size: 19px;
}
.privateButton {
  padding: 2px;
  box-shadow: 1px 1px black !important;
  animation: scaler 1s infinite;
  -webkit-animation: scaler 1s infinite;
  -webkit-transform-origin: 0% 100% 0% 100%;
  -moz-transform-origin: 0% 100% 0% 100%;
  -ms-transform-origin: 0% 100% 0% 100%;
  -o-transform-origin: 0% 100% 0% 100%;
  transform-origin: 0% 100% 0% 100%;
}
.deleteButton {
  border-radius: 5px;
  padding: 2px;
  box-shadow: 1px 1px black !important;
}
.deleteButton:hover {
  color: rgb(216, 92, 45);
  background-color: rgba(125, 125, 125, 0.5);
  box-shadow: 1px 1px black !important;
}
/* .v-data-table >>> th {
  font-size: 20px;
} */
.subInfo-bucketname {
  font-size: 15px;
  color: grey;
}
.subInfo {
  font-size: 10px;
  color: grey;
}

pre {
  white-space: pre-line;
}

/* Keyframes */
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

@keyframes scaler {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}
@-webkit-keyframes scaler {
  0% {
    -webkit-transform: scale(1);
  }
  50% {
    -webkit-transform: scale(1.1);
  }
  100% {
    -webkit-transform: scale(1);
  }
}
</style>
