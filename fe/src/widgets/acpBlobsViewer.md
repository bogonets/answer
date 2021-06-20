<details>
<summary>Example code</summary>
<div>

```html
  <div style="width: 100%; height: 100%;">
    <acp-blobs-viewer
    @component_data="saveData($event)"
    :component_data="loadData"
    ></acp-blobs-viewer>
  </div>
```
```javascript
import acpBlobsViewer from "@/widget/acpBlobsViewer.vue"; // when use component`s local.
export default {
  props:{

  },
  components:{
    acpBlobsViewer
  },
  data(){
    return {
      loadData: // load from API.
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

## 흐름도
왼쪽과 오른쪽의 버켓과 프리픽스(Dir)를 선택하여
Object의 리스트를 받아온다.

그리고 받아온 Object 리스트를 비교하여 파일명끼리 짝을 이루는 것이 한 라인이 된다.

짝을 이룬 것끼리 리스트가되어 오래되서 없는 데이터는 삭제되고 새로 생긴 데이터는 추가된다.

그리고 새로 생긴 데이터의 Object(Binary)파일을 불러와 UI에 표출한다.

setInverval을 사용하여 반복적으로 불러온다.


</div>
</details>
