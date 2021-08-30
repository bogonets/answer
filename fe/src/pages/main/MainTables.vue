<template>
  <div>
    <view-port>
      <grid-view>
      </grid-view>
    </view-port>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import GridView from '@/components/DynamicTable/GridView.vue';

@Component({
  components: {
    ViewPort,
    GridView,
  }
})
export default class MainTables extends VueBase {
}
</script>
