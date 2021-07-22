<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md6>
          <af-signup-form ref="signup_comp" @close="onClose" @success="onSuccess"></af-signup-form>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import afSignupForm from "@/components/Form/afSignupForm.vue";
// import afSignupForm from "@/components/Form/test/afSignupFormTest.vue"; 
export default {
  name: "SignupPage",
  props:{
  },
  components:{
    afSignupForm
  },
  data(){
    return {
    }
  },
  computed:{
  },
  methods:{
    onClose: function () {
      this.$router.push(this.$page.login);
    },
    onSuccess: function () {
      this.$router.push(this.$page.login).catch(err => console.info('#####', err));
    }
  },
  created(){
  },
  mounted(){
  }
}
</script>
<style scoped lang="">

</style>