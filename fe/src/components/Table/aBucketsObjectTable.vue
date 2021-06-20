<template>
  <div :style="outline ? 'border: 1px solid' : ''">
    <v-splitpanes class="default-theme splitPane">
      <v-pane :size="75" :min-size="55" class="pane">
        <div class="listZone" @dragover.prevent @drop.prevent="fileDrop">
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
                <strong>{{ title ? title : $t("objects.object_list") }}</strong>
              </span>
            </slot>
            <slot name="options">
              <slot name="options-prepand">
                <v-menu
                  v-if="!getSignal"
                  v-model="newFolder.show"
                  :nudge-width="250"
                  :close-on-content-click="false"
                  offset-x
                  right
                >
                  <template v-slot:activator="{ on }">
                    <v-btn small icon color="teal" v-on="on"
                      ><v-icon size="18">fas fa-folder-plus</v-icon></v-btn
                    >
                  </template>
                  <v-card>
                    <v-card-text>
                      <v-text-field
                        dense
                        outlined
                        type="text"
                        hide-details
                        class="ma-1"
                        :label="$t('objects.folder_name')"
                        @input="inputFolderName"
                        v-model="newFolder.name"
                      ></v-text-field>
                      <v-alert
                        v-model="newFolder.alert"
                        type="error"
                        class="ma-1"
                        dense
                        outlined
                        dismissible
                      >
                        {{ $t(newFolder.errorMsg) }}
                      </v-alert>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                      <v-btn small @click="closeNewFolderMenu">{{
                        $t("cancel")
                      }}</v-btn>
                      <v-spacer></v-spacer>
                      <v-btn small @click="createNewFolder">{{
                        $t("add")
                      }}</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-menu>
              </slot>
              <v-spacer></v-spacer>
              <slot name="options-append">
                <v-icon
                  v-if="!getSignal"
                  @click.stop="onRefreshObjectList"
                  class="elevation-3 refreshButton"
                  >refresh</v-icon
                >
                <div class="searchZone">
                  <input
                    class="searchInput"
                    type="text"
                    :placeholder="$t('search')"
                    v-model="searchObject"
                  />
                  <v-icon class="searchIcon">search</v-icon>
                </div>
                <v-btn
                  color="info"
                  small
                  @click="selectFile"
                  :title="$t('file_upload')"
                  class="uploadButton"
                  :loading="uploadSignal"
                >
                  <v-icon size="15" left>fas fa-upload</v-icon
                  >{{ "   " + $t("file_upload") }}
                </v-btn>
              </slot>
            </slot>
          </v-toolbar>
          <v-divider></v-divider>
          <v-data-table
            v-if="objectList.length !== 0"
            id="myTable"
            fixed-header
            hide-default-footer
            :headers="objectHeaders"
            :items="objectList"
            :search="searchObject"
            :items-per-page="14"
            :page.sync="page"
            @page-count="pageCount = $event"
          >
            <template v-slot:item.icon="{ item }">
              <v-icon
                v-if="item.icon"
                @click="selectObject(item)"
                :color="getIconColor(item)"
                >{{ item.icon }}</v-icon
              >
              <v-avatar v-else :color="$util.makeColor()" size="32">
                <span
                  class="headline bucketAvatar"
                  @click="selectObject(item)"
                  >{{ item.name.substring(0, 1).toUpperCase() }}</span
                >
              </v-avatar>
            </template>
            <template v-slot:item.objectName="{ item }">
              <span
                class="objectNaming"
                @click="selectObject(item)"
                :title="item.objectName"
                >{{ item.objectName }}</span
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
              <v-card-actions
                class="tableFooter"
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
                <v-spacer></v-spacer>
                <!-- <v-btn color="orange" small fab style="width: 25px; height: 25px;" @click="selectFile"><v-icon size="24">add</v-icon></v-btn> -->
              </v-card-actions>
            </template>
            <template v-slot:no-data>
              <v-alert
                :value="true"
                color="warning"
                outlined
                class="alertStyle text-center"
              >
                <v-icon class="alertIcon--error" color="warning"
                  >warning</v-icon
                >
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
                <v-icon class="alertIcon--error" color="warning"
                  >warning</v-icon
                >
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
              <v-icon class="alertIcon" color="info"
                >fas fa-hourglass-start</v-icon
              >
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
        </div>
      </v-pane>
      <v-pane :size="25" class="pane">
        <slot name="preview">
          <div class="previewZone">
            <v-container fluid grid-list-md fill-height>
              <v-layout row wrap fill-height justify-center>
                <v-flex
                  v-if="resource"
                  xs10
                  class="preview--content flex align-center"
                >
                  <template v-if="isImage(selected_object)">
                    <div class="text-center" style="height: 100%;">
                      <v-img
                        :src="resource"
                        @load="onImageLoad"
                        @error="onImageLoadError"
                        ref="resource"
                        class="preview--content__image"
                      ></v-img>
                      <v-btn
                        v-if="imageViewerOpener"
                        icon
                        small
                        :title="$t('zoom_in')"
                        @click="openImageViewer"
                        ><v-icon>zoom_in</v-icon></v-btn
                      >
                      <div v-else class="unknown--container">
                        <v-icon class="unknown--icon" size="50"
                          >fas fa-file</v-icon
                        >
                        <div class="unknown--text">
                          <span>{{ $t("objects.error_file") }}</span>
                        </div>
                      </div>
                    </div>
                  </template>
                  <a-json-field
                    v-else-if="isJson(selected_object)"
                    class="preview--content__json"
                    :json="resource"
                    :tabSize="2"
                    :readonly="true"
                    :resize="'none'"
                    outline
                    ref="resource"
                  ></a-json-field>
                  <a-textarea
                    v-else-if="isText(selected_object)"
                    ref="resource"
                    v-model="resource"
                    readonly
                    :resize="'none'"
                    class="preview--content__text"
                  ></a-textarea>
                  <template v-else-if="isPdf(selected_object)">
                    <div class="text-center" style="height: 100%;">
                      <div class="unknown--container">
                        <v-icon
                          class="unknown--icon"
                          size="50"
                          color="red lighten-1"
                          >fas fa-file-pdf</v-icon
                        >
                      </div>
                    </div>
                  </template>
                  <div
                    v-else
                    class="unknown--container text-center"
                    ref="resource"
                  >
                    <v-icon class="unknown--icon" size="50">fas fa-file</v-icon>
                    <div class="unknown--text">
                      <span>{{ $t("objects.unknown_file") }}</span>
                    </div>
                  </div>
                </v-flex>
                <v-flex v-else xs10 class="preview--content">
                  <div
                    v-if="selected_object"
                    class="unknown--container text-center"
                  >
                    <v-icon
                      v-if="getObjectSignal"
                      class="unknown--icon spinner"
                      size="50"
                      color="info"
                      >fas fa-spinner</v-icon
                    >
                    <div
                      v-else
                      class="unknown--container text-center"
                      ref="resource"
                    >
                      <v-icon class="unknown--icon" size="50"
                        >fas fa-file</v-icon
                      >
                      <div class="unknown--text">
                        <span>{{ $t("objects.error_file") }}</span>
                      </div>
                    </div>
                  </div>
                </v-flex>
                <v-footer
                  v-if="selected_object"
                  :padless="false"
                  height="200"
                  class="preview--footer"
                >
                  <v-card-text class="text-center">
                    <span class="preview--name">{{
                      selected_object.objectName
                    }}</span
                    ><br />
                    <span class="preview--size">{{ selected_object.size }}</span
                    ><br />
                    <span class="preview--modifiedAt">{{
                      selected_object.lastModified
                    }}</span
                    ><br />
                    <v-btn
                      small
                      fab
                      @click="objectDownload"
                      :title="$t('download')"
                      ><v-icon>fas fa-download</v-icon></v-btn
                    >
                  </v-card-text>
                </v-footer>
              </v-layout>
            </v-container>
          </div>
        </slot>
      </v-pane>
    </v-splitpanes>

    <v-snackbar v-model="alert" :timeout="5000" bottom right>
      <span :style="'color: ' + alertColor">{{ alertMessage }}</span>
      <v-btn text icon @click="alert = false">
        <v-icon>close</v-icon>
      </v-btn>
    </v-snackbar>

    <v-dialog v-model="imageViewer" fullscreen @keydown.esc="closeImageViewer">
      <template v-if="imageViewer">
        <div ref="viewerZone" class="imageViewer--content">
          <v-container fluid fill-height>
            <v-layout align-center justify-center>
              <img
                class="imageViewer--content__image"
                ref="viewerImage"
                :src="viewerSrc"
              />
            </v-layout>
          </v-container>
        </div>
        <div class="imageViewer--footer">
          <v-container fluid fill-height>
            <v-layout align-center justify-center>
              <v-btn icon @click="viewerZoomOut"
                ><v-icon size="20">fas fa-search-minus</v-icon></v-btn
              >
              <v-btn icon @click="viewerZoomIn"
                ><v-icon size="20">fas fa-search-plus</v-icon></v-btn
              >
            </v-layout>
          </v-container>
        </div>
        <v-btn
          absolute
          top
          right
          icon
          class="imageViewer--closer"
          @click="closeImageViewer"
          ><v-icon>close</v-icon></v-btn
        >
      </template>
    </v-dialog>

    <v-dialog
      v-model="showDeleteChecker"
      max-width="450"
      :dark="this.$vuetify.theme.dark"
    >
      <v-card outlined>
        <v-card-title class="text-center deleteChecker--title">
          <v-alert
            :value="true"
            class="deleteChecker--alert"
            color="warning"
            tile
            dense
            text
          >
            <v-icon color="warning">warning</v-icon>&nbsp;&nbsp;&nbsp;
            <span>{{ $t("warning") }}</span>
          </v-alert>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-2">
          <span class="focusUsername">
            <b>{{ "[ " + deleteObjectName + " ] " }}</b>
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
            @click="onDeleteObject"
            :loading="deleteSignal"
            >{{ $t("delete") }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
// import acvSimpleImageViewer from "@/components/Image/acvSimpleImageViewer.vue";
import { Observable } from "rxjs";
export default {
  name: "aObjectTable",
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
      default: false,
    },
    showModifiedAt: {
      type: Boolean,
      default: true,
    },
    showDelete: {
      type: Boolean,
      default: true,
    },
    parentBucket: {
      type: Object,
      default: undefined,
    },
  },
  components: {},
  data() {
    return {
      myPermission: "admin",

      // new folder data.
      newFolder: {
        show: false,
        alert: false,
        errorMsg: "objects.duplicated_folder_name",
        name: "",
      },

      // signal.
      getSignal: false, // Get object list signal.
      getObjectSignal: false, // Get object data signal.
      uploadSignal: false,
      deleteSignal: false, // Delete project signal.

      // table data.
      objectHeaders: [
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
          text: this.$t("objects.object_name"),
          align: "center",
          sortable: true,
          value: "objectName",
        },
        {
          text: this.$t("objects.size"),
          align: "center",
          sortable: true,
          value: "size",
        },
        {
          text: this.$t("created_time"),
          align: "center",
          sortable: true,
          value: "createdAt",
        },
        {
          text: this.$t("modified_time"),
          align: "center",
          sortable: true,
          value: "lastModified",
        },
        {
          text: this.$t("delete"),
          align: "center",
          sortable: false,
          value: "delete",
        },
      ],
      searchObject: "",
      objectList: [],
      page: 1,
      pageCount: 0,

      // messages.
      noDataMessage: "no_search_data",
      loadingMessage: "loading_data",
      errorMessage: "no_data_table",
      deleteMessage: "objects.check_delete_object",

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
          success: this.$t("objects.delete_success"),
          error: this.$t("objects.delete_failed"),
        },
        list: {
          success: this.$t("objects.get_list_success"),
          error: this.$t("objects.get_list_failed"),
        },
        add: {
          success: this.$t("objects.add_success"),
          error: this.$t("objects.add_failed"),
        },
      },

      // Delete Check dialog.
      showDeleteChecker: false,
      deleteObjectName: "",

      // Selection.
      resource: null,
      selected_prefix: [],
      selected_object: null,

      // Const.
      imageExt: ["jpg", "jpeg", "png", "gif", "svg"],
      jsonExt: ["json"],
      textExt: ["txt", "log", "rtf", "csv"],
      codeExt: ["html", "js", "vue", "java", "scala", "c", "cpp", "h", "hpp"],

      // Upload.
      upload_file: null,

      // Image viewer dialog.
      imageViewerOpener: true,
      imageViewer: false,
      viewerSrc: null,
      zoom_min: -3,
      zoom_max: 3,
      zoom_count: 0,
      zoom_px: 1.2,
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
        // Initialize objectlist.
        this.objectList = [];
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
     * Make icon color.
     * @public
     * @param {object} - object information.
     */
    getIconColor: function(object) {
      if (this.isDir(object)) {
        return "teal";
      } else if (this.isImage(object)) {
        return "orange";
      } else if (this.isText(object)) {
        return "blue lighten-2";
      } else if (this.isJson(object)) {
        return "yellow darken-2";
      } else if (this.isPdf(object)) {
        return "red lignten-1";
      } else {
        return "grey lighten-1";
      }
    },

    /**
     * Open file finder. (Select file)
     * @public
     */
    selectFile: function() {
      var a = document.createElement("input");
      a.setAttribute("type", "file");
      a.setAttribute("multiple", true);
      a.click();
      var self = this;
      a.addEventListener("change", (evt) => {
        var files = evt.target.files;
        this.uploadFiles(files);
      });
    },

    /**
     * File drop event.
     * @public
     * @param {DropEvent} - File drop event.
     */
    fileDrop: function(event) {
      let files = event.dataTransfer.files;
      this.uploadFiles(files);
    },

    /**
     * Upload files.
     * @public
     * @param {array} - Files(Blobs).
     */
    uploadFiles: function(files) {
      this.$debug(this.$options.name, "uploadFiles", "Files:", files);
      var self = this;
      self.upload_file = new FormData();
      var prefixes = this.cvtPrefixData();
      files.forEach((file) => {
        if (prefixes) {
          self.upload_file.append(`file`, file, prefixes + "/" + file.name);
        } else {
          self.upload_file.append(`file`, file, file.name);
        }
      });
      this.uploadSignal = true;
    },

    /**
     * Object upload success event.
     * @public
     */
    onObjectUploadSuccess: function() {
      this.showAlert(true, "add");
      this.onProjectMakerClose();
      this.getSignal = true;
    },

    /**
     * Object upload Failed event.
     * @public
     */
    onObjectUploadError: function() {
      this.showAlert(false, "add");
      this.onProjectMakerClose();
    },

    /**
     * Select object.
     * @public
     * @param {object} - object data.
     */
    selectObject: function(object) {
      this.resource = null;
      this.selected_object = null;
      this.$nextTick().then(() => {
        this.$debug(this.$options.name, "selectObject", "Object:", object);
        if (this.isDir(object)) {
          // dir object load.
          this.selected_prefix.push(object);
          this.$emit("selectPrefix", this.selected_prefix);
          this.$emit("selectObject", null);
          this.getSignal = true;
          return;
        }
        this.selected_object = object;
        this.$emit("selectObject", object);
        if (object !== null && object !== undefined) {
          this.getObjectSignal = true;
        }
      });
    },

    /**
     * Convert prefix array to string.
     * @public
     */
    cvtPrefixData: function() {
      var result = "";
      if (!this.selected_prefix) {
        return result;
      }
      this.selected_prefix.forEach((prefix) => {
        result += prefix.objectName + "/";
      });
      return result;
    },

    /**
     * For vuetify breadcrumds link.
     * @public
     * @param {array} - prefix object list.
     */
    reLinkPrefix: function(prefixes, reload) {
      if (prefixes) {
        this.selected_prefix = [...prefixes];
      } else {
        this.selected_prefix = [];
      }
      this.$emit("selectPrefix", this.selected_prefix);
      if (reload) {
        this.getSignal = true;
      }
    },

    /**
     * Get ext name.
     * @public
     * @param {string} - object name.
     */
    getExt: function(objectName) {
      var spl;
      var ext;
      try {
        spl = objectName.split(".");
        ext = spl[spl.length - 1];
        return ext.toLowerCase();
      } catch (e) {
        this.$error(this.$options.name, "imageDownload", "Details:", e);
        return null;
      }
    },

    /**
     * Make Donwloader and download.
     * @public
     * @param {string} - filename.
     * @param {string} - download url.
     */
    onDownload: function(filename, href) {
      var downloader = document.createElement("a");
      downloader.style = "display: none";
      downloader.href = href;
      downloader.download = `${filename}`;
      downloader.click();
      setTimeout(() => {
        downloader = null;
      }, 650);
    },

    /**
     * object download.
     * @public
     */
    objectDownload: function() {
      if (!this.selected_object) {
        return;
      }
      if (
        this.isImage(this.selected_object) ||
        this.isPdf(this.selected_object)
      ) {
        this.imageDownload(this.selected_object, this.resource);
      } else if (this.isJson(this.selected_object)) {
        this.jsonDownload(this.selected_object, this.resource);
      } else {
        this.textDownload(this.selected_object, this.resource);
      }
    },

    /**
     * Image Download.
     * @public
     * @param {string} - object name.
     * @param {string} - image binary data.
     */
    imageDownload: function(object, resource, qual) {
      this.onDownload(object.objectName, resource);

      // var quality = qual || 1.0;
      // var ext = null;
      // if (object.type) {
      //   ext = `${object.type}`;
      // } else {
      //   ext = this.getExt(object.objectName);
      //   if (ext === null) {
      //     return;
      //   }
      //   if (ext === 'jpg') {
      //     ext = 'jpeg';
      //   }
      //   ext = `image/${ext}`;
      // }
      // var img = new Image();
      // var canvas = document.createElement("canvas");
      // var ctx = canvas.getContext("2d");
      // img.onload = () => {
      //   canvas.width = img.naturalWidth;
      //   canvas.height = img.naturalHeight;
      //   ctx.drawImage(img, 0, 0);
      //   var uri = canvas.toDataURL(`${ext}`, quality);
      //   this.onDownload(object.objectName, uri);
      // }
      // img.src = resource

      /**
      // make array buffer.
      // 1. catch resource
      var bin;
      try {
        bin = window.atob(resource.split("base64,")[1]);
      } catch (e) {
        this.$error(this.$options.name, "imageDownload", "Details:", e);
        return;
      }
      // 2. Convert binary to arraybuffer.
      var length = bin.length;
      var buffer = new ArrayBuffer(length);
      var array = new Uint8Array(buffer);
      for (var i = 0; i < length; ++i) {
        array[i] = bin.charCodeAt(i);
      }

      // 3. Convert arraybuffer to blob.
      var file = new Blob([buffer], { type: `image/${ext}` });

      // 4. Make downloader.
      var downloader = document.createElement("a");
      downloader.style = "display: none";
      downloader.href = URL.createObjectURL(file);
      downloader.download = `${objectName}`;
      downloader.click();
      */
    },

    /**
     * Text Download.
     * @public
     * @param {string} - object name.
     * @param {string} - resource data.
     */
    textDownload: function(object, resource) {
      var ext = object.type || "text/plain";
      var file = new Blob([resource], { type: ext });
      this.onDownload(object.objectName, URL.createObjectURL(file));
    },

    /**
     * Json Download.
     * @public
     * @param {string} - object name.
     * @param {string} - resource data.
     */
    jsonDownload: function(object, resource) {
      var ext = object.type || "application/json";
      var text;
      if (typeof resource === "object") {
        text = JSON.stringify(resource, null, 4);
      } else {
        text = resource;
      }
      var file = new Blob([text], { type: ext });
      this.onDownload(object.objectName, URL.createObjectURL(file));
    },

    /**
     * Open object delete checker dialog.
     * @public
     * @param {object} - Object information data.
     */
    openDeleteChecker: function(objectInfo) {
      this.deleteObjectName = objectInfo.objectName;
      this.showDeleteChecker = true;
    },

    /**
     * Close Delete check dialog.
     * @public
     */
    closeDeleteCheck: function() {
      this.showDeleteChecker = false;
      this.$nextTick().then(() => {
        this.deleteObjectName = "";
      });
    },

    /**
     * Send will be delete user data for delete and close delete check dialog.
     * @public
     */
    onDeleteObject: function() {
      this.deleteSignal = true;
    },

    /**
     * Check bucket-prefiex(dir).
     * @public
     * @param {object} - object information.
     */
    isDir: function(object) {
      if (object === null || object === undefined) {
        return false;
      }
      return !!object.isDir;
    },

    /**
     * Check image file.
     * @public
     * @param {object} - object information.
     */
    isImage: function(object) {
      var result = false;
      if (object.type) {
        object.type = object.type.toLowerCase();
        if (object.type !== "unknown") {
          result = object.type.includes("image/");
          return result;
        }
      }
      var spl = object.objectName.split(".");
      var ext = spl[spl.length - 1];
      var is = this.imageExt.indexOf(ext.toLowerCase());
      if (is >= 0) {
        result = true;
      }
      return result;
    },

    /**
     * Check code file.
     * @public
     * @param {object} - object information.
     */
    isCode: function(object) {
      var spl = object.objectName.split(".");
      var ext = spl[spl.length - 1];
      var is = this.codeExt.indexOf(ext.toLowerCase());
      if (is < 0) {
        return false;
      } else {
        return true;
      }
    },

    /**
     * Check text file.
     * @public
     * @param {object} - object information.
     */
    isText: function(object) {
      var result = false;
      if (object.type) {
        object.type = object.type.toLowerCase();
        if (object.type === "unknown") {
          return this.isCode(object);
        } else {
          result = object.type.includes("text/");
          if (!result) {
            result = this.isCode(object);
          }
          return result;
        }
      }
      var spl = object.objectName.split(".");
      var ext = spl[spl.length - 1];
      var is = this.textExt.indexOf(ext.toLowerCase());
      if (is < 0) {
        return this.isCode(object);
      } else {
        result = true;
      }
      return result;
    },

    /**
     * Check json file.
     * @public
     * @param {object} - object information.
     */
    isJson: function(object) {
      var result = false;
      if (object.type) {
        object.type = object.type.toLowerCase();
        if (object.type !== "unknown") {
          result = object.type.includes(`/json`);
          return result;
        }
      }
      var spl = object.objectName.split(".");
      var ext = spl[spl.length - 1];
      var is = this.jsonExt.indexOf(ext.toLowerCase());
      if (is >= 0) {
        result = true;
      }
      return result;
    },

    /**
     * Check pdf file.
     * @public
     * @param {object} - object information.
     */
    isPdf: function(object) {
      var result = false;
      if (object.type) {
        object.type = object.type.toLowerCase();
        if (object.type !== "unknown") {
          result = object.type.includes(`pdf`);
          return result;
        }
      }
      var spl = object.objectName.split(".");
      var ext = spl[spl.length - 1];
      var is = ["pdf"].indexOf(ext.toLowerCase());
      if (is >= 0) {
        result = true;
      }
      return result;
    },

    /**
     * Open Image viewer dialog.
     * @public
     */
    openImageViewer: function() {
      this.imageViewer = true;
      this.viewerSrc = this.resource;
    },

    /**
     * Close Image viewer dialog.
     * @public
     */
    closeImageViewer: function() {
      this.viewerSrc = null;
      this.imageViewer = false;
      this.zoom_count = 0;
    },

    /**
     * Zoom out image at Image viewer dialog.
     * @public
     */
    viewerZoomOut: function() {
      if (this.$refs.viewerImage) {
        if (this.zoom_count < this.zoom_min) {
          return;
        }
        var img = this.$refs.viewerImage;
        var width = img.clientWidth;
        var height = img.clientHeight;
        img.style.width = width / this.zoom_px + "px";
        img.style.height = height / this.zoom_px + "px";
        --this.zoom_count;
      }
    },

    /**
     * Zoom in image at Image viewer dialog.
     * @public
     */
    viewerZoomIn: function() {
      if (this.$refs.viewerImage) {
        if (this.zoom_count > this.zoom_max) {
          return;
        }
        var img = this.$refs.viewerImage;
        var width = img.clientWidth;
        var height = img.clientHeight;
        // if (this.$refs.viewerZone.offsetWidth < (width + this.zoom_px) || this.$refs.viewerZone.offsetHeight < (height + this.zoom_px)) {
        //   return;
        // }
        img.style.width = width * this.zoom_px + "px";
        img.style.height = height * this.zoom_px + "px";
        ++this.zoom_count;
      }
    },

    /**
     * Get object list refresh.
     * @public
     */
    onRefreshObjectList: function() {
      this.selected_object = null;
      this.getSignal = true;
    },

    /**
     * Export folder names.
     * @public
     */
    getFolders: function() {
      var dirs = [];
      this.objectList.forEach((object) => {
        if (object.isDir) {
          dirs.push(object.objectName);
        }
      });
      return dirs;
    },

    /**
     * Check Duplicated folder name.
     * @public
     */
    isDuplicatedFolder: function(newFolderName) {
      var folders = this.getFolders() || [];
      var find = folders.indexOf(newFolderName);
      if (find < 0) {
        return false;
      } else {
        return true;
      }
    },

    /**
     * Close new folder dialog.
     * @public
     */
    closeNewFolderMenu: function() {
      this.newFolder.show = false;
      this.$nextTick().then(() => {
        this.newFolder.name = "";
        this.newFolder.errorMsg = "";
        this.newFolder.alert = false;
      });
    },

    /**
     * Create new folder.
     * @public
     */
    createNewFolder: function() {
      if (this.newFolder.name) {
        if (this.isDuplicatedFolder(this.newFolder.name)) {
          this.newFolder.alert = true;
          this.newFolder.errorMsg = "objects.duplicated_folder_name";
          return;
        }
        var newDir = {};
        newDir.icon = "fas fa-folder";
        newDir.isDir = true;
        newDir.lastModified = "  ";
        newDir.objectName = this.newFolder.name;
        this.objectList.unshift(newDir);
        this.closeNewFolderMenu();
      } else {
        this.newFolder.alert = true;
        this.newFolder.errorMsg = "objects.empty_folder_name";
        return;
      }
    },

    /**
     * Event folder name input.
     * @public
     */
    inputFolderName: function() {
      this.newFolder.alert = false;
      this.newFolder.errorMsg = "";
    },

    /**
     * Preview image load event.
     * @public
     * @param {event} - image src data.
     */
    onImageLoad: function(img) {
      this.imageViewerOpener = true;
    },

    /**
     * Preview image load error event.
     * @public
     * @param {event} - image src data.
     */
    onImageLoadError: function(err) {
      this.imageViewerOpener = false;
    },
  },
  created() {
    if (!this.showIndex) {
      var find;
      for (var i = 0; i < this.objectHeaders.length; ++i) {
        if (this.objectHeaders[i].value === "index") {
          find = i;
        }
      }
      this.objectHeaders.splice(find, 1);
      this.objectHeaders = [...this.objectHeaders];
    }
    if (!this.showIcon) {
      var find;
      for (var i = 0; i < this.objectHeaders.length; ++i) {
        if (this.objectHeaders[i].value === "icon") {
          find = i;
        }
      }
      this.objectHeaders.splice(find, 1);
      this.objectHeaders = [...this.objectHeaders];
    }
    if (!this.showCreatedAt) {
      var find;
      for (var i = 0; i < this.objectHeaders.length; ++i) {
        if (this.objectHeaders[i].value === "createdAt") {
          find = i;
        }
      }
      this.objectHeaders.splice(find, 1);
      this.objectHeaders = [...this.objectHeaders];
    }
    if (!this.showModifiedAt) {
      var find;
      for (var i = 0; i < this.objectHeaders.length; ++i) {
        if (this.objectHeaders[i].value === "modifiedAt") {
          find = i;
        }
      }
      this.objectHeaders.splice(find, 1);
      this.objectHeaders = [...this.objectHeaders];
    }
    if (!this.showDelete) {
      var find;
      for (var i = 0; i < this.objectHeaders.length; ++i) {
        if (this.objectHeaders[i].value === "delete") {
          find = i;
        }
      }
      this.objectHeaders.splice(find, 1);
      this.objectHeaders = [...this.objectHeaders];
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
    const $getObjectSignal = this.$watchAsObservable("getObjectSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((getObjectSignal) => getObjectSignal == true) // if signal is true.
      .debounceTime(1000);
    const $uploadSignal = this.$watchAsObservable("uploadSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((uploadSignal) => uploadSignal == true); // if signal is true.
    // .debounceTime(1000)
    const $deleteSignal = this.$watchAsObservable("deleteSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((deleteSignal) => deleteSignal == true) // if signal is true.
      .debounceTime(1000);
    return {
      getObjects: Observable.combineLatest($getSignal, (getSignal) => ({
        getSignal,
      })).flatMap(
        ({ getSignal }) =>
          this.$api
            .getBucketsObjects(
              this.$store.getters["user/getAccessToken"],
              this.$store.getters["user/getRefreshToken"],
              this.$store.getters["project/getSelectProject"],
              this.parentBucket.name,
              this.cvtPrefixData()
            )
            .do((res) => {
              this.showAlert(true, "list");
              this.$debug(
                this.$options.name,
                "subscriptions::getBucketsObjects",
                "Response:",
                res
              );
              var checker = res.result.obj;
              var list = [];
              for (var index = 0; index < checker.length; ++index) {
                if (checker[index].status !== "failure") {
                  list.push(checker[index].item);
                }
              }
              var objects = [];
              var dir = [];
              for (var i = 0; i < list.length; ++i) {
                var obj = list[i];
                var dateTime = this.$util.cvtTime(obj.lastModified);
                obj.lastModified = `${
                  dateTime.year ? dateTime.year + "." : ""
                } ${dateTime.month ? dateTime.month + "." : ""} ${
                  dateTime.day ? dateTime.day + "." : ""
                } ${dateTime.hour ? dateTime.hour + ":" : ""}${
                  dateTime.min ? dateTime.min + ":" : ""
                }${dateTime.sec ? dateTime.sec : ""}`;
                if (this.isDir(obj)) {
                  list[i].icon = "fas fa-folder";
                  list[i].objectName = list[i].objectName.substring(
                    0,
                    list[i].objectName.length - 1
                  );
                  if (list[i].objectName.includes("/")) {
                    var tempSplit = list[i].objectName.split("/");
                    list[i].objectName = tempSplit[tempSplit.length - 1];
                  }
                  if (list[i].size === 0) {
                    delete list[i].size;
                  }
                  dir.push(list[i]);
                  continue;
                } else if (this.isImage(obj)) {
                  list[i].icon = "fas fa-file-image";
                } else if (this.isText(obj)) {
                  list[i].icon = "fas fa-file-code";
                } else if (this.isJson(obj)) {
                  list[i].icon = "fas fa-file-alt";
                } else if (this.isPdf(obj)) {
                  list[i].icon = "fas fa-file-pdf";
                } else {
                  list[i].icon = "fas fa-file";
                }
                if (obj.size) {
                  obj.size = this.$util.convertByteType(obj.size);
                }
                if (list[i].objectName.includes("/")) {
                  var copyName = list[i].objectName.split("/");
                  list[i].objectName = copyName[copyName.length - 1];
                }
                objects.push(list[i]);
              }
              dir = dir.concat([...objects]); // Merge dir list and object list. (For dir first view)
              this.objectList = [...dir];
              this.showAlert(true, "list");
            })
            .catch((error) => {
              this.showAlert(false, "list");
              this.$error(
                this.$options.name,
                "subscriptions::getBucketsObjects",
                error
              );
              return Observable.of(null);
            })
            .do(() => {
              this.getSignal = false;
            })
        /*
          {
            var list = this.$util.cloneObject(require("./test/objectlist.json")["obj"]);
            var objects = [];
            var dir = [];
            for (var i = 0; i < list.length; ++i) {
              var obj = list[i];
              obj.size = Math.round(obj.size / 1024) + "KB";
              if (this.isDir(obj)) {
                list[i].icon = "fas fa-folder";
                dir.push(list[i]);
                continue;
              } else if (this.isImage(obj)) {
                list[i].icon = "fas fa-file-image";
              } else if (this.isText(obj)) {
                list[i].icon = "fas fa-file-code";
              } else if (this.isJson(obj)) {
                list[i].icon = "fas fa-file-alt";
              } else {
                list[i].icon = "fas fa-file";
              }
              objects.push(list[i]);
            }
            dir = dir.concat([...objects]); // Merge dir list and object list. (For dir first view)
            this.objectList = [...dir];
            this.showAlert(true, 'list');
            this.getSignal = false;
          }
          */
      ),
      getObject: Observable.combineLatest(
        $getObjectSignal,
        (getObjectSignal) => ({ getObjectSignal })
      ).flatMap(({ getObjectSignal }) =>
        this.$api
          .getBucketsObject(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.parentBucket.name,
            this.selected_object.objectName,
            this.cvtPrefixData(),
            this.isImage(this.selected_object)
          )
          .do((res) => {
            // success.
            this.$debug(
              this.$options.name,
              "subscriptions::getBucketsObject",
              "Response:",
              res
            );
            if (res.status !== 200) {
              this.resource = null;
              throw new Error(`Response status ${res.status}`);
            }
            var reader = new FileReader();
            if (res.data) {
              reader.onload = (r) => {
                if (this.isJson(this.selected_object)) {
                  this.resource = JSON.parse(r.target.result);
                } else {
                  this.resource = r.target.result;
                }
              };
              if (
                this.isImage(this.selected_object) ||
                this.isPdf(this.selected_object)
              ) {
                reader.readAsDataURL(res.data);
              } else {
                reader.readAsText(res.data);
              }
            }
            this.showAlert(true, "list");
          })
          .catch((error) => {
            // failed.
            this.showAlert(false, "list");
            this.$error(
              this.$options.name,
              "subscriptions::getBucketsObject",
              error
            );
            return Observable.of(null);
          })
          .do(() => {
            this.getObjectSignal = false;
          })
      ),
      uploadObject: Observable.combineLatest($uploadSignal, (uploadSignal) => ({
        uploadSignal,
      })).flatMap(({ uploadSignal }) =>
        this.$api
          .uploadBucketsObject(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.parentBucket.name,
            this.upload_file
          )
          .do((res) => {
            // success.
            this.$debug(
              this.$options.name,
              "subscriptions::uploadBucketsObject",
              "Response: ",
              res
            );
            this.showAlert(true, "add");
            this.upload_file = null;
            this.getSignal = true;
          })
          .catch((error) => {
            // failed.
            this.showAlert(false, "add");
            this.$error(
              this.$options.name,
              "subscriptions::uploadBucketsObject",
              error
            );
            return Observable.of(null);
          })
          .do(() => {
            this.uploadSignal = false;
          })
      ),
      deleteBucket: Observable.combineLatest($deleteSignal, (deleteSignal) => ({
        deleteSignal,
      })).flatMap(({ deleteSignal }) =>
        this.$api
          .deleteBucketsObject(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.parentBucket.name,
            this.deleteObjectName,
            this.cvtPrefixData()
          )
          .do((res) => {
            // success.
            this.showAlert(true, "delete");
            this.$debug(
              this.$options.name,
              "subscriptions::deleteBucketsObject",
              "Response:",
              res
            );
            if (this.selected_object) {
              if (this.deleteObjectName === this.selected_object.objectName) {
                this.selectObject(null);
              }
            }
            this.closeDeleteCheck();
            this.getSignal = true;
          })
          .catch((error) => {
            // failed.
            this.showAlert(false, "delete");
            this.$error(
              this.$options.name,
              "subscriptions::deleteBucketsObject",
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
.unknown--container {
  display: inline-block;
  position: relative;
  width: 100%;
  height: 50%;
}
.unknown--icon {
  width: 100%;
  height: 100%;
}
.unknown--text {
  width: 100%;
  position: absolute;
  top: 5px;
  font-weight: bold;
  font-style: italic;
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
.objectNaming {
  font-weight: bold;
}
.objectNaming:hover {
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
.preview--name {
  font-weight: bold;
  font-size: 20px;
}
.preview--size {
  font-size: 13px;
  color: grey;
}
.preview--modifiedAt {
  font-size: 13px;
  color: grey;
}

#myTable >>> .v-data-table__wrapper {
  max-height: calc(100vh - 95px);
}
pre {
  white-space: pre-line;
}
.spinner {
  background-color: transparent;
  animation: rotation 3s infinite linear;
  -webkit-animation: rotation 3s infinite linear;
  -webkit-transform-origin: 0% 100% 0% 100%;
  -moz-transform-origin: 0% 100% 0% 100%;
  -ms-transform-origin: 0% 100% 0% 100%;
  -o-transform-origin: 0% 100% 0% 100%;
  transform-origin: 0% 100% 0% 100%;
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

.splitPane {
  position: absolute;
}
.pane {
  background-color: transparent !important;
  overflow-y: auto;
}
.listZone {
  width: 100%;
  height: 100%;
}
.refreshButton {
  border-radius: 5px;
  margin-right: 10px;
}
.uploadButton {
  margin-left: 10px;
}
.tableFooter {
  position: relative;
  padding: 0px 10px 0px 10px;
}
.previewZone {
  width: 100%;
  height: 100%;
}
.preview--content {
  height: calc(100% - 200px) !important;
}
.preview--content__image {
  width: 100%;
  max-height: 100%;
  margin: 10px;
}
.preview--content__json {
  width: 100%;
  height: 50%;
}
.preview--content__text {
  width: 100%;
  height: 50%;
}
.preview--footer {
  background-color: transparent !important;
}
.imageViewer--content {
  position: absolute;
  top: 10%;
  left: 10%;
  width: 80%;
  height: 80%;
}
.imageViewer--content__image {
  object-fit: scale-down;
  width: 80%;
  height: 80%;
}
.imageViewer--footer {
  position: absolute;
  width: 80%;
  height: 10%;
  left: 10%;
  bottom: 0px;
  /* border: 1px dotted grey; */
  border-radius: 15px;
}
/* .imageViewer--closer {
  border: 1px dotted grey;
} */
.deleteChecker--title {
  padding: 0px !important;
}
.deleteChecker--alert {
  margin: 0px;
  width: 100%;
  border-radius: 4px 0px 0px 0px;
}
</style>
