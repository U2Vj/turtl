import App from './App.vue'
import router from './router'
import '@mdi/font/css/materialdesignicons.css'
import {createPinia} from 'pinia'
import {createApp} from 'vue'
import {createVuetify, type ThemeDefinition} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import {VDataTable} from 'vuetify/labs/VDataTable'
import 'vuetify/styles'
import Toast, {type PluginOptions, POSITION} from 'vue-toastification'
import 'vue-toastification/dist/index.css';

const turtlTheme: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#333399',
    cardColor: '#f5f5fa',
    finished: '#cfdd61',
    progress: '#7e86d0'
  }
}

const vuetify = createVuetify({
  components: {
    VDataTable,
    ...components
  },
  directives,
  theme: {
    defaultTheme: 'turtlTheme',
    themes: { turtlTheme }
  }
})

const app = createApp(App)

// The options for the used notification library (vue-toastification)
const toastificationOptions: PluginOptions = {
  transition: "Vue-Toastification__fade",
  maxToasts: 10,
  newestOnTop: true,
  timeout: 10000
}

app.use(createPinia())
app.use(router)
app.use(vuetify)
app.use(Toast, toastificationOptions)

app.mount('#app')
