<template>
  <div class="viewerMain">
    <audio ref="alarm">
      <source src="@/assets/beep-1.wav" />
    </audio>
    <v-toolbar height="30">
      <v-spacer></v-spacer>
      <v-btn icon small @click="reverse = !reverse">
        <v-icon size="21">{{ reverse ? 'fas fa-sort-amount-up' : 'fas fa-sort-amount-up-alt' }}</v-icon>
      </v-btn>
      <v-btn icon small @click="openSetting">
        <v-icon>settings</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card v-if="originBlobs.length > 0 || reverseBlobs.length > 0" class="viewerCard">
      <v-splitpanes class="default-theme">
        <v-pane :size="30" class="pane">
          <div
            class="viewer"
            v-for="(blob, index) in reverse ? reverseBlobs : originBlobs"
            :key="index"
            :title="blob.left.name"
          >
            <img
              v-if="isImage(blob.left)"
              :src="blob.left.src"
              class="viewer--image"
              @click="openDataViewer(blob.left)"
            />
            <audio
              v-else-if="isAudio(blob.left)"
              :src="blob.left.src"
              controls
              class="viewer--audio"
            ></audio>
            <video
              v-else-if="isVideo(blob.left)"
              :src="blob.left.src"
              controls
              class="viewer--video"
            ></video>
            <div v-else-if="isPdf(blob.left)" class="viewer--pdf">
              <v-btn icon width="31" height="31">
                <v-icon
                  size="25"
                  color="red lighten-1"
                  class="viewer--pdf__content"
                  @click="openDataViewer(blob.left)"
                >fas fa-file-pdf</v-icon>
              </v-btn>
              <span>{{ blob.left.name ? blob.left.name: undefined }}</span>
            </div>
            <div v-else class="viewer--text">
              <pre v-html="blob.left.src" @click="openDataViewer(blob.left)"></pre>
            </div>
          </div>
        </v-pane>
        <v-pane :size="70" class="pane">
          <div
            class="viewer"
            v-for="(blob, index) in reverse ? reverseBlobs : originBlobs"
            :key="index"
            :title="blob.right.name"
          >
            <img
              v-if="isImage(blob.right)"
              :src="blob.right.src"
              class="viewer--image"
              @click="openDataViewer(blob.right)"
            />
            <audio
              v-else-if="isAudio(blob.right)"
              :src="blob.right.src"
              controls
              class="viewer--audio"
            ></audio>
            <video
              v-else-if="isVideo(blob.right)"
              :src="blob.right.src"
              controls
              class="viewer--video"
            ></video>
            <div v-else-if="isPdf(blob.right)" class="viewer--pdf">
              <v-btn icon width="31" height="31">
                <v-icon
                  size="25"
                  color="red lighten-1"
                  class="viewer--pdf__content"
                  @click="openDataViewer(blob.right)"
                >fas fa-file-pdf</v-icon>
              </v-btn>
              <span>{{ blob.right.name ? blob.right.name: undefined }}</span>
            </div>
            <div v-else class="viewer--text">
              <pre v-html="blob.right.src" @click="openDataViewer(blob.right)"></pre>
            </div>
          </div>
        </v-pane>
      </v-splitpanes>
    </v-card>

    <v-dialog
      v-model="showSetting"
      scrollable
      persistent
      max-width="650px"
      transition="dialog-transition"
    >
      <v-card>
        <v-card-title>
          {{ $t('setting') }}
          <v-spacer></v-spacer>
          <v-btn small icon @click="bucketsSignal = !bucketsSignal" :loading="bucketsSignal">
            <v-icon>refresh</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="settingZone">
          <v-container>
            <v-row no-gutters>
              <v-col class="leftSetting">
                <div class="timerSetting">
                  <v-text-field
                    :label="$t('timer_time_setting') + ` (${$t('second')})`"
                    v-model.number="settingValue.interval"
                    hide-details
                    dense
                    outlined
                  ></v-text-field>
                </div>
              </v-col>
              <v-col class="rightSetting">
                <div class="timerSetting">
                  <v-select
                    :label="$t('limit_setting')"
                    v-model="settingValue.limited"
                    dense
                    outlined
                    hide-details
                    :items="limits"
                  ></v-select>
                </div>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <v-row no-gutters>
              <v-col class="leftSetting">
                <v-select
                  dense
                  outlined
                  hide-details
                  class="margin-10"
                  :label="$t('left') + ' ' + $t('bucket')"
                  :disabled="!buckets"
                  :items="buckets"
                  @input="onSelectLeftBucketPrefix($event)"
                  v-model="settingValue.left.bucket"
                ></v-select>
                <template v-for="(prefixes, index) in prefixes1">
                  <v-select
                    :key="index"
                    dense
                    outlined
                    hide-details
                    class="margin-10"
                    :label="`${$t('objects.folder_name')} [${index + 1}]`"
                    :disabled="!prefixes"
                    :items="prefixes"
                    @input="onSelectLeftBucketPrefix('dir', index)"
                    v-model="settingValue.left.prefix[index]"
                  ></v-select>
                </template>
                <v-text-field
                  dense
                  outlined
                  class="margin-10"
                  hide-details
                  :label="$t('auto_change_dir')"
                  v-model="settingValue.left.appendPrefix"
                ></v-text-field>
              </v-col>
              <v-col class="rightSetting">
                <v-select
                  dense
                  outlined
                  hide-details
                  class="margin-10"
                  :label="$t('right') + ' ' + $t('bucket')"
                  @input="onSelectRightBucketPrefix($event)"
                  :disabled="!buckets"
                  :items="buckets"
                  v-model="settingValue.right.bucket"
                ></v-select>
                <template v-for="(prefixes, index) in prefixes2">
                  <v-select
                    :key="index"
                    dense
                    outlined
                    hide-details
                    class="margin-10"
                    :label="`${$t('objects.folder_name')} [${index + 1}]`"
                    :disabled="!prefixes"
                    :items="prefixes"
                    @input="onSelectRightBucketPrefix('dir', index)"
                    v-model="settingValue.right.prefix[index]"
                  ></v-select>
                </template>
                <v-text-field
                  dense
                  outlined
                  class="margin-10"
                  hide-details
                  :label="$t('auto_change_dir')"
                  v-model="settingValue.right.appendPrefix"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <div class="text-right pa-1">
            <span
              v-if="bucketsSignal"
              class="loadmessage"
            >{{ `${$t('bucket')} ${$t('loading_data')}` }}</span>
            <span
              v-else-if="!buckets"
              class="emptymessage"
            >{{ `${$t('bucket')} ${$t('empty_data')}` }}</span>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn small text @click="closeSetting">{{ $t('cancel') }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn small text @click="applySetting">{{ $t('apply') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showDataViewer" fullscreen @keydown.esc="closeDataViewer">
      <template v-if="showData">
        <div ref="dataViewerZone" class="dataViewerZone">
          <v-container fluid fill-height>
            <v-layout align-center justify-center>
              <img v-if="isImage(showData)" :src="showData.src" class="dataViewerZone__image" />
              <!-- <video v-else-if="isVideo(showData)" :src="showData.src" controls class="dataViewerZone__video"></video> -->
              <iframe v-else-if="isPdf(showData)" :src="showData.src" class="dataViewerZone__pdf"></iframe>
              <v-sheet v-else class="dataViewerZone__text">
                <pre v-html="showData.src"></pre>
              </v-sheet>
            </v-layout>
          </v-container>
        </div>
        <v-btn absolute top right icon class="dataViewerZone__closer" @click="closeDataViewer">
          <v-icon>close</v-icon>
        </v-btn>
      </template>
    </v-dialog>
  </div>
</template>

<script>
import { Observable } from "rxjs";

export default {
  name: "BlobViewer",
  props: {
    /**
     * Init Save data from API.
     */
    component_data: {
      default: null
    }
  },
  data() {
    return {
      /**
       * blobs
       * [
       *   { left: {name: $name, type: $type, src: $src}, right: {name: $name, type: $type, src: $src} },
       *   { left: {name: $name, type: $type, src: $src}, right: {name: $name, type: $type, src: $src} }
       * ]
       */
      blobs: [],
      /**
       * objects
       * [
       *   { left: $name, right: $name },
       *   { left: $name, right: $name }
       * ]
       */
      objects: [],
      /**
       * newObjects
       * [
       *   { left: $name, right: $name },
       *   { left: $name, right: $name }
       * ]
       */
      newObjects: [],

      // pane options.
      bucket1: null,
      prefix1: null,
      appendPrefix1: null,
      bucket2: null,
      prefix2: null,
      appendPrefix2: null,
      interval: 3,
      limited: 10,
      limits: [5, 10, 15, 20],
      repeater: null,

      // api options.
      page: 1,
      order: "desc-Date",
      filter: "fileOnly",

      // Options.
      reverse: false,

      // Settings.
      showSetting: false,
      bucketsSignal: false,
      leftBucketSignal: false,
      rightBucketSignal: false,
      buckets: null,
      prefixes1: [],
      prefixes2: [],
      settingValue: {
        left: {
          bucket: null,
          prefix: [],
          appendPrefix: ""
        },
        right: {
          bucket: null,
          prefix: [],
          appendPrefix: ""
        },
        interval: this.interval,
        limited: this.limited
      },
      initValue: {
        left: {
          bucket: null,
          prefix: [],
          appendPrefix: ""
        },
        right: {
          bucket: null,
          prefix: [],
          appendPrefix: ""
        },
        interval: this.interval,
        limited: this.limited
      },

      // Data Viewer dialog.
      showDataViewer: false,
      showData: null
    };
  },
  watch: {
    /**
     * 버켓이 변경될 경우 초기화 하기 위해 사용.
     */
    bucket1() {
      this.blobs = [];
      this.objects = [];
      this.newObjects = [];
    },
    bucket2() {
      this.blobs = [];
      this.objects = [];
      this.newObjects = [];
    }
  },
  computed: {
    /**
     * 파일 리스트의 개수 제한을 사용하기 위해 사용.
     */
    originBlobs() {
      if (!this.blobs) {
        return [];
      }
      var blobs = this.blobs.slice();
      if (!blobs) {
        return [];
      }
      if (blobs.length > this.limited) {
        var a = blobs.splice(0, this.limited);
        return a;
      }
      return this.blobs;
    },

    /**
     * 리스트 역순 출력을 위해 사용.
     */
    reverseBlobs: function() {
      if (!this.blobs) {
        return [];
      }
      var blobs = this.blobs.slice();
      if (!blobs) {
        return [];
      }
      if (blobs.length > this.limited) {
        var a = blobs.splice(0, this.limited);
        return a.reverse();
      }
      return blobs.reverse();
    }
  },
  methods: {
    /**
     * Convert Blob to Data Source.
     * @public
     * @param {Blob} - Blob is file(binary).
     */
    blobToSource: function(blob) {
      return new Promise((resolve, reject) => {
        var reader = new FileReader();
        reader.onload = function() {
          resolve(reader.result);
        };
        reader.onerror = function(err) {
          this.$error(this.$options.name, "blobToSource", err);
          reject(null);
        };
        if (
          blob.type.includes("pdf") ||
          blob.type.includes("image") ||
          blob.type.includes("audio") ||
          blob.type.includes("video")
        ) {
          reader.readAsDataURL(blob);
        } else {
          reader.readAsText(blob);
        }
      });
    },

    /**
     * Check blob type images.
     * @public
     * @param {Blob}
     */
    isImage: function(blob) {
      if (!blob) {
        return false;
      }
      if (blob.type.includes("image")) {
        return true;
      } else {
        return false;
      }
    },

    /**
     * Check blob type video.
     * @public
     * @param {Blob}
     */
    isVideo: function(blob) {
      if (!blob) {
        return false;
      }
      if (blob.type.includes("video")) {
        return true;
      } else {
        return false;
      }
    },

    /**
     * Check blob type audio.
     * @public
     * @param {Blob}
     */
    isAudio: function(blob) {
      if (!blob) {
        return false;
      }
      if (blob.type.includes("audio")) {
        return true;
      } else {
        return false;
      }
    },

    /**
     * Check blob type pdf.
     * @public
     * @param {Blob}
     */
    isPdf: function(blob) {
      if (!blob) {
        return false;
      }
      if (blob.type.includes("pdf")) {
        return true;
      } else {
        return false;
      }
    },

    /**
     * Check blob type images.
     * @public
     * @param {filename}
     * @param {minio/ObjectList}
     */
    checkPair: function(left, rights) {
      if (typeof left !== "string") {
        return null;
      }
      if (rights.length <= 0) {
        return null;
      }
      var temp = left.split(".");
      if (temp.length < 2) {
        return null;
      }
      for (var right of rights) {
        if (!right.item.objectName) {
          continue;
        }
        if (right.item.objectName.includes("/")) {
          var spt = right.item.objectName.split("/");
          right.item.objectName = spt[spt.length - 1];
        }
        if (right.item.objectName.split(".")[0] === temp[0]) {
          return right.item.objectName;
        }
      }
      return null;
    },

    /**
     * Edit object list.
     * @public
     * @param {minio/ObjectList}
     */
    editObjectList: async function(newValue) {
      var oldValue = this.objects.slice();
      // old data delete.
      for (var old of oldValue) {
        var isDelete = true;
        for (var newV of newValue) {
          if (newV.left === old.left) {
            isDelete = false;
          }
        }
        if (isDelete) {
          var find = this.objects.indexOf(old);
          if (find >= 0) {
            this.objects.splice(find, 1);
            this.objects = [...this.objects];
          }
        }
      }
      var tempBlobs = this.blobs.slice();
      for (var blob of tempBlobs) {
        var isDelete = true;
        for (var obj of this.objects) {
          if (blob.left.name === obj.left) {
            isDelete = false;
          }
        }
        if (isDelete) {
          var find = this.blobs.indexOf(blob);
          if (find >= 0) {
            this.blobs.splice(find, 1);
            this.blobs = [...this.blobs];
          }
        }
      }

      // new data add.
      this.newObjects = [];
      for (var newV of newValue) {
        var isAdd = true;
        for (var old of oldValue) {
          if (newV.left === old.left) {
            isAdd = false;
          }
        }
        if (isAdd) {
          this.objects.push(newV);
          this.newObjects.push(newV);

          // call beep
          this.playSound(2, 300);
        }
      }
      if (this.newObjects.length > 0) {
        for (var newobj of this.newObjects) {
          var lres = await this.$api.getBucketsObject2(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getrefreshtoken"],
            this.$store.getters["project/getSelectProject"],
            this.bucket1,
            newobj.left,
            this.prefix1
          );
          var rres = await this.$api.getBucketsObject2(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.bucket2,
            newobj.right,
            this.prefix2
          );
          var leftBlob = lres.data;
          leftBlob.src = await this.blobToSource(leftBlob);
          leftBlob.name = newobj.left;
          var rightBlob = rres.data;
          rightBlob.src = await this.blobToSource(rightBlob);
          rightBlob.name = newobj.right;
          this.blobs.push({ left: leftBlob, right: rightBlob });
        }
      }
    },

    /**
     * Load Left Right Object list.
     * @public
     */
    loadObjects: async function() {
      if (!(this.bucket1 && this.bucket2)) {
        return;
      }
      var lobjects;
      var robjects;
      try {
        var appendPrefix1 = this.cvtAppendPrefix(this.appendPrefix1);
        var appendPrefix2 = this.cvtAppendPrefix(this.appendPrefix2);
        var resultPrefix1 = this.makePrefix(this.prefix1, appendPrefix1);
        var resultPrefix2 = this.makePrefix(this.prefix2, appendPrefix2);
        var left = await this.$api.getBucketsObjects2(
          this.$store.getters["user/getAccessToken"],
          this.$store.getters["user/getRefreshToken"],
          this.$store.getters["project/getSelectProject"],
          this.bucket1,
          this.page,
          this.limited,
          this.order,
          this.filter,
          resultPrefix1
        );
        var right = await this.$api.getBucketsObjects2(
          this.$store.getters["user/getAccessToken"],
          this.$store.getters["user/getRefreshToken"],
          this.$store.getters["project/getSelectProject"],
          this.bucket2,
          this.page,
          this.limited,
          this.order,
          this.filter,
          resultPrefix2
        );
        lobjects = left.result.obj.list;
        robjects = right.result.obj.list;
        var result = [];
        if (lobjects) {
          for (var left of lobjects) {
            if (!left.item.isDir) {
              if (
                left.item.objectName !== null &&
                left.item.objectName !== undefined
              ) {
                if (left.item.objectName.includes("/")) {
                  var temp = left.item.objectName.split("/");
                  left.item.objectName = temp[temp.length - 1];
                }
              }
            }
            var pairRight = this.checkPair(left.item.objectName, robjects);
            if (pairRight) {
              result.push({ left: left.item.objectName, right: pairRight });
            }
          }
        }

        // sort array
        this.editObjectList(
          result.sort(this.dynamicsort("item.lastModified", this.order))
        );
      } catch (e) {
        this.$error(this.$options.name, "loadObjects", e);
        return;
      }
    },


    /**
     * Sorting Array object
     * @date 2020-08-25
     * @param {object name} property
     * @param {order} order
     * @returns {sorted array}
     */
    dynamicsort: function(property, order) {
      var sort_order = 1;
      if (order === "desc-Date") {
        sort_order = -1;
      }
      return function(a, b) {
        if (a[property] < b[property]) {
          return -1 * sort_order;
        } else if (a[property] > b[property]) {
          return 1 * sort_order;
        } else {
          return 0 * sort_order;
        }
      };
    },

    /**
     * Executer for load object.
     * @public
     */
    onLoadObjects: function() {
      this.repeater = setInterval(() => {
        this.loadObjects();
      }, this.interval * 1000);
    },

    /**
     * Destroy interval.
     * @public
     */
    onDestroyRepeater: function() {
      if (this.repeater) {
        clearInterval(this.repeater);
        this.repeater = null;
      }
    },

    /**
     * Open Setting dialog.
     * @public
     */
    openSetting: function() {
      this.showSetting = true;
      this.bucketsSignal = true;
      this.$nextTick().then(() => {
        if (this.bucket1) {
          this.settingValue.left.bucket = this.bucket1;
        }
        if (this.prefix1) {
          this.settingValue.left.prefix = this.prefix1.split("/");
        } else {
          this.prefixes1 = [];
        }
        if (this.appendPrefix1) {
          this.settingValue.left.appendPrefix = this.appendPrefix1;
        }
        if (this.bucket2) {
          this.settingValue.right.bucket = this.bucket2;
        }
        if (this.prefix2) {
          this.settingValue.right.prefix = this.prefix2.split("/");
        } else {
          this.prefixes2 = [];
        }
        if (this.appendPrefix2) {
          this.settingValue.right.appendPrefix = this.appendPrefix2;
        }
        this.settingValue.interval = this.interval;
        this.settingValue.limited = this.limited;
      });
    },

    /**
     * Close setting dialog.
     * @public
     */
    closeSetting: function() {
      this.showSetting = false;
      this.settingValue = Object.assign({}, this.initValue);
    },

    /**
     * Apply setting value.
     * @public
     */
    applySetting: function() {
      this.bucket1 = this.settingValue.left.bucket;
      if (this.settingValue.left.prefix) {
        this.prefix1 = this.cvtPrefixData(this.settingValue.left.prefix);
      }
      if (
        this.settingValue.left.appendPrefix !== null &&
        this.settingValue.left.appendPrefix !== undefined
      ) {
        this.appendPrefix1 = this.settingValue.left.appendPrefix;
      } else {
        this.appendPrefix1 = null;
      }
      this.bucket2 = this.settingValue.right.bucket;
      if (this.settingValue.right.prefix) {
        this.prefix2 = this.cvtPrefixData(this.settingValue.right.prefix);
      }
      if (
        this.settingValue.right.appendPrefix !== null &&
        this.settingValue.right.appendPrefix !== undefined
      ) {
        this.appendPrefix2 = this.settingValue.right.appendPrefix;
      } else {
        this.appendPrefix2 = null;
      }
      this.interval = this.settingValue.interval;
      this.limited = this.settingValue.limited;
      this.saveApi();
      this.closeSetting();
      this.$nextTick().then(() => {
        this.onDestroyRepeater();
        this.onLoadObjects();
      });
    },

    /**
     * Trans Save Component Data To API.
     * @public
     */
    saveApi: function() {
      var component_data = {};
      component_data.interval = this.interval;
      component_data.bucket1 = this.bucket1;
      component_data.bucket2 = this.bucket2;
      component_data.prefix1 = this.prefix1;
      component_data.prefix2 = this.prefix2;
      component_data.prefixes1 = this.prefixes1;
      component_data.prefixes2 = this.prefixes2;
      component_data.appendPrefix1 = this.appendPrefix1;
      component_data.appendPrefix2 = this.appendPrefix2;
      /**
       * Events that occur when component data is stored.
       * @type {Emit}
       * @param {object} - this component data.
       */
      this.$emit("component_data", component_data);
    },

    /**
     * Load Component Data From API.
     * @param {null}
     * @public
     */
    loadApi: function() {
      if (this.component_data) {
        var copy_data = this.$util.cloneObject(this.component_data);
        for (var key in copy_data) {
          switch (key) {
            case "interval": {
              this.interval = copy_data[key];
              break;
            }
            case "bucket1": {
              this.bucket1 = copy_data[key];
              break;
            }
            case "bucket2": {
              this.bucket2 = copy_data[key];
              break;
            }
            case "prefix1": {
              this.prefix1 = copy_data[key];
              break;
            }
            case "prefix2": {
              this.prefix2 = copy_data[key];
              break;
            }
            case "prefixes1": {
              this.prefixes1 = copy_data[key];
              break;
            }
            case "prefixes2": {
              this.prefixes2 = copy_data[key];
              break;
            }
            case "appendPrefix1": {
              this.appendPrefix1 = copy_data[key];
              break;
            }
            case "appendPrefix2": {
              this.appendPrefix2 = copy_data[key];
              break;
            }
          }
        }
      }
    },

    /**
     * Select left bucket or Prefix event.
     * @public
     * @param {string} - type dir, else object.
     * @param {index} - selected dir or object index.
     */
    onSelectLeftBucketPrefix: function(isDir, index) {
      if (isDir !== "dir") {
        this.prefixes1 = [];
        this.settingValue.left.prefix = [];
      } else {
        this.prefixes1.splice(index + 1, 1);
        this.settingValue.left.prefix.splice(index + 1, 1);
      }
      this.leftBucketSignal = true;
    },

    /**
     * Select right bucket or Prefix event.
     * @public
     * @param {string} - type dir, else object.
     * @param {index} - selected dir or object index.
     */
    onSelectRightBucketPrefix: function(isDir, index) {
      if (isDir !== "dir") {
        this.prefixes2 = [];
        this.settingValue.right.prefix = [];
      } else {
        this.prefixes2.splice(index + 1, 1);
        this.settingValue.right.prefix.splice(index + 1, 1);
      }
      this.rightBucketSignal = true;
    },

    /**
     * Convert prefix array to string.
     * @public
     * @param {array} - selected prefix(dir) list.
     */
    cvtPrefixData: function(prefix) {
      var result = "";
      if (!prefix) {
        return null;
      }
      prefix.forEach(dir => {
        // dir 에 빈값이 들어가는 경우 예외처리
        if (!dir.length == 0) {
          result += dir + "/";
        }
      });
      return result;
    },

    /**
     * Make result prefix selected prefix + append Prefix(auto dirs).
     * @public
     * @param {array} - selected prefix list.
     * @param {string} - append Prefix.
     */
    makePrefix: function(prefix, append) {
      if (prefix) {
        if (append) {
          return `${prefix}${append}/`;
        } else {
          return `${prefix}`;
        }
      } else {
        if (append) {
          return `${append}/`;
        } else {
          return null;
        }
      }
    },

    /**
     * Auto convert append prefix.(Now, only datetime.)
     * @public
     * @param {string} - time=#yyyy-#mm-#dd  => 2020-05-06, time=#yy-#m-#d => 20-5-6
     */
    cvtAppendPrefix: function(append) {
      var result = null;
      if (append) {
        result = append;
        if (result.includes("=")) {
          var whitespace = / /gi;
          result = result.replace(whitespace, "");
          var checker = result.split("=")[0];
          if (checker.toLowerCase() === "time") {
            var datetime = new Date();
            var time = /time=/gi;
            var fullYears = /#yyyy/gi;
            var fullMonth = /#mm/gi;
            var fullDay = /#dd/gi;
            var years = /#yy/gi;
            var month = /#m/gi;
            var day = /#d/gi;
            var hour = /#hh/gi;
            result = result.replace(time, "");
            result = result.replace(
              fullYears,
              datetime.getFullYear().toString()
            );
            result = result.replace(
              years,
              datetime
                .getFullYear()
                .toString()
                .slice(-2)
            );
            result = result.replace(
              fullMonth,
              ("0" + (datetime.getMonth() + 1)).slice(-2)
            );
            result = result.replace(
              month,
              (datetime.getMonth() + 1).toString()
            );
            result = result.replace(
              fullDay,
              ("0" + datetime.getDate()).slice(-2)
            );
            result = result.replace(day, datetime.getDate().toString());
            result = result.replace(hour, datetime.getHours().toString());
          }
        }
      }
      return result;
    },

    /**
     * Open data viewer dialog.
     * @public
     * @param {Blob} - object binary.
     */
    openDataViewer: function(blob) {
      this.showDataViewer = true;
      this.showData = blob;
    },

    /**
     * Close data viewer dialog.
     */
    closeDataViewer: function() {
      this.showData = null;
      this.showDataViewer = false;
    },
    playSound: function(repeat, interval) {
      if (this.$refs.alarm) {
        // for(var i=0; repeat; i++){
        this.$refs.alarm.play();
        // }
      } else {
        this.$warn(this.name, "onBeep", "Alarm is not mounted.");
      }
    }
  },
  created() {
    /**
     * 해당 컴포넌트 데이터가 API에 저장되어 있을 경우 로드해서 적용한다.
     */
    this.loadApi();
  },
  mounted() {
    this.$nextTick().then(() => {
      if (this.bucket1 && this.bucket2) {
        /**
         * Mount 되었을 시 선택되어 있는 버켓이 있으면 자동으로 로드해준다.
         */
        this.onLoadObjects();
      }
    });
  },
  beforeDestroy() {
    /**
     * setInterval의 사용을 파기한다.
     */
    this.onDestroyRepeater();
  },
  subscriptions() {
    const $bucketsSignal = this.$watchAsObservable("bucketsSignal", {
      immediate: true
    })
      .pluck("newValue")
      .filter(bucketsSignal => bucketsSignal == true); // if signal is true.
    const $leftBucketSignal = this.$watchAsObservable("leftBucketSignal", {
      immediate: true
    })
      .pluck("newValue")
      .filter(leftBucketSignal => leftBucketSignal == true); // if signal is true.
    const $rightBucketSignal = this.$watchAsObservable("rightBucketSignal", {
      immediate: true
    })
      .pluck("newValue")
      .filter(rightBucketSignal => rightBucketSignal == true); // if signal is true.
    return {
      getBuckets: Observable.combineLatest($bucketsSignal, bucketsSignal => ({
        bucketsSignal
      })).flatMap(({ bucketsSignal }) =>
        this.$api
          .getBuckets(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"]
          )
          .do(res => {
            this.$debug(
              this.$options.name,
              "subscriptions::getBuckets",
              "Response:",
              res
            );
            this.buckets = [];
            for (var bucket of res.result.obj) {
              this.buckets.push(bucket.name);
            }
          })
          .catch(error => {
            this.$error(this.$options.name, "subscriptions::getBuckets", error);
            return Observable.of(null);
          })
          .do(() => {
            this.bucketsSignal = false;
          })
      ),
      getDirs1: Observable.combineLatest(
        $leftBucketSignal,
        leftBucketSignal => ({ leftBucketSignal })
      ).flatMap(({ leftBucketSignal }) =>
        this.$api
          .getBucketsObjects(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.settingValue.left.bucket,
            this.cvtPrefixData(this.settingValue.left.prefix)
          )
          .do(res => {
            this.$debug(
              this.$options.name,
              "subscriptions::getDirs1",
              "Response:",
              res
            );
            var dirs = [];
            for (var obj of res.result.obj) {
              if (obj.item.isDir) {
                if (obj.item.objectName) {
                  obj.item.objectName = obj.item.objectName.substring(
                    0,
                    obj.item.objectName.length - 1
                  );
                  if (obj.item.objectName.includes("/")) {
                    var temp = obj.item.objectName.split("/");
                    obj.item.objectName = temp[temp.length - 1];
                  }
                  dirs.push(obj.item.objectName);
                }
              }
            }
            if (dirs.length > 0) {
              this.prefixes1.push(dirs);
              this.settingValue.left.prefix.length = this.prefixes1.length;
            }
          })
          .catch(error => {
            this.$error(this.$options.name, "subscriptions::getDirs1", error);
            return Observable.of(null);
          })
          .do(() => {
            this.leftBucketSignal = false;
          })
      ),
      getDirs2: Observable.combineLatest(
        $rightBucketSignal,
        rightBucketSignal => ({ rightBucketSignal })
      ).flatMap(({ rightBucketSignal }) =>
        this.$api
          .getBucketsObjects(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.settingValue.right.bucket,
            this.cvtPrefixData(this.settingValue.right.prefix)
          )
          .do(res => {
            this.$debug(
              this.$options.name,
              "subscriptions::getDirs2",
              "Response:",
              res
            );
            var dirs = [];
            for (var obj of res.result.obj) {
              if (obj.item.isDir) {
                if (obj.item.objectName) {
                  obj.item.objectName = obj.item.objectName.substring(
                    0,
                    obj.item.objectName.length - 1
                  );
                  if (obj.item.objectName.includes("/")) {
                    var temp = obj.item.objectName.split("/");
                    obj.item.objectName = temp[temp.length - 1];
                  }
                  dirs.push(obj.item.objectName);
                }
              }
            }
            if (dirs.length > 0) {
              this.prefixes2.push(dirs);
              ++this.settingValue.right.prefix.length;
            }
          })
          .catch(error => {
            this.$error(this.$options.name, "subscriptions::getDirs2", error);
            return Observable.of(null);
          })
          .do(() => {
            this.rightBucketSignal = false;
          })
      )
    };
  }
};
</script>

<style scoped>
.viewerMain {
  width: 100%;
  height: 100%;
}
.viewerCard {
  border: 1px solid;
  margin-bottom: 5px;
  width: 100%;
  max-height: calc(100% - 30px);
  overflow: auto;
}
.left {
  border: 1px solid blue;
}
.right {
  border: 1px solid red;
}
.pane {
  display: inline-block;
  background-color: transparent !important;
}
.viewer {
  width: 100%;
  height: 100px !important;
  max-height: 100px !important;
  padding: 5px;
  overflow: hidden;
  border-bottom: 1px solid;
}
.viewer--image {
  object-fit: scale-down !important;
  height: 100%;
  max-height: 90px !important;
  overflow-x: auto;
  overflow-y: hidden;
}
.viewer--image:hover {
  cursor: pointer;
}
.viewer--audio {
  width: 100%;
  height: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  max-height: 90px !important;
}
.viewer--video {
  object-fit: scale-down;
  overflow-x: auto;
  overflow-y: hidden;
  width: 100%;
  height: 100%;
  max-height: 90px !important;
}
.viewer--text {
  /* white-space: pre-line; */
  overflow: auto;
  font-size: 12px;
  width: 100%;
  height: 100%;
  max-height: 90px !important;
}
.viewer--text:hover {
  cursor: pointer;
}
.viewer--pdf {
  overflow-x: auto;
  overflow-y: hidden;
  height: 100%;
  max-height: 90px !important;
}
.divider {
  margin: 0;
  padding: 0;
  width: 100%;
}
.settingZone {
  padding: 0px !important;
}
.subTitle {
  padding: 0px !important;
}
.timerSetting {
  margin: 5px;
  padding: 5px;
}
.leftSetting {
  margin: 5px;
}
.rightSetting {
  margin: 5px;
}
.loadmessage {
  color: greenyellow;
}
.emptymessage {
  color: orange;
}
.dataViewerZone {
  position: absolute;
  top: 10%;
  left: 10%;
  width: 80%;
  height: 80%;
}
.dataViewerZone__image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.dataViewerZone__video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.dataViewerZone__pdf {
  width: 100%;
  height: 100%;
}
.dataViewerZone__text {
  width: 100%;
  height: 100%;
  padding: 10px;
  overflow-y: auto;
  border: 1px solid;
}
.dataViewerZone__text >>> pre {
  max-width: 100%;
  white-space: pre-line;
  word-wrap: break-word;
}
.margin-10 {
  margin: 10px;
}
</style>
