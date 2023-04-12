import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

import './assets/main.css'

import { createVuetify, type ThemeDefinition } from 'vuetify'
import * as components from 'vuetify/components'
import { VDataTable } from 'vuetify/labs/VDataTable'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

const turtlTheme: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#333399'
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

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
