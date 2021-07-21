<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="8" sm="6" md="6" lg="6" xl="4">

        <div class="d-block mb-16">
          <title-logo
              max-width="300px"
              max-height="300px"
          ></title-logo>
        </div>

        <v-btn block text rounded disabled class="d-block my-4 secondary">
          {{ versionText }}
        </v-btn>

        <v-btn
            block
            text
            rounded
            class="d-block my-4 secondary"
            @click="onClickDocumentation"
        >
          {{ 'Show document' }}
        </v-btn>

        <v-btn
            block
            text
            rounded
            class="d-block my-4 secondary" @click="onClickVender"
        >
          {{ 'GoTo bogonets' }}
        </v-btn>

      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import TitleLogo from '@/components/TitleLogo.vue';

@Component({
  components: {
    TitleLogo,
  }
})
export default class AboutPage extends Vue {
  get versionText(): string {
    return 'Version: 2.0.0';
  }

  onClickDocumentation() {
  }

  onClickVender() {
  }
}
</script>
