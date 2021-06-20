<details>
<summary>Example code</summary>
<div>

```html
  <div style="width: 100%; height: 100%;">
    <a-json-field
    :json="jsonData"
    :tabSize="tabSize"
    :resultObject="resultObject"
    :readonly="readonly"
    :resize="resize.vertical"
    @transData="onChanged"></a-json-field>
  </div>
```
```javascript
import aJsonField from "@/components/Input/aJsonField.vue"; // when use component`s local.
export default {
  props:{

  },
  components:{
    aJsonField
  },
  data(){
    return {
      jsonData: { test: "test1", test2: "test2" },
      tabSize: 4,
      resultObject: true,
      readonly: false,
      resize: {vertical: "vertical", horizontal: "horizontal", none: "none", both: "both"}
    }
  },
  methods:{
    onChanged: function ($event) {
      if (typeof $event === "object") {
        this.jsonData = $event;
      } else if (typeof $event === "string") {
        this.jsonData = JSON.parse($event);
      }
    }
  }
}
```

</div>
</details>

<details>
<summary>HISTORY</summary>
<div>

### v1.0.0
Add Copy func.

### v0.9.0
Remake base answer`s json field.

### v0.8.0
make base answer`s json field.

</div>
</details>
