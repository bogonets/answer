<i18n lang="yaml">
en:
  kanban: "Kanban"

ko:
  kanban: "간반보드"
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Kanban"></breadcrumb-main>
    <v-divider></v-divider>

    <div class="d-flex flex-row">
      <div ref="bar1" style="width: 200px; height: 400px;">
        <v-card
            class="mx-auto"
            max-width="344"
            outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <div class="text-overline mb-4">
                OVERLINE
              </div>
              <v-list-item-title class="text-h5 mb-1">
                Headline 5
              </v-list-item-title>
              <v-list-item-subtitle>Greyhound divisely hello coldly fonwderfully</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-avatar
                tile
                size="80"
                color="grey"
            ></v-list-item-avatar>
          </v-list-item>

          <v-card-actions>
            <v-btn
                outlined
                rounded
                text
            >
              Button
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>

      <div ref="bar2" style="width: 200px; height: 400px;">
        <v-card
            class="mx-auto"
            max-width="344"
            outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <div class="text-overline mb-4">
                OVERLINE
              </div>
              <v-list-item-title class="text-h5 mb-1">
                Headline 5
              </v-list-item-title>
              <v-list-item-subtitle>Greyhound divisely hello coldly fonwderfully</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-avatar
                tile
                size="80"
                color="grey"
            ></v-list-item-avatar>
          </v-list-item>

          <v-card-actions>
            <v-btn
                outlined
                rounded
                text
            >
              Button
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </div>

  </v-container>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import createDragula, {Drake} from 'dragula';

@Component({
  components: {
    BreadcrumbMain,
  }
})
export default class MainKanban extends VueBase {
  @Ref()
  bar1!: HTMLDivElement;

  @Ref()
  bar2!: HTMLDivElement;

  loading = false;

  dragula!: Drake;

  mounted() {
    this.dragula = createDragula([this.bar1, this.bar2]);
  }
}
</script>
