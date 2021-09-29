<i18n lang="yaml">
en:
  groups: "Groups"
  projects: "Projects"

ko:
  groups: "Groups"
  projects: "Projects"
</i18n>

<template>
  <v-container>

    <span class="ml-2 text--secondary text-subtitle-2">
      {{ $t('groups') }}
    </span>
    <v-divider></v-divider>
    <table-groups
        hide-filter-input
        hide-new-item-button
        hide-action-edit
        hide-action-move
        clickable-row
        :loading="loading"
        :items="groups"
        @click:row="onClickGroupRow"
    ></table-groups>

    <span class="ml-2 text--secondary text-subtitle-2">
      {{ $t('projects') }}
    </span>
    <v-divider></v-divider>
    <table-projects
        hide-filter-input
        hide-new-item-button
        hide-action-edit
        hide-action-move
        clickable-row
        :loading="loading"
        :items="projects"
        @click:row="onClickProjectRow"
    ></table-projects>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import TableGroups from '@/components/TableGroups.vue';
import TableProjects from '@/components/TableProjects.vue';
import {GroupA} from "@/packet/group";
import {ProjectA} from "@/packet/project";

@Component({
  components: {
    TableGroups,
    TableProjects,
  }
})
export default class Root extends VueBase {
  loading = false;
  groups = [] as Array<GroupA>;
  projects = [] as Array<ProjectA>;

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

      this.groups = await this.$api2.getMainGroups();
      this.projects = await this.$api2.getMainProjects();
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  onClickGroupRow(item: GroupA) {
    this.moveToGroupProjects(item.slug);
  }

  onClickProjectRow(item: ProjectA) {
    this.moveToMain(item.group_slug, item.project_slug);
  }
}
</script>
