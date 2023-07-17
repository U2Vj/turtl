import '@mdi/font/css/materialdesignicons.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createVuetify, type ThemeDefinition } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { VDataTable } from 'vuetify/labs/VDataTable'
import 'vuetify/styles'
import App from './App.vue'
import router from './router'

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

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
