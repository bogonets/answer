<details>
<summary>Example code</summary>
<div>

```html
  <div style="width: 100%; height: 100%;">
    <acp-vod-player
    @component_data="saveData($event)"
    :component_data="loadData"
    :edit="edit"
    ></acp-vod-player>
  </div>
```
```javascript
import acpVodPlayer from "@/widget/acpVodPlayer.vue"; // when use component`s local.
export default {
  props:{

  },
  components:{
    acpVodPlayer
  },
  data(){
    return {
      loadData: // load from API.
      edit: true,
    }
  },
  methods:{
    saveData () {
      // save to API.
    }
  }
}
```

</div>
</details>

<details>
<summary>Descriptions</summary>
<div>

## 사용하는 곳.
대시보드에서 사용하는 위젯.

WebRTC의 스트림 데이터를 출력한다.

## 흐름도
설정에서 RTC URL을 설정하여 medias데이터를 받는다 (audios, videos, datas) 각 받을 데이터를 선택한 후,

(RTC URL은 람다에서 설정한 주소로 받아올 수 있으며, 수동입력 버튼을 클릭하여 수동으로 입력할 수 있다.)

ICE Candidatae 를 받고 자동으로 선택하여 WebRTC서버에 연결된다.

연결이 끊어 졌을 시 재연결 회수와 재연결 타이머를 설정 창에서 설정할 수 있다.

현재 datas로 받은 data는 Painter를 통해 그려주기 위한 데이터로 사용되고 있다.


</div>
</details>
