<details>
<summary>Example code</summary>
<div>

```html
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
```
```javascript
function onHeaderClick ($event) {
  // $event - type: object - header`s data.
  // Your Code.
}
function onMainClick ($event) {
  // $event - type: object - main item`s data.
  // Your Code.
}
function onMainGroupClick ($event) {
  // $event - type: object - main group item`s data.
  // Your Code.
}
function onSubClick ($event) {
  // $event - type: object - sub item and sub item`s parent item data.
  // Your Code.
}
function onExpandClick ($event) {
  // $event - type: object - expand item and sub item`s parent item data.
  // Your Code.
}
var header = {
    title: "header",
    icon: "project"
}
var testLists = [
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
```

</div>
</details>

<details>
<summary>HISTORY</summary>
<div>

### v1.0.0
Get Active value of Group item`s active.

### v0.9.0
add header`s icon


### v0.8.0
make base answer`s list

</div>
</details>
