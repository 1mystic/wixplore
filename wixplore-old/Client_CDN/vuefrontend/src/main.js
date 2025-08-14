import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.use(router)
app.use(store)

app.config.errorHandler = (err, vm, info) => {
    console.error('Vue Error:', err)
    console.log('Error Info:', info)
}

app.mount('#app') 