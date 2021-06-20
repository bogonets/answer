<details>
<summary>Example code</summary>
<div>

```html
    <simple-video-player
    ref="simpleVideo"
    :src="'https://www.w3schools.com/html/mov_bbb.mp4'"
    :controls="true"
    :autoplay="true"
    :loop="true"
    @created="onCreated"
    @beforeplay="onBefore"
    @play="onPlay"
    @afterplay="onAfter"
    @error="onError"></simple-video-player>
```

```javascript
<script>
import SimpleVideoPlayer from "@/components/Video/SimpleVideoPlayer.vue";
export default {
  props:{

  },
  components:{
    SimpleVideoPlayer
  },
  data(){
    return {

    }
  },
  computed:{

  },
  methods:{
    onCreated: function (event) {
      console.log("Created", event);
    },
    onBefore: function (event) {
      console.log("Before", event);
    },
    onPlay: function (event) {
      console.log("Play", event);
    },
    onAfter: function (event) {
      console.log("After", event);
    },
    onError: function (event) {
      console.log("Error", event);
    }
  }
}
</script>
```
</div>
</details>
