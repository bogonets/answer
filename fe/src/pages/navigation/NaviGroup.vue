<i18n lang="yaml">
en:
  group:
    unknown: '[Unknown Group]'
  projects: 'Projects'
  members: 'Members'
  settings: 'Settings'

ko:
  group:
    unknown: '[알수없는 그룹]'
  projects: '프로젝트'
  members: '회원 관리'
  settings: '그룹 설정'
</i18n>

<template>
  <v-navigation-drawer
    app
    clipped
    permanent
    stateless
    touchless
    :mini-variant.sync="mini"
  >
    <v-list nav dense>
      <!-- User Profile -->
      <v-list-item link @click.stop="onClickFoldNavigation">
        <v-list-item-icon>
          <v-avatar color="accent" size="24">{{ groupAvatar }}</v-avatar>
        </v-list-item-icon>
        <v-list-item-title>
          {{ groupSlug }}
        </v-list-item-title>
        <v-btn icon @click.stop="onClickFoldNavigation">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list-item-group
        mandatory
        color="primary"
        :value="index"
        @change="onChangeIndex"
      >
        <v-list-item link @click.stop="onClickProjects">
          <v-list-item-icon>
            <v-icon>mdi-clipboard-check-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('projects') }}
          </v-list-item-title>
        </v-list-item>

        <div v-if="showMembers || showSettings">
          <v-divider></v-divider>

          <v-list-item v-if="showMembers" link @click.stop="onClickMembers">
            <v-list-item-icon>
              <v-icon>mdi-account-group</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('members') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-if="showSettings" link @click.stop="onClickSettings">
            <v-list-item-icon>
              <v-icon>mdi-cog-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('settings') }}
            </v-list-item-title>
          </v-list-item>
        </div>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {
  PERM_SLUG_RECC_DOMAIN_MEMBER_VIEW,
  PERM_SLUG_RECC_DOMAIN_SETTING_VIEW,
} from '@recc/api/dist/packet/permission';

@Component
export default class MainAccount extends VueBase {
  index = 0;
  mini = false;
  permissions = [] as Array<string>;

  get groupSlug(): string {
    const name = this.$route.params.group;
    if (name) {
      return name;
    }
    return this.$t('group.unknown').toString();
  }

  get groupAvatar(): string {
    const name = this.$route.params.group;
    if (name) {
      return name[0].toUpperCase();
    }
    return '?';
  }

  private hasPermission(perm: string) {
    return this.permissions.includes(perm);
  }

  get showMembers() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_MEMBER_VIEW);
  }

  get showSettings() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_SETTING_VIEW);
  }

  created() {
    (async () => {
      await this.requestSetup();
    })();
  }

  async requestSetup() {
    try {
      const group = this.$route.params.group;
      this.permissions = await this.$api2.getSelfPermissionsPgroup(group);
    } catch (error) {
      this.toastRequestFailure(error);
      this.moveToBack();
    }
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  onChangeIndex(index: number) {
    this.index = index;
  }

  onClickProjects() {
    this.moveToGroupProjects(this.$route.params.group);
  }

  onClickMembers() {
    this.moveToGroupMembers(this.$route.params.group);
  }

  onClickSettings() {
    this.moveToGroupSettings(this.$route.params.group);
  }
}
</script>
