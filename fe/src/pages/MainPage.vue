<template>
  <v-app>
    <main-title-bar>
    </main-title-bar>

    <v-main>
      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import MainTitleBar from '@/components/MainTitleBar.vue';

@Component({
  components: {
    MainTitleBar,
  }
})
export default class MainPage extends Vue {
  mounted() {
    this.$router.push('/main/projects');
  }
}
</script>
