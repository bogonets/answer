import VuexPersist from 'vuex-persist'

const PERSIST_KEY = 'answer';

export const vuexSessionStorage = new VuexPersist({
    key: PERSIST_KEY,
    storage: window.sessionStorage
})
export const vuexLocalStorage = new VuexPersist({
    key: PERSIST_KEY,
    storage: window.localStorage
})
