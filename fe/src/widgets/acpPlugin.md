<details>
<summary>Example code</summary>
<div>

```html
  <div style="width: 100%; height: 100%;">
    <acp-plugin
    @component_data="saveData($event)"
    :component_data="loadData"
    ></acp-plugin>
  </div>
```
```javascript
import acpPlugin from "@/widget/acpPlugin.vue"; // when use component`s local.
export default {
  props:{

  },
  components:{
    acpPlugin
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

Iframe을 통해 웹사이트나 로컬파일(HTML, PDF 등)을 출력하여 보여주는 위젯.

## 흐름도
URL을 설정하여 Iframe을 통해 출력한다.

로컬파일을 출력하는 경우 파일 탐색기에서 파일을 선택하여 파일을 URL로 변경하여 출력한다.

</div>
</details>
