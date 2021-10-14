<i18n lang="yaml">
en:
  menu: "VMS Menu"
  live: "Live"
  devices: "Devices"

ko:
  menu: "VMS 메뉴"
  live: "실시간"
  devices: "장치 목록"
</i18n>

<template>
  <div>
    <v-navigation-drawer
        app
        right
        clipped
        permanent
        stateless
        touchless
        :mini-variant.sync="mini"
    >
      <v-list nav dense>

        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-icon>
            <v-icon>mdi-menu</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('menu') }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item-group
            mandatory
            color="primary"
            v-model="index"
        >
          <v-list-item link @click.stop="onClickLive">
            <v-list-item-icon>
              <v-icon>mdi-broadcast</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('live') }}
            </v-list-item-title>
          </v-list-item>

        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <view-port>
      <router-view>
      </router-view>
    </view-port>
  </div>
</template>

<script lang="ts">
import {Component, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import mainNames from '@/router/names/main';

@Component({
  components: {
    ViewPort,
  }
})
export default class MainVms extends VueBase {
  mini = false;
  index = 0;

  get hasAdminPermission(): boolean {
    return this.$localStore.user.is_admin || false;
  }

  @Watch('$route')
  onChangeRoute() {
    const name = this.$route.name;
    if (name === mainNames.mainVmsLive) {
      this.index = 0;
    } else {
      this.index = -1;
    }
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  onClickLive() {
    this.moveToMainVmsLive();
  }
}
</script>
