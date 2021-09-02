<template>
  <div>
    <grid-view>
    </grid-view>
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
