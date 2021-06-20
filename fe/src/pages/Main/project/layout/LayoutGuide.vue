<template>
  <div class="main">
    <v-container fluid fill-height>
      <v-col cols="12">
        <v-row :align="'center'" :justify="'center'">
          <v-btn
            v-if="operator"
            icon
            @click="onAddLayoutDialog"
            style="width: 100px; height: 100px"
          >
            <v-icon
              ref="opener"
              style="position: absolute; color: grey"
              size="80"
              >dashboard</v-icon
            >
            <v-icon
              ref="opener2"
              style="position: absolute; top: 10px; left: 65px; color: orange; border: 1px solid orange; border-radius: 100% 100% 100% 100%"
              size="30"
              >add</v-icon
            >
          </v-btn>
        </v-row>
        <v-row :align="'center'" :justify="'center'" class="text-xs-center">
          <span>{{ $t("have_no_layout") }}</span>
        </v-row>
        <v-row v-if="operator" :align="'center'" :justify="'center'">
          <span>{{ $t("click_icon_addlayout") }}</span>
        </v-row>
      </v-col>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "LayoutGuide",
  props: {},
  components: {},
  data() {
    return {
      operator: Boolean,
    };
  },
  computed: {},
  methods: {
    onAddLayoutDialog: function() {
      this.$store.commit("drawer/setOpenAddLayout", { bool: true });
    },
  },
  created() {
    this.operator = this.$store.getters["project/isOperator"];
  },
  mounted() {
    this.$nextTick(() => {
      var opener = this.$refs.opener;
      var opener2 = this.$refs.opener2;
      if (opener) {
        opener.$el.animate(
          [
            // keyframes
            { transform: "scale(1)" },
            { transform: "scale(1.5)" },
            { transform: "scale(1)" },
          ],
          {
            // timing options
            duration: 800,
            iterations: 3,
          }
        );
      }
      if (opener2) {
        opener2.$el.animate(
          [
            // keyframes
            { transform: "rotate(45deg)" },
            { transform: "rotate(90deg)" },
            { transform: "rotate(135deg)" },
            { transform: "rotate(180deg)" },
            { transform: "rotate(225deg)" },
            { transform: "rotate(270deg)" },
            { transform: "rotate(315deg)" },
            { transform: "rotate(360deg)" },
          ],
          {
            // timing options
            duration: 800,
            iterations: 3,
          }
        );
      }
    });
  },
  beforeDestroy() {},
};
</script>

<style scoped>
.main {
  width: 100%;
  height: 100%;
}
</style>
