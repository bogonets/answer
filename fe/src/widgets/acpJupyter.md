<details>
<summary>Example code</summary>
<div>

```html
  <div style="width: 100%; height: 100%;">
    <acp-jupyter
    @component_data="saveData($event)"
    :component_data="loadData"
    ></acp-jupyter>
  </div>
```
```javascript
import acpJupyter from "@/widget/acpJupyter.vue"; // when use component`s local.
export default {
  props:{

  },
  components:{
    acpJupyter
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

Core의 Jupyter를 출력한다.

## 흐름도
처음에는 프로젝트 목록 다이얼로그에서 프로젝트를 생성한 후, 프로젝트 목록에서 프로젝트를 선택하여 연다.

원하는 Jupter작업을 할 수 있으며, Pip 다이얼로그를 통해 Pip 설치를 할 수 있다.


</div>
</details>
