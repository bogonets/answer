<i18n lang="yaml">
en:
  menu:
    connect: "Connect"

ko:
  menu:
    connect: "연결"
</i18n>

<template>
  <div class="d-flex flex-column fill-height">
    <div class="d-flex flex-wrap main">
      <v-card
          v-for="i in maxCards"
          :key="i"
          color="grey"
          outlined
          tile
          :style="cardStyle(i)"
          @contextmenu="onShowContextMenu(i, $event)"
      >
        <media-player></media-player>
      </v-card>
    </div>

    <v-footer>
      <v-system-bar absolute>
        <v-icon>mdi-application</v-icon>
        <v-spacer></v-spacer>
        <v-btn icon small max-width="22px" max-height="22px" @click="onClickCloseFooter">
          <v-icon small class="ma-0">mdi-close</v-icon>
        </v-btn>
      </v-system-bar>
      <v-sheet :height="footerHeight"></v-sheet>
    </v-footer>

    <v-menu
        v-model="showContextMenu"
        :position-x="contextMenuPositionX"
        :position-y="contextMenuPositionY"
        absolute
        offset-y
    >
      <v-list dense>
        <v-list-item @click="onClickConnect">
          <v-list-item-title>{{ $t('menu.connect') }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import MediaPlayer from '@/media/MediaPlayer.vue';

@Component({
  components: {
    ViewPort,
    MediaPlayer,
  }
})
export default class MainVmsLive extends VueBase {
  readonly footerHeight = 200;

  maxCards = 9;
  showFooter = true;

  showContextMenu = false;
  contextMenuPositionX = 0;
  contextMenuPositionY = 0;

  cardStyle(index: number) {
    return {
      width: '33.333%',
      height: '33.333%',
    };
  }

  onClickConnect() {
  }

  onShowContextMenu(index: number, event) {
    event.preventDefault();
    this.showContextMenu = false;
    this.contextMenuPositionX = event.clientX;
    this.contextMenuPositionY = event.clientY;
    this.$nextTick(() => {
      this.showContextMenu = true;
    })
  }

  onClickCloseFooter() {
    this.showFooter = false;
  }
}
</script>

<style lang="scss" scoped>
.fill-height {
  height: 100%;
}

.main {
  flex: auto;
}
</style>
