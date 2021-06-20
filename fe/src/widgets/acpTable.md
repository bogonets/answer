<details>
<summary>Example code</summary>
<div>

```html
  <div style="width: 100%; height: 100%;">
    <acp-table
    :resizeTrigger="trigger"
    @component_data="saveData($event)"
    :component_data="loadData"
    ></acp-table>
  </div>
```
```javascript
import acpTable from "@/widget/acpTable.vue"; // when use component`s local.
export default {
  props:{

  },
  components:{
    acpBlobsViewer
  },
  data(){
    return {
      loadData: {},// load from API.
      trigger: true// true or false.
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

## 특징
헤더가 두개 좌측과 우측으로 되어있는 테이블이다.

## 사용하는 곳.
대시보드에서 사용하는 위젯.(한국철강에서 사용되었다.)

## 흐름도
설정 다이얼로그에서 어떤 데이터를 가져올 지 선택한 후 해당 데이터를 

일정 시간 간격만큼 요청하여 데이터를 갱신한다.

## 데이터 포맷
```javascript
{
    "header1-label": "header1",
    "header1": ["A", "B", "C"],
    "header2-label": "header2",
    "header2": ["X", "Y"],
    "data-label": "$",
    "data": [
        [10, 20, 30],
        [10, 20, 30]
    ]
}
```

결과 예시.

| |A|B|C|
|:---|:---|:---|:---|
|*X*|10|20|30|
|*Y*|10|20|30|



</div>
</details>
