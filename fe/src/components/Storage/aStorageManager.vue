<template>
  <v-card class="setting--card">
    <v-toolbar dense height="35">
      <template v-if="selectBucket">
        <v-btn small icon style="margin-right: 10px;" @click="showBucketList"><v-icon>fas fa-arrow-left</v-icon></v-btn>
        <a @click="onFlowBucket"><i class="fas fa-database spanSlash"></i>{{ selectBucket.name }}</a>
        <span class="spanSlash">{{ `/` }}</span>
      </template>
      <template v-else>
        <i class="far fa-question-circle" style="color: burlywood"></i><span style="color: burlywood;" class="spanSlash">{{ $t('select_project_storage') }}</span>
      </template>
      <template v-if="selectPrefix">
        <template v-for="(prefix, index) in selectPrefix">
          <a @click="onFlowPrefix(prefix)" :key="index"><i :class="`${prefix.icon} spanSlash`"></i>{{ prefix.objectName }}</a>
          <span class="spanSlash" :key="prefix.objectName + index">{{ `/` }}</span>
        </template>
      </template>
      <template v-if="selectObject">
        <span @click="onFlowObject"><i :class="`${selectObject.icon} spanSlash`"></i>{{ selectObject.objectName }}</span>
      </template>
    </v-toolbar>
    <v-card-text class="setting--table">
      <bucket-table
      v-if="!selectBucket"
      ref="bucketTable"
      @selectBucket="onSelectBucket">
      </bucket-table>
      <object-table
      v-else
      ref="objectTable"
      :parentBucket.sync="selectBucket"
      @selectPrefix="onSelectPrefix"
      @selectObject="onSelectObject">
      </object-table>
    </v-card-text>
  </v-card>
</template>

<script>
import BucketTable from "@/components/Table/aBucketTable.vue";
import ObjectTable from "@/components/Table/aBucketsObjectTable.vue";
export default {
  props:{

  },
  components:{
    BucketTable,
    ObjectTable
  },
  data(){
    return {
      selectBucket: null,
      selectPrefix: [],
      selectObject: null
    }
  },
  computed:{

  },
  methods:{
    showBucketList: function () {
      this.selectBucket = null;
      this.selectPrefix = null;
      this.selectObject = null;
    },
    onSelectBucket: function (bucketName) {
      this.selectBucket = bucketName;
    },
    onSelectPrefix: function (prefixes) {
      if (!prefixes) {
        return;
      }
      this.selectPrefix = [...prefixes];
    },
    onSelectObject: function (object) {
      this.selectObject = object;
    },
    onFlowBucket: function () {
      this.selectPrefix = null;
      this.selectObject = null;
      this.$refs.objectTable.reLinkPrefix(this.selectPrefix, true);
    },
    onFlowPrefix: function (prefix) {
      var find = this.selectPrefix.indexOf(prefix);
      this.selectPrefix.splice(find + 1);
      this.$refs.objectTable.reLinkPrefix(this.selectPrefix, true);
      this.selectObject = null;
    },
    onFlowObject: function () {
    },
  },
  created(){

  },
  mounted(){

  }
}
</script>

<style scoped>
.setting--card {
  width: 100%;
  height: 100%;
}
.setting--table {
  position: absolute;
  top: 35px;
  height: calc(100% - 35px);
  padding: 0px;
}
.spanSlash {
  margin-left: 5px;
  margin-right: 5px;
}
.icon {
  margin-right: 5px;
}
</style>
