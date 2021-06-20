<template>
  <div :style="outline ? 'border: 1px solid' : ''">
    <template v-if="!showProjectMaker">
      <v-toolbar
        height="50"
        class="elevation-1"
        :color="
          $vuetify.theme.dark
            ? 'rgb(10, 10, 10)'
            : 'rgb(245, 245, 245)'
        "
      >
        <span class="titleFont">
          <strong>{{ title ? title : $t("project_list") }}</strong>
        </span>
        <!--<v-icon class="addMember" :title="$t('add')" v-if="level <= 0" @click="openProjectMaker">add</v-icon>-->
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
            v-model="searchProject"
          />
          <v-icon class="searchIcon">search</v-icon>
        </div>
        <v-btn
          small
          :title="$t('add')"
          v-if="level <= 0"
          @click="openProjectMaker"
          color="info"
          style="margin-left: 10px;"
          >{{ $t("create_project.new_project") }}</v-btn
        >
      </v-toolbar>
      <v-divider></v-divider>
      <v-data-table
        v-if="projectList.length !== 0"
        hide-default-footer
        :headers="headers"
        :items="projectList"
        :search="searchProject"
        :items-per-page="10"
        :page.sync="page"
        :mobile-breakpoint="1055"
        @page-count="pageCount = $event"
        :style="this.$backgroundColor()"
      >
        <template v-slot:item.icon="{ item }">
          <v-avatar :color="$util.makeColor()" size="32">
            <span class="headline projectAvatar" @click="selectProject(item)">{{
              item.name.substring(0, 1).toUpperCase()
            }}</span>
          </v-avatar>
        </template>
        <template v-slot:item.name="{ item }">
          <span
            class="projectNaming"
            @click="selectProject(item)"
            :title="item.name"
            >{{ item.name }}</span
          >
        </template>
        <template v-slot:item.private="{ item }">
          <v-icon
            size="18"
            :title="item.private ? $t('private') : $t('public')"
            >{{ item.private ? "fas fa-lock" : "fas fa-lock-open" }}</v-icon
          >
        </template>
        <template v-slot:item.edit="{ item }">
          <v-icon
            v-if="showPrivate && showDescription"
            class="editButton"
            size="20"
            @click="openEditor(item)"
            :title="$t('edit')"
            >edit</v-icon
          >
          <v-icon
            v-else
            class="editButton"
            size="20"
            @click="openEditor(item)"
            :title="$t('information')"
            >fas fa-info-circle</v-icon
          >
        </template>
        <template v-slot:item.delete="{ item }">
          <v-icon
            class="deleteButton"
            size="20"
            @click="openDeleteChecker(item)"
            :title="$t('delete')"
            :disabled="item.auth < 100"
            >delete</v-icon
          >
        </template>
        <template v-slot:footer>
          <div
            :style="
              $vuetify.theme.dark
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
      <v-container fluid grid-list-lg>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card style="height: 100%;">
              <v-card-title class="headline">
                {{ $t("create_project.new_project") }}
              </v-card-title>
              <v-divider></v-divider>
              <v-container fluid>
                <v-layout row wrap>
                  <v-flex xs3>
                    <v-card style="height: 100%;">
                      <pre>{{ $t("create_project.descriptions") }}</pre>
                      <br />
                      <h3>{{ "[ " + $t("how_to") + " ]" }}</h3>
                      <pre>{{ $t("create_project.how_to") }}</pre>
                    </v-card>
                  </v-flex>
                  <v-flex xs9>
                    <af-project-maker
                      v-if="showProjectMaker"
                      :useTitle="false"
                      @close="onProjectMakerClose"
                      @success="onProjectMakerSuccess"
                      @error="onProjectMakerError"
                      :cancel-text="'back'"
                      :useSelection="showPrivate && showDescription"
                    ></af-project-maker>
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
      <v-btn text icon @click="alert = false">
        <v-icon>close</v-icon>
      </v-btn>
    </v-snackbar>

    <v-dialog
      v-model="showEditor"
      max-width="450px"
      :dark="$vuetify.theme.dark"
    >
      <v-card v-if="showEditor">
        <v-card-title>
          <span class="headline">{{ $t("project_edit") }}</span>
          <v-spacer></v-spacer>
          <v-btn
            v-if="showPrivate && showDescription && showAction"
            ref="privateButton"
            small
            icon
            :color="
              editProjectProp.private
                ? 'rgb(216, 92, 45)'
                : 'rgb(108, 195, 120)'
            "
            class="privateButton"
            @click.stop="editProjectProp.private = !editProjectProp.private"
            ><v-icon size="20">{{
              editProjectProp.private ? "fas fa-lock" : "fas fa-lock-open"
            }}</v-icon></v-btn
          >
          <v-icon
            v-else-if="showPrivate"
            size="20"
            :color="
              editProjectProp.private
                ? 'rgb(216, 92, 45)'
                : 'rgb(108, 195, 120)'
            "
            :title="editProjectProp.private ? $t('private') : $t('public')"
            >{{
              editProjectProp.private ? "fas fa-lock" : "fas fa-lock-open"
            }}</v-icon
          >
        </v-card-title>
        <v-card-subtitle style="padding-bottom: 5px; font-weight: bold;">
          <div class="subInfo-projectname">
            <span>{{ editorTitle }}</span>
          </div>
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-text>
          <v-container grid-list-xs style="padding-bottom: 0;">
            <div class="subInfo">
              <span>{{ $t("created_time") }}&nbsp;:&nbsp;</span>
              <span>{{ editProjectProp.createdAt }}</span>
            </div>
            <div class="subInfo">
              <span>{{ $t("last_login") }}&nbsp;:&nbsp;</span>
              <span>{{ editProjectProp.modifiedAt }}</span>
            </div>
            <v-container v-if="showDescription" grid-list-md>
              <v-layout row wrap>
                <v-flex xs12>
                  <div class="editDescription">
                    <v-textarea
                      v-model="editProjectProp.description"
                      :readonly="
                        !(showPrivate && showDescription && showAction)
                      "
                      :label="$t('description')"
                      hide-details
                      outlined
                    ></v-textarea>
                  </div>
                </v-flex>
              </v-layout>
            </v-container>
          </v-container>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <template v-if="!(showPrivate && showDescription && showAction)">
            <v-spacer></v-spacer>
            <v-btn text @click="closeEditor">{{ $t("close") }}</v-btn>
          </template>
          <template v-else>
            <v-btn text @click="closeEditor">{{ $t("close") }}</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="rgb(108, 195, 120)"
              text
              @click="saveEditor"
              :loading="editSignal"
              >{{ $t("edit") }}</v-btn
            >
          </template>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="showDeleteChecker"
      max-width="450"
      :dark="$vuetify.theme.dark"
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
            <b>{{ "[ " + deleteProjectName + " ] " }}</b>
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
            @click="onDeleteProject"
            :loading="deleteSignal"
            >{{ $t("delete") }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import afProjectMaker from "@/components/Form/afProjectMaker.vue";
import { Observable } from "rxjs";
export default {
  name: "aProjectTable",
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
      default: true,
    },
    showPrivate: {
      type: Boolean,
      default: false,
    },
    showAction: {
      type: Boolean,
      default: true,
    },
    showDescription: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    afProjectMaker,
  },
  data() {
    return {
      myPermission: "admin",

      // signal.
      getSignal: false, // Get project list signal.
      editSignal: false, // Edit project signal.
      deleteSignal: false, // Delete project signal.

      // table data.
      headers: [
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
          text: this.$t("project_name"),
          align: "center",
          sortable: false,
          value: "name",
        },
        {
          text: this.$t("created_time"),
          align: "center",
          sortable: false,
          value: "createdAt",
        },
        {
          text: this.$t("modified_time"),
          align: "center",
          sortable: false,
          value: "modifiedAt",
        },
        {
          text: this.$t("public_and_private"),
          align: "center",
          sortable: false,
          value: "private",
        },
        {
          // text: this.$t("edit"),
          text: this.$t("information"),
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
      searchProject: "",
      projectList: [],
      page: 1,
      pageCount: 0,

      // messages.
      noDataMessage: "no_search_data",
      loadingMessage: "loading_data",
      errorMessage: "no_data_table",
      deleteMessage: "dialog_message.project_delete",

      // alert.
      alert: false,
      alertColor: "",
      alertMessage: "",
      alertColors: {
        success: "rgb(108, 195, 120)",
        error: "rgb(216, 92, 45)",
      },
      alertMessages: {
        edit: {
          success: this.$t("projects.edit_success"),
          error: this.$t("projects.edit_failed"),
        },
        delete: {
          success: this.$t("projects.delete_success"),
          error: this.$t("projects.delete_failed"),
        },
        list: {
          success: this.$t("projects.get_list_success"),
          error: this.$t("projects.get_list_failed"),
        },
        add: {
          success: this.$t("projects.add_success"),
          error: this.$t("projects.add_failed"),
        },
      },

      // Editor dialog.
      showEditor: false,
      editorTitle: "",
      editProjectProp: {
        name: "",
        createdAt: "",
        modifiedAt: "",
      },
      initProjectProp: {
        name: "",
        createdAt: "",
        modifiedAt: "",
      },

      // Delete Check dialog.
      showDeleteChecker: false,
      deleteProjectName: "",

      // New project dialog.
      showProjectMaker: false,
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
        this.projectList = [];
      }
    },
  },
  methods: {
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
     * Open project make dialog.
     * @public
     */
    openProjectMaker: function() {
      this.showProjectMaker = true;
    },

    /**
     * Close project make dialog.
     * @public
     */
    onProjectMakerClose: function() {
      this.showProjectMaker = false;
    },

    /**
     * Project make success event.
     * @public
     */
    onProjectMakerSuccess: function() {
      this.showAlert(true, "add");
      this.onProjectMakerClose();
      this.getSignal = true;
    },

    /**
     * Project make Failed event.
     * @public
     */
    onProjectMakerError: function() {
      this.showAlert(false, "add");
      this.onProjectMakerClose();
    },

    /**
     * Open project editor dialog.
     * @public
     */
    openEditor: function(project) {
      this.editorTitle = project.name;
      this.editProjectProp = Object.assign({}, project);
      this.showEditor = true;
    },

    /**
     * Close project editor dialog.
     * @public
     */
    closeEditor: function() {
      this.showEditor = false;
      this.$nextTick().then(() => {
        this.editProjectProp = Object.assign({}, this.initProjectProp);
        this.editorTitle = "";
      });
    },

    /**
     * Send edited project data.
     * @public
     */
    saveEditor: function() {
      this.editSignal = true;
    },

    /**
     * Enter project. (Select project)
     * @public
     * @param {object} - project data.
     */
    selectProject: function(project) {
      // session select project = project.name.
      // router goto project main.
      this.$debug(
        this.$options.name,
        "selectProject",
        "Project:",
        project.name
      );
      this.$store.commit("project/setSelectProject", { name: project.name });
      this.$store.commit("project/setProjectAuth", { auth: project.auth });
      this.$router.push(this.$page.project);
    },

    /**
     * Open user delete checker dialog.
     * @public
     * @param {object} - User information data.
     */
    openDeleteChecker: function(projectInfo) {
      this.deleteProjectName = projectInfo.name;
      this.showDeleteChecker = true;
    },

    /**
     * Close Delete check dialog.
     * @public
     */
    closeDeleteCheck: function() {
      this.showDeleteChecker = false;
      this.$nextTick().then(() => {
        this.deleteProjectName = "";
      });
    },

    /**
     * Send will be delete user data for delete and close delete check dialog.
     * @public
     */
    onDeleteProject: function() {
      this.deleteSignal = true;
    },
  },
  created() {
    if (!this.showIndex) {
      var find;
      for (var i = 0; i < this.headers.length; ++i) {
        if (this.headers[i].value === "index") {
          find = i;
        }
      }
      this.headers.splice(find, 1);
      this.headers = [...this.headers];
    }
    if (!this.showIcon) {
      var find;
      for (var i = 0; i < this.headers.length; ++i) {
        if (this.headers[i].value === "icon") {
          find = i;
        }
      }
      this.headers.splice(find, 1);
      this.headers = [...this.headers];
    }
    if (!this.showCreatedAt) {
      var find;
      for (var i = 0; i < this.headers.length; ++i) {
        if (this.headers[i].value === "createdAt") {
          find = i;
        }
      }
      this.headers.splice(find, 1);
      this.headers = [...this.headers];
    }
    if (!this.showModifiedAt) {
      var find;
      for (var i = 0; i < this.headers.length; ++i) {
        if (this.headers[i].value === "modifiedAt") {
          find = i;
        }
      }
      this.headers.splice(find, 1);
      this.headers = [...this.headers];
    }
    if (!this.showPrivate) {
      var find;
      for (var i = 0; i < this.headers.length; ++i) {
        if (this.headers[i].value === "private") {
          find = i;
        }
      }
      this.headers.splice(find, 1);
      this.headers = [...this.headers];
    }
    if (!this.showAction) {
      var find;
      for (var i = 0; i < this.headers.length; ++i) {
        if (this.headers[i].value === "edit") {
          find = i;
        }
      }
      this.headers.splice(find, 2);
      this.headers = [...this.headers];
    }
    if (this.showAction && this.showPrivate && this.showDescription) {
      for (var i = 0; i < this.headers.length; ++i) {
        if (this.headers[i].value === "edit") {
          this.headers[i].text = this.$t("edit");
        }
      }
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
      getProjects: Observable.combineLatest($getSignal, (getSignal) => ({
        getSignal,
      })).flatMap(({ getSignal }) =>
        this.$api
          .getProjects(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"]
          )
          .do((res) => {
            this.showAlert(true, "list");
            this.projectList = res.obj;

            // set temp auth
            for (var i = 0; i < this.projectList.length; i++) {
              if (i == 0) {
                this.projectList[i].auth = 10;
              } else if (i == 1) {
                this.projectList[i].auth = 80;
              } else {
                this.projectList[i].auth = 100;
              }
            }
          })
          .catch((error) => {
            this.showAlert(false, "list");
            this.$error(
              this.$options.name,
              "subscriptions::getProjects",
              error
            );

            // test.
            // this.projectList = require("./test/projectlist.json")["obj"];
            return Observable.of(null);
          })
          .do(() => {
            this.getSignal = false;
          })
      ),
      deleteProject: Observable.combineLatest(
        $deleteSignal,
        (deleteSignal) => ({ deleteSignal })
      ).flatMap(({ deleteSignal }) =>
        this.$api
          .rmProject(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.deleteProjectName
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
            this.$error(this.$options.name, "subscriptions::rmProject", error);
            return Observable.of(null);
          })
          .do(() => {
            this.deleteSignal = false;
          })
      ),
      editProject: Observable.combineLatest($editSignal, (editSignal) => ({
        editSignal,
      })).flatMap(({ editSignal }) =>
        this.$api
          .editProject(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            { name: this.editProjectProp.name }
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
.addMember {
  /* border: 1px solid; */
  border-radius: 75px;
  margin-left: 15px;
  margin-right: 15px;
}
.editDescription {
  width: 100%;
  display: inline-block;
  position: relative;
}
.editDescription--icon {
  margin: 0;
  padding: 0;
  position: absolute;
  top: 2px;
  right: 2px;
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
.projectAvatar {
  font-weight: bold;
}
.projectAvatar:hover {
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
.editButton {
  border-radius: 5px;
  padding: 2px;
  box-shadow: 1px 1px black !important;
}
.editButton:hover {
  color: rgb(108, 195, 120);
  background-color: rgba(125, 125, 125, 0.5);
  box-shadow: 1px 1px black !important;
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
.subInfo-projectname {
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
