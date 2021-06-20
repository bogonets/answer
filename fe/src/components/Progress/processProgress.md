# HISTROY
## 0.9.0
Add Error funciton in list items.

## 0.8.0
make base answer`s progress


# How To
```html
<div style="width: 100%; height: 100%;">
  <v-loader 
  @allComplete="allTrueFunction"
  :serialize="true" 
  :loadList="listData">
  </v-loader>
</div>
```
```js
testFunction: function (arg1, arg2) {
  return otherFunction(arg1, arg2);
  //real return then or catch.
}
//or
testFunction2: function (resolve, reject) {
  setTimeout(() => { // for test delay.
    for (var i = 0; i < 9000; ++i) {
      resolve(true);
    }
  }, 7000)
}
allTrueFunction: function () {
  // all list item complete is success.
}
var listData = [
  {
    name: "test1 name",
    func: () => { 
        return new Promise((resolve, reject) => {
        testFunction("arg1", "arg2")
        .then(ans => {
                        setTimeout(() => { // for test delay.
                          resolve(true)
                        }, 3000)
                      })
        .catch(err => {
                        setTimeout(() => {
                          reject(false);
                        }, 3000)
                      })
        })
    },
    status: null,
    complete: false,
    onError: () => {}
  },
  {
    name: "test2 name",
    func: () => { 
        return new Promise((resolve, reject) => {
        testFunction2(resolve, reject)
    },
    status: null,
    complete: false,
    onError: () => { console.error('error!!'); }
  }
]
```