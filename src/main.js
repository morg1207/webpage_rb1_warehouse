import "./assets/styles.css";
import "./assets/scripts.js";

import { createApp } from "vue";
import App from "./App.vue";

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.js'

// Make BootstrapVue available throughout your project

createApp(App).use(bootstrap).mount("#app");
