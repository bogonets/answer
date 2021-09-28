<template>
  <v-container>
    <table-groups
        hide-action-edit
        hide-action-move
        clickable-row
        :loading="loading"
        :items="items"
        @click:new="onClickNew"
        @click:row="onClickRow"
    ></table-groups>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import TableGroups from '@/components/TableGroups.vue';
import {GroupA} from "@/packet/group";

@Component({
  components: {
    TableGroups,
  }
})
export default class Root extends VueBase {
  loading = false;
  items = [] as Array<GroupA>;

  created() {
    if (!this.$localStore.alreadySession) {
      this.moveToSignin();
      return;
    }

    this.requestSetup();
  }

  requestSetup() {
    this.loading = true;
    (async () => {
      await this._setup();
    })();
  }

  async _setup() {
    try {
      const user = await this.$api2.getSelf();
      this.$sessionStore.permissionAdmin = user.is_admin || false;

      this.items = await this.$api2.getMainGroups();
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  onClickNew() {
    this.moveToRootGroupsNew();
  }

  onClickRow(item: GroupA) {
    this.moveToGroupProjects(item.slug);
  }
}
</script>
