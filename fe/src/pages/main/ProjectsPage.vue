<template>
  <a-project-table></a-project-table>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import aProjectTable from '@/components/Table/aProjectTable.vue';

@Component({
  components: {
    aProjectTable,
  }
})
export default class ProjectsPage extends Vue {
  // EMPTY.
}
</script>
