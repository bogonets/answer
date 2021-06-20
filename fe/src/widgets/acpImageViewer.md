<details>
<summary>Example code</summary>
<div>

```html
  <div style="width: 100%; height: 100%;">
    <acp-image-viewr
    @component_data="saveData($event)"
    :component_data="loadData"
    ></acp-image-viewr>
  </div>
```
```javascript
import acpImageViewer from "@/widget/acpImageViewer.vue"; // when use component`s local.
export default {
  props:{

  },
  components:{
    acpImageViewer
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
그래프 설정의 태스크 람다 중 이미지(JPEG, PNG)를 OUTPUT으로 뱉는 람다의 이미지를 보여준다.


## 흐름도
태스크와 람다, 아웃풋 슬롯을 설정하여
setInterval을 통하여 이미지를 API(CORE->API)로부터 불러와서 출력한다.

타이머값이 -1인 경우 수동으로 갱신해준다.


</div>
</details>
