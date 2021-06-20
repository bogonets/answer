import VuexPersist from 'vuex-persist'

export const vuexSessionStorage = new VuexPersist({
    key: 'vuex',
    storage: window.sessionStorage
})

export const vuexLocalStorage = new VuexPersist({
    key: 'vuex',
    storage: window.localStorage
})