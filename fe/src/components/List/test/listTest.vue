<template>
  <div style="width: 100%; height: 100%;">
    <a-list 
    :header="header"
    :lists="testLists"
    :i18nHaeder="false"
    :i18nMain="false"
    :i18nSub="false"
    :i18nExpand="false"
    @headerClick="onHeaderClick($event)"
    @mainClick="onMainClick($event)"
    @mainGroupClick="onMainGroupClick($event)"
    @subClick="onSubClick($event)"
    @expandClick="onExpandClick($event)">
    </a-list>
  </div>
</template>
<script>
// AnswerList(alist.vue) v 0.9.0
// HISTORY 0.8.0 -> 0.9.0 {
// `Add Header iocn`
// }
import aList from "@/components/List/aList.vue";
export default {
  name: "listTest",
  props:{
  },
  components:{
    aList
  },
  data(){
    return {
      header: { 
        title: 'project', 
        // icon: 'person'
        icon: undefined
      },
      testLists: [
        {
          title: 'list1',
          icon: 'person',
          active: true
        },
        {
          title: 'list2', // title or name (필수).
          icon: 'person', // undefined: 아이콘 자리 비워져있음 (선택).
          submenu: [ // list group를 생성하기 위한 조건 (선택). 
            {
              name: 'sublist1', // group item의 title or name (필수).
              icon: 'settings' // undefined: 아이콘 자리 비워져있음 (선택).
            },
            {
              name: 'sublist2',
              icon: 'settings'
            }
            ],
          expands: [ // submenu 이외에 추가할 또다른 submenu
            {
              name: 'expand1',  // name or title (필수).
              icon: 'add' // (선택).
            }
          ],
          active: true // list group으로 사용할 시 (필수). 일반적인 리스트로 사용할 시 필요 없는 값 (선택).
        },
        {
          title: 'list2-2', // title or name (필수).
          icon: 'dashboard', // undefined: 아이콘 자리 비워져있음 (선택).
          submenu: [],
          expands: [ // submenu 이외에 추가할 또다른 submenu
            {
              name: 'expand1',  // name or title (필수).
              icon: 'add' // (선택).
            }
          ],
          active: false // list group으로 사용할 시 (필수). 일반적인 리스트로 사용할 시 필요 없는 값 (선택).
        },
        {
          title: 'list3',
          icon: 'person',
          active: true
        },
        {
          title: 'list4',
          icon: 'person',
          active: true
        }
      ]
    }
  },
  computed:{
    
  },
  methods:{
    onHeaderClick: function (event) {
      var name = event.title || event.name;
      this.$debug(this.$options.name, "HEADER CLICK !! data name = ", name);
    },

    onMainClick: function (event) {
      var name = event.title || event.name;
      this.$debug(this.$options.name, "MAIN CLICK !! data name = ", name);
    },

    onMainGroupClick: function (event) {
      var name = event.title || event.name;
      this.$debug(this.$options.name, "MAINGROUP CLICK !! data name = ", name);
    },

    onSubClick: function (event) {
      var name = event.title || event.name;
      this.$debug(this.$options.name, "SUB CLICK !! data name = ", name);
    },

    onExpandClick: function (event) {
      var name = event.title || event.name;
      this.$debug(this.$options.name, "EXPAND CLICK !! data name = ", name);
    },
  },
  created(){

  },
  mounted(){
  }
}
</script>
<style scoped>

</style>